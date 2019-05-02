// From https://doc.rust-lang.org/book/ch08-03-hash-maps.html:
//
//     Given a list of integers, use a vector and return the mean (the average
//     value), median (when sorted, the value in the middle position), and mode
//     (the value that occurs most often; a hash map will be helpful here) of
//     the list.
use std::collections::HashMap;
use std::convert::TryFrom;

fn main() {
    let mut numbers: Vec<isize> = vec![1, 2, 1, 3];
    print_info(&numbers);
    numbers.push(3);
    print_info(&numbers);
    numbers.push(3);
    print_info(&numbers);
    numbers.push(-5);
    print_info(&numbers);
}

fn print_info(numbers: &Vec<isize>) {
    println!();
    println!("{:?}", numbers);
    println!("mean: {}", mean(&numbers));
    println!("median: {}", median(&numbers));
    println!("mode: {}", mode(&numbers));
}

fn mean(numbers: &Vec<isize>) -> isize {
    let mut sum: isize = 0;
    for number in numbers {
        sum += number;
    }
    sum / isize::try_from(numbers.len()).unwrap()
}

fn median(numbers: &Vec<isize>) -> isize {
    let mut sorted_numbers = numbers.clone();
    sorted_numbers.sort_unstable();
    let mid_index: usize = sorted_numbers.len() / 2;
    sorted_numbers[mid_index]
}

fn mode(numbers: &Vec<isize>) -> isize {
    let mut counts: HashMap<isize, usize> = HashMap::new();
    for &number in numbers {
        let count = counts.entry(number).or_insert(0);
        *count += 1;
    }

    let mut candidate_key: Option<isize> = None;
    let mut candidate_val: Option<usize> = None;
    for (&key, &val) in counts.iter() {
        candidate_key.get_or_insert(key);
        candidate_val.get_or_insert(val);
        if val > candidate_val.unwrap() {
            candidate_key.replace(key);
            candidate_val.replace(val);
        }
    }
    candidate_key.unwrap()
}
