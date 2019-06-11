// As per the std::str documentation, the following are equivalent:
//
//     let hello_world = "Hello, World!";
//     let hello_world: &'static str = "Hello, World!";
//
// Also:
//
//     String literals have a static lifetime, which means the string
//     hello_world is guaranteed to be valid for the duration of the entire
//     program.
//
// With this in mind, consider the definintion of Foo, below. The lifetime
// annotations state that Foo's lifetime is less than or equal to bar's
// lifetime.
//
// new() and make_foo() can be read in similar ways:
//
// #.   `bar` has a static lifetime.
// #.   Therefore, Foo has a lifetime less than or equal to static.
// #.   Therefore, 'b and 'c denote lifetimes less than or equal to static.

fn main() {
    let foo = Foo::new();
    println!("{:?}", foo);

    let foo = make_foo();
    println!("{:?}", foo);
}

#[derive(Debug)]
struct Foo<'a> {
    bar: &'a str,
}

impl<'b> Foo<'b> {
    fn new() -> Foo<'b> {
        Foo { bar: "bar" }
    }
}

fn make_foo<'c>() -> Foo<'c> {
    Foo { bar: "bar" }
}
