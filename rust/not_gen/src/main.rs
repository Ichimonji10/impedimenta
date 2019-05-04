use std::process;

fn main() {
    let args = not_gen::get_cli_args();
    match args.subcommand() {
        ("list-caps", Some(args_sub)) => {
            let format = args_sub.value_of("format").unwrap().to_string();
            not_gen::list_caps(&format)
        }
        ("notify", Some(args_sub)) => {
            let summary = args_sub.value_of("summary").unwrap().to_string();
            let body = args_sub.value_of("body").unwrap().to_string();
            let notification = not_gen::Notification { summary, body };
            not_gen::notify(&notification)
        }
        _ => {
            eprintln!("An unexpected code path executed. Please contact the developer.");
            process::exit(1);
        }
    }
}
