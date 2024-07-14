use std::fs::File; // Used to interact with files on the system
// Imports io and bufread
// BufRead imports buffered reading capabilities, adding efficient methods that can be used
// You would use BufRead to read lines from a file
use std::io::{self, BufRead};
// Reads in paths in a platform-free way (works cross platform)
// Used to check if files exists, join paths, extract components from paths etc.
use std::path::Path;

fn main() {
    let filePath = "test.txt";
    let targetWord = "okay";

    if let Err(err) = wordFinder(filePath, targetWord) {
        eprintln!("Error searching for wordL {}", err);
    }
}

// io::Result<()> is a type alias that represents the result of an I/O operation that could potentially result in an error
// Result is an enum defined within io that represents the result of an operation that may fail
// () is Rusts unit type, similar to void in C++, it signifies that the result type of the operation is empty or does not carry any meaningful data when it succeeds
// Result has two variants Ok(T) and Err(E), T carries the type value and E carries the error value
// io::Result<()> specifies that the operation returns a Result where:
// Ok(()) says the I/O operation was successful and returns the type ()
// Err(io::Error) is used when an I/O error occurred during the operation and it contains details about the error in the form of an io::Error type
// Functions that perform I/O operations (like reading from a file, writing to a socket), io::Result<()> is often used as the return type to indicate a success or failure of the operation
// () signifies that no meaningful data is returned upon success, success is indicated by a lack of an error
fn wordFinder(_filePath: &str, _targetWord: &str) -> io::Result<()> {
    let path = Path::new(_filePath);

    // & creates a reference to that variable instead of changing owernship (moves the value) or copying it's value (which can be expensive for larger data)
    // ? checks if it exists and returns false if it doesn't
    let file = File::open(&path)?;

    // Create a vector to hold all the words
    // Vec acts like arrays/lists
    // It can dynamically grow and shrink
    // Elements in Vecs can be accessed via vec[index]
    let reader = io::BufReader::new(file);
    let mut numberOfWords = Vec::new();

    // i32 is a signed 32-bit integer
    // Range: -2,147,483,648 to 2,147,483,647
    // Sign can represent both positive and negative integers
    // Takes up 32 bits or 4 bytes of memory
    // Useful when dealing with mumbers that can be negative or positive
    // u32 is an unsigned 32-bit integer
    // Range: 0 to 4,294,967,295
    // Sign represents only non-negative integers (0 and up)
    // Takes up 32 bits or 4 bytes of memory
    // Useful for cases where only non-negative numbers are expected or when you need to store large values wihtout negative numbers
    // i64 and u64 also exist (takes 8 bytes)
    // i64 range is -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807
    // u63 range is 0 to 18,446,744,073,709,551,615
    let mut lineNum : i32 = 0;
    for line in reader.lines() {
        lineNum += 1;
        let line = line?;

        let mut colNum : i32 = 0;
        for word in line.split_whitespace() {
            let word : String = word.chars().filter(|c| c.is_ascii_alphanumeric()).collect::<String>().to_lowercase();
            colNum += 1;

            if word == _targetWord {
                // Vecs can store tuples like in python
                // Tuples are a fixed-size ordered list of elements that can be of different types and their size is fixed once they're created
                // Tuples are often used to group together elements of different types when the exact number of elements needed is known and relatively small
                numberOfWords.push((lineNum, colNum, word.to_string()));
            }
        }
    }

    // This syntax is called destrcuturing
    // Allows to unpack each tuple element from each tuple contained within the vector
    for (lineNum, colNum, word) in numberOfWords {
        println!("{} -> at {}:{}", word, lineNum, colNum);
    }

    Ok(())
}
