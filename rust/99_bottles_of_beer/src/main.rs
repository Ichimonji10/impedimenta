// Prints the "99 Bottles of Beer On The Wall" song.
fn main() {
    for i in (1..100).rev() {
        println!("{} bottles of beer on the wall, {} bottles of beer!", i, i);
        if i > 2 {
            println!(
                "Take one down and pass it around, {} more bottles of beer on \
                 the wall!",
                i - 1
            );
        } else if i == 2 {
            println!(
                "Take one down and pass it around, one more bottle of beer on \
                 the wall!"
            );
        } else if i == 1 {
            println!(
                "Take one down and pass it around, no more bottles of beer \
                 on the wall!"
            );
        }
        if i > 1 {
            println!("");
        }
    }
}
