def fibonacci(until):
    a = 1
    b = 1
    while b < until:
        yield b
        a, b = b, a + b
    
print(sum(n for n in fibonacci(4000000) if n % 2 == 0))
