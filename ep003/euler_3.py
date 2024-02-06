n = 600851475143

factor = 1

while n > 1:
    if n % factor == 0:
        n //= factor
    else:
        factor += 1

print(factor)