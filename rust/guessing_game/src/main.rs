// A simple game: guess a randomly generated number!
extern crate rand;

use rand::Rng;
use std::cmp::Ordering;
use std::io::stdin;

pub const MIN: i32 = 1;
pub const MAX: i32 = 100;

fn main() {
    let secret_number = rand::thread_rng().gen_range(MIN, MAX + 1);
    println!(
        "Welcome to the guessing game! Your objective is to guess a randomly \
         generated number. The number is between {} and {}, inclusive.",
        MIN, MAX
    );
    loop {
        // Fetch a guess from the user.
        println!("Guess a number.");
        let mut str_guess = String::new();
        stdin()
            .read_line(&mut str_guess)
            .expect("Failed to read line.");
        let guess: Guess = match str_guess.trim().parse() {
            Err(msg) => {
                println!("Error: {}", msg);
                continue;
            }
            Ok(int_guess) => match Guess::new(int_guess) {
                Err(msg) => {
                    println!("Error: {}", msg);
                    continue;
                }
                Ok(guess) => guess,
            },
        };

        // Compare the user's guess to the secret_number
        match guess.value().cmp(&secret_number) {
            Ordering::Less => println!("Too small."),
            Ordering::Equal => {
                println!("Just right.");
                break;
            }
            Ordering::Greater => println!("Too large."),
        }
    }
}

pub struct Guess {
    value: i32,
}

impl Guess {
    pub fn new(value: i32) -> Result<Guess, String> {
        if value < MIN || value > MAX {
            Err(format!(
                "Guess value must be between 1 and 100 inclusive, got {}.",
                value
            ))
        } else {
            Ok(Guess { value })
        }
    }

    pub fn value(&self) -> i32 {
        self.value
    }
}
