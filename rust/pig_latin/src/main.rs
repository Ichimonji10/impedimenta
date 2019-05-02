// From https://doc.rust-lang.org/book/ch08-03-hash-maps.html:
//
//     Convert strings to pig latin. The first consonant of each word is moved
//     to the end of the word and “ay” is added, so “first” becomes “irst-fay.”
//     Words that start with a vowel have “hay” added to the end instead
//     (“apple” becomes “apple-hay”). Keep in mind the details about UTF-8
//     encoding!
//
// Some examples:
//
//  a    →  a-hay
//  art  →  art-hay
//  b    →  -bay
//  bar  →  ar-bay
//
fn main() {
    let phrases = vec![
        "a",
        "art",
        "f",
        "foo",
        "ƒ",
        "ƒoo",
        "",
        " ",
        " foo…bar …biz… ",
    ];
    for phrase in phrases {
        for word in phrase.split_whitespace() {
            println!("{} → {}", &word, pigize(&word));
        }
    }
}

fn pigize(word: &str) -> String {
    let first_char = match word.chars().next() {
        Some(_first_char) => _first_char,
        None => ' ',
    };
    let pig_word = match first_char {
        'a' | 'e' | 'i' | 'o' | 'u' => format!("{}-hay", word),
        ' ' => String::from(""),
        _ => {
            let mut temp = String::from(word);
            temp.remove(0);
            format!("{}-{}ay", temp, first_char)
        }
    };
    pig_word
}
