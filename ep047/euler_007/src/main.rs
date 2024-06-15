const LIMIT: usize = 10001;

struct MyPrimes {
    data: [u128; LIMIT],
    size: usize,
}

fn is_prime(primes: &MyPrimes, n: u128) -> bool {
    for i in 0..primes.size {
        if n % primes.data[i] == 0 {
            return false;
        }
    }
    return true;
}

fn next_prime(primes: &mut MyPrimes) -> u128 {
    let last_prime = primes.data[primes.size - 1];
    let mut candidate = last_prime + 2;
    while !is_prime(primes, candidate) {
        candidate += 2;
    }
    primes.data[primes.size] = candidate;
    primes.size += 1;
    return candidate;
}

fn main() {
    let mut primes = MyPrimes {
        data: [0; LIMIT],
        size : 2,
    };
    primes.data[0] = 2;
    primes.data[1] = 3;

    for _ in primes.size..LIMIT {
        next_prime(&mut primes);
    }
    println!("{}", primes.data[LIMIT-1]);
}
