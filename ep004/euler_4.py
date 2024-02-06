def is_palindrome(original):
    n = original
    r = 0

    while n > 0:
        r = r * 10 + n % 10
        n //= 10

    return r == original

m = max(i * j for i in range(100, 1000)
              for j in range(i, 1000)
              if is_palindrome(i * j))

print(m)