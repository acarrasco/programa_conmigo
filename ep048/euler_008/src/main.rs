use std::fs;

const NUMBER_SIZE : usize = 1000;
const PRODUCT_DIGITS : usize = 13;

fn digits_product(string: &String, start: usize, size: usize) -> u64 {
    let mut result: u64= 1;

    let slice = &string[start..start+size];
    for digit in slice.chars() {
        result *= digit.to_digit(10).expect("invalid digit") as u64;
    }

    return result;
}

fn main() {
    let long_number = fs::read_to_string("long_number.txt")
        .expect("error reading file")
        .chars()
        .filter(|x| x.is_digit(10))
        .collect();

    let mut largest_product = 0;
    for start in 0..NUMBER_SIZE-PRODUCT_DIGITS {
        let candidate = digits_product(&long_number, start, PRODUCT_DIGITS);
        if candidate > largest_product {
            largest_product = candidate;
        }
    }

    println!("{}", largest_product);
}
