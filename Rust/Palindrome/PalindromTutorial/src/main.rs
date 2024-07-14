// std is used for modules like in C++
// io is for input and output
// Write allows to write some data into an object
// self brings io into scope, makes it so you can refer to the module as io
// Write brings Write into scope, allowing the use of methods without having to prefix std::io::Write
use std::io::{self, Write};

fn main() {
    print!("Type a word to check for a palindrome -> ");
    // stdout() constructs a new handle to the current output
    // what is a handle? -> an object that acts as an interface for some resource (in this case to the stdout), this allows you to perform things like writing text to the terminal
    // current output typically referes to the terminal or console
    // flush() ensures all intermediately buffered contents reach their destination?
    // -> makes sure all the data gets sent out immediately, in this case straight to the terminal/console
    // what is a buffer? -> a temporary storage area
    // unwrap() returns an okay value of self?
    // -> allows you to get the data that's been wrapped up in something
    io::stdout().flush().unwrap();

    let mut word = String::new();

    // stdin() constructs a new handle to the current input
    // read_line() reads the line and appends it to the variable
    // expect() checks if it's valid and presents a message if failed
    io::stdin().read_line(&mut word).expect("Failed to read");
    let word = word.trim(); // Trims any whitespace

    if palindrome(word) {
        println!("{word} is a palindrome!");
    } else {
        println!("{word} is not a palindrome!");
    }
}

// & reads in the value, not making a copy, but cannot change the original value
fn palindrome(word: &str) -> bool {
    // chars() iterates through each character in a string
    // filter() will filter through each character
    // -> filters use closures, closures work like lambdas (|parameter| expression) and only returns the parts that are true
    // is_ascii_alphanumeric() will check if it's alphanumeric, returning false if not
    // collect will convert any iterator data into a collection
    // what's a collection? -> just a variable of the final output really
    let sanitize: String = word.chars().filter(|word| word.is_ascii_alphanumeric()).collect::<String>().to_lowercase();

    // rev() makes it iterate right to left instead of left to right
    // adding a ; at the end breaks it... why?
    // -> ; turns the line into a statement, so if there's no ;, then it is never turned into a statement treats it as the return value
    // -> BUT you CAN use the return keyword to explicity state a return, in which case adding a ; to the end is fine
    return sanitize == sanitize.chars().rev().collect::<String>();
}
