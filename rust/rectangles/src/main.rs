fn main() {
    let rect1 = Rectangle::square(50);
    let rect2 = Rectangle {
        width: rect1.width - 10,
        ..rect1
    };
    let rect3 = Rectangle {
        width: rect1.width - 10,
        height: rect1.height - 10,
    };

    println!("rect1 is {:?}", rect1);
    println!("The area of rect1 is {} square pixels.", rect1.area());
    println!("Can rect1 hold rect2? {}", rect1.can_hold(&rect2));
    println!("Can rect1 hold rect3? {}", rect1.can_hold(&rect3));
}

#[derive(Debug)]
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn square(size: u32) -> Rectangle {
        Rectangle {
            width: size,
            height: size,
        }
    }

    fn area(&self) -> u32 {
        self.width * self.height
    }

    fn can_hold(&self, other: &Rectangle) -> bool {
        self.width > other.width && self.height > other.height
    }
}
