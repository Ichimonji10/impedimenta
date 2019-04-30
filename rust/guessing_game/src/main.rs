// A simple game: guess a randomly generated number!
extern crate rand;

use rand::Rng;
use std::cmp::Ordering;
use std::io::stdin;

fn main() {
    let secret_number = rand::thread_rng().gen_range(1, 101);
    println!(
        "Welcome to the guessing game! Your objective is to guess a randomly \
         generated number."
    );
    loop {
        // Fetch a guess from the user.
        println!("Guess a number.");
        let mut str_guess = String::new();
        stdin()
            .read_line(&mut str_guess)
            .expect("Failed to read line.");
        let guess: u32 = match str_guess.trim().parse() {
            Ok(num) => num,
            Err(msg) => {
                println!("Whoops! Input isn't a number. (Error: {})", msg);
                continue;
            }
        };

        // Compare the user's guess to the secret_number
        match guess.cmp(&secret_number) {
            Ordering::Less => println!("Too small."),
            Ordering::Equal => {
                println!("Just right.");
                break;
            }
            Ordering::Greater => println!("Too large."),
        }
    }
}
