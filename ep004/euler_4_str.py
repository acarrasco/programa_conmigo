def is_palindrome(original):
    s = str(original)
    return s == s[::-1]

m = max(i * j for i in range(100, 1000)
              for j in range(i, 1000)
              if is_palindrome(i * j))

print(m)