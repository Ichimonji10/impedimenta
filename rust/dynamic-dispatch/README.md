Dynamic Dispatch
================

Compiling should give the following error:

    error[E0225]: only auto traits can be used as additional traits in a trait object
      --> src/main.rs:11:36
       |
    11 |     subjects: Vec<Box<dyn Mammal + Clone>>,
       |                           ------   ^^^^^
       |                           |        |
       |                           |        additional non-auto trait
       |                           |        trait alias used in trait object type (additional use)
       |                           first non-auto trait
       |                           trait alias used in trait object type (first use)

For details, see `rustc --explain E0225` and [Exploring Dynamic Dispatch in
Rust](https://alschwalm.com/blog/static/2017/03/07/exploring-dynamic-dispatch-in-rust/).
