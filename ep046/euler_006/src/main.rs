use std::ops::Range;

fn sum_squares(sequence: &Range<i32>) -> i32 {
    return sequence.clone().map(|x| x*x).sum();
}

fn main() {
    let seq: Range<i32> = 1..101;
    let seq_sum: i32 = seq.clone().sum();
    let result = (sum_squares(&seq) - seq_sum.pow(2)).abs();
    println!("{}", result);
}
