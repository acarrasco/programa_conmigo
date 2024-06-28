const PERIMETER : u32 = 1000;

fn main() {
    for a in 1..PERIMETER / 3 {
        for b in a + 1 .. (PERIMETER-1-a) / 2 {
            let c = PERIMETER - a - b;
            if a * a + b * b == c * c {
                println!("{}", a * b * c);
            }
        }
    }
}
