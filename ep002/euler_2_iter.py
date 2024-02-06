def fibonacci(n):
    a = 1
    b = 1
    for _ in range(n):
        t = a + b
        a = b
        b = t
    return b
    
i = 1
fib_i = fibonacci(i)
acc = 0
while fib_i < 4000000:
    if fib_i % 2 == 0:
        acc += fib_i
    i += 1
    fib_i = fibonacci(i)

print(acc)