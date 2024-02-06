def fibonacci(n):
    if n <= 2:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)
    
i = 1
fib_i = fibonacci(i)
acc = 0
while fib_i < 4000000:
    if fib_i % 2 == 0:
        acc += fib_i
    i += 1
    fib_i = fibonacci(i)

print(acc)