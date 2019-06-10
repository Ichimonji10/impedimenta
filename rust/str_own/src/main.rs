// It's impossible to have a function whose return type is `str`. To understand
// why, let's talk about stack frames.
//
// "When a function gets called, some memory gets allocated for all of its local
// variables and some other information. This is called a ‘stack frame’." Only
// objects whose size is known at compile time can be stored on the stack.
//
// The requirement that stack variables have a size known at compile time makes
// certain constructs illegal. For example, the following is illegal:
//
//     fn make_str() -> str { "foo" }
//
// This is because `str` variables do not have a fixed size. This is in contrast
// to e.g. a `u32` variable. The notion that `str` variables do not have a fixed
// size may seem strange, but it's absolutely true. To illustrate a bit more,
// consider the following functions:
//
//     fn make_random_str() -> str { if … { "foo" } else { "barr" } }
//     fn make_random_u32() -> str { if … { 12345 } else { 23456  } }
//
// It's possible to work around this limitation by declaring a variable as
// static. This causes the variable's value to be hard-coded into the
// application binary and be loaded into static storage when the application
// starts. This allows the following to work:
//
//     fn make_random_str() -> &'static str { if … { "foo" } else { "barr" } }
//
// In this case, a reference to one of two memory locations in static storage is
// returned. This has obvious performance implications.
extern crate rand;
use rand::Rng;

fn main() {
    let fixed_str = make_fixed_str();
    println!("{}", fixed_str);

    let random_str = make_random_str();
    println!("{}", random_str);

    let fixed_string = make_fixed_string();
    println!("{}", fixed_string);

    let random_string = make_random_string();
    println!("{}", random_string);

    let s = if rand::thread_rng().gen_bool(0.5) {
        "foo"
    } else {
        "barr"
    };
    println!("{}", s);
}

fn make_fixed_str() -> &'static str {
    "fixed str"
}

fn make_random_str() -> &'static str {
    if rand::thread_rng().gen_bool(0.5) {
        "random str a"
    } else {
        "random str bb"
    }
}

fn make_fixed_string() -> String {
    "fixed string".to_string()
}

fn make_random_string() -> String {
    if rand::thread_rng().gen_bool(0.5) {
        "random string a".to_string()
    } else {
        "random string bb".to_string()
    }
}
