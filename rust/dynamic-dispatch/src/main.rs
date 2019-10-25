fn main() {
    println!("Hello, world!");
}

trait Mammal {
    fn walk(&self);
    fn run(&self);
}

struct CloningLab {
    subjects: Vec<Box<dyn Mammal + Clone>>,
}
