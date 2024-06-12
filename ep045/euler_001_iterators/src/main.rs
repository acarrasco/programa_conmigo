fn is_multiple_of_three_or_five(x: &u32) -> bool {
    return x % 3 == 0 || x % 5 == 0;
}

fn main() {
    let sequence = 1..1000;
    let multiples_of_three_and_five = sequence.filter(is_multiple_of_three_or_five);
    let result: u32 = multiples_of_three_and_five.sum();
    println!("{}", result);
}
