def gcd(a, b):
    '''
    >>> gcd(2, 4)
    2
    >>> gcd(3, 7)
    1
    >>> gcd(252, 105)
    21
    '''

    if a < b:
        a, b = b, a
    while a % b != 0:
        a, b = b, a % b
    return b


lcm = 1
for n in range(2, 21):
    lcm *= n // gcd(lcm, n)

print(lcm)