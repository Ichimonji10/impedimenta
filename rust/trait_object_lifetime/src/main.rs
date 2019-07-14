//! Adapted from The Rust book, section 19.2: "Advanced Lifetimes."

trait Red {}

struct Ball<'a> {
    radius: &'a f64,
}

impl<'b> Ball<'b> {}

impl<'c> Red for Ball<'c> {}

fn main() {
    let radius = 5.0;

    // "_red_obj is a box referencing an object that implements Red." Red doesn't use any lifetimes,
    // so we can't explicitly annotate lifetimes. If it did, we could add explicit annotations:
    //
    //     Box<dyn Red + 'a>
    //     Box<dyn Red + 'static>
    //
    let _red_obj: Box<dyn Red> = Box::new(Ball { radius: &radius });
    println!("Red object might or might not have a radius.");

    let red_ball: Box<Ball> = Box::new(Ball { radius: &radius });
    println!("Red ball has a radius: {}", red_ball.radius);
}
