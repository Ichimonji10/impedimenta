//! Inspect and interact with the desktop notification service.
//!
//! This crate provides tools for interacting with the desktop notification
//! service via D-Bus. D-Bus is a message bus targeted primarily at single-host
//! IPC. It's cross-platform, but is deployed almost exclusively on Linux
//! distributions. The desktop notification service is the service which, among
//! other things, generates pop-up notifications.
//!
//! This crate should not be taken seriously. It's a [breakable
//! toy](https://www.oreilly.com/library/view/apprenticeship-patterns/9780596806842/ch05s03.html).
//!
//! For more information, see:
//!
//! *   [D-Bus](https://www.freedesktop.org/wiki/Software/dbus/)
//! *   [Desktop Notifications Specification](https://developer.gnome.org/notification-spec/)

use std::cmp;
use std::collections::HashMap;

extern crate clap;
extern crate dbus;
extern crate serde_json;
extern crate textwrap;
use clap::{App, AppSettings, Arg, ArgMatches, SubCommand};
use dbus::arg::{RefArg, Variant};

/// On narrow terminals, text shall be wrapped to the width of the terminal. On
/// wide terminals, text shall be wrapped at an arbitrary bound. This latter
/// requirement aids readability, as failing to wrap code on especially wide
/// terminals harms legibility.
static MAX_WIDTH: usize = 100;

/// Used by [notify](fn.notify.html) when generating a notification.
///
/// Here's a very dumb doctest:
///
/// ```
/// let _not = not_gen::Notification {
///     summary: "Message from Alice".to_owned(),
///     body: "Knock knock!".to_owned(),
/// };
/// ```
#[derive(Debug)]
pub struct Notification {
    pub summary: String,
    pub body: String,
}

pub fn get_cli_args<'a>() -> ArgMatches<'a> {
    let summary_help = textwrap::dedent(
        r###"
        This is a single line overview of the notification. For instance, "You
        have mail" or "A friend has come online". It should generally not be
        longer than 40 characters, though this is not a requirement, and server
        implementations should word wrap if necessary. The summary must be
        encoded using UTF-8.
        "###,
    )
    .trim()
    .replace("\n", " ");

    let body_help = textwrap::dedent(
        r###"
        This is a multi-line body of text. Each line is a paragraph, server
        implementations are free to word wrap them as they see fit.

        The body may contain simple markup as specified in Markup. It must be
        encoded using UTF-8.

        If the body is omitted, just the summary is displayed.
        "###,
    )
    .trim()
    .replace("\n", " ");

    App::new("Notification Generator")
        .version("0.0.1")
        .author("Jeremy Audet <jerebear@protonmail.com>")
        .about("Generate desktop notifications.")
        .setting(AppSettings::SubcommandRequiredElseHelp)
        .subcommand(
            SubCommand::with_name("list-caps")
                .about("List notifier capabilities.")
                .arg(
                    Arg::with_name("format")
                        .long("format")
                        .takes_value(true)
                        .possible_value("json")
                        .possible_value("prose")
                        .default_value("prose")
                        .help("How to format output."),
                ),
        )
        .subcommand(
            SubCommand::with_name("notify")
                .about("Generate a desktop notification.")
                .arg(
                    Arg::with_name("summary")
                        .long("summary")
                        .takes_value(true)
                        .default_value("")
                        .help(&summary_help),
                )
                .arg(
                    Arg::with_name("body")
                        .long("body")
                        .takes_value(true)
                        .default_value("")
                        .help(&body_help),
                ),
        )
        .get_matches()
}

pub fn list_caps(format: &str) {
    let conn = dbus::Connection::get_private(dbus::BusType::Session)
        .expect("Failed to establish connection to session bus.");

    let destination = "org.freedesktop.Notifications";
    let path = "/org/freedesktop/Notifications";
    let iface = "org.freedesktop.Notifications";
    let name = "GetCapabilities";
    let req = dbus::Message::new_method_call(destination, path, iface, name)
        .expect("Failed to compile message due to invalid headers.");

    let resp = conn
        .send_with_reply_and_block(req, 5000)
        .expect("Method call failed.");
    let capabilities: Vec<String> = resp.read1().expect("Failed to unpack response body.");

    match format {
        "json" => list_caps_as_json(&capabilities),
        "prose" => list_caps_as_prose(&capabilities),
        _ => panic!(
            "'{}' formatting hasn't been implemented. Please contact the developers",
            format
        ),
    }
}

fn list_caps_as_prose(capabilities: &[String]) {
    let descriptions = get_cap_descriptions();
    let mut wrapper = textwrap::Wrapper::new(get_wrapper_width());
    println!(
        "{}",
        wrapper.fill("The current notifications server supports the following capabilities:\n",)
    );
    wrapper.initial_indent = "    ";
    wrapper.subsequent_indent = "    ";
    for capability in capabilities {
        println!("{}", capability);
        let description = match descriptions.get(capability) {
            Some(value) => value,
            None => "No description.",
        };
        println!("{}", wrapper.fill(description));
    }
}

fn list_caps_as_json(capabilities: &[String]) {
    let descriptions = get_cap_descriptions();
    let mut present_capabilities: HashMap<&str, &str> = HashMap::new();
    for capability in capabilities {
        let description = match descriptions.get(capability) {
            Some(desc) => desc,
            None => "Unknown capability! No description available.",
        };
        present_capabilities.insert(capability, description);
    }
    let serialized = serde_json::to_string(&present_capabilities).unwrap();
    println!("{}", serialized);
}

/// Generate a desktop notification (i.e. a pop-up).
///
/// Synchronous, with a five second timeout when sending a message. Will panic
/// if:
///
/// *   Connecting to the session bus fails.
/// *   Compiling a message fails.
/// *   Sending the message fails.
pub fn notify(notification: &Notification) {
    let conn = dbus::Connection::get_private(dbus::BusType::Session)
        .expect("Failed to establish connection to session bus.");

    let destination = "org.freedesktop.Notifications";
    let path = "/org/freedesktop/Notifications";
    let iface = "org.freedesktop.Notifications";
    let name = "Notify";
    let app_name = "Notification Generator";
    let replaces_id: u32 = 0;
    let app_icon = "";
    let summary = &notification.summary;
    let body = &notification.body;
    let actions: Vec<String> = vec![];
    let hints: HashMap<String, Variant<Box<dyn RefArg>>> = HashMap::new();
    let expire_timeout: i32 = -1;
    let req = dbus::Message::new_method_call(destination, path, iface, name)
        .expect("Failed to compile message due to invalid headers.")
        .append1(app_name)
        .append1(replaces_id)
        .append1(app_icon)
        .append1(summary)
        .append1(body)
        .append1(actions)
        .append1(hints)
        .append1(expire_timeout);

    conn.send_with_reply_and_block(req, 5000)
        .expect("Method call failed.");
}

fn get_wrapper_width() -> usize {
    cmp::min(textwrap::termwidth(), MAX_WIDTH)
}

fn get_cap_descriptions() -> HashMap<String, String> {
    vec![
        (
            "action-icons",
            r###"
            Supports using icons instead of text for displaying actions. Using
            icons for actions must be enabled on a per-notification basis using
            the "action-icons" hint.
            "###,
        ),
        (
            "actions",
            r###"
            The server will provide the specified actions to the user. Even if
            this cap is missing, actions may still be specified by the client,
            however the server is free to ignore them.
            "###,
        ),
        (
            "body",
            r###"
            Supports body text. Some implementations may only show the summary
            (for instance, onscreen displays, marquee/scrollers)
            "###,
        ),
        (
            "body-hyperlinks",
            r###"
            The server supports hyperlinks in the notifications.
            "###,
        ),
        (
            "body-images",
            r###"
            The server supports images in the notifications.
            "###,
        ),
        (
            "body-markup",
            r###"
            Supports markup in the body text. If marked up text is sent to a
            server that does not give this cap, the markup will show through as
            regular text so must be stripped clientside.
            "###,
        ),
        (
            "icon-multi",
            r###"
            The server will render an animation of all the frames in a given
            image array.  The client may still specify multiple frames even if
            this cap and/or "icon-static" is missing, however the server is free
            to ignore them and use only the primary frame.
            "###,
        ),
        (
            "icon-static",
            r###"
            Supports display of exactly 1 frame of any given image array. This
            value is mutually exclusive with "icon-multi", it is a protocol
            error for the server to specify both.
            "###,
        ),
        (
            "persistence",
            r###"
            The server supports persistence of notifications. Notifications will
            be retained until they are acknowledged or removed by the user or
            recalled by the sender. The presence of this capability allows
            clients to depend on the server to ensure a notification is seen and
            eliminate the need for the client to display a reminding function
            descriptions.insert(such as a status icon) of its own.
            "###,
        ),
        (
            "sound",
            r###"
            The server supports sounds on notifications. If returned, the server
            must support the "sound-file" and "suppress-sound" hints.
            "###,
        ),
    ]
    .iter()
    .map(|pair| {
        (
            pair.0.to_string(),
            textwrap::dedent(pair.1).trim().replace("\n", " "),
        )
    })
    .collect()
}
