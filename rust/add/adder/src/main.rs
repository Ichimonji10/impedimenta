//! A simple demonstration of how to use workspaces.
//!
//! For more information, see [The Rust Programming Language, chapter 14,
//! section
//! 3](https://doc.rust-lang.org/stable/book/ch14-03-cargo-workspaces.html).

use add_one;
use add_two;

fn main() {
    println!("0 + 1 + 2 == {}", add_two::add_two(add_one::add_one(0)));
}
