# Fixed base

```
// big endian
N = [d0, d1, d2..., dn]
0 <= di < base
N = sum(di * base**i)
```

example binary
```
N = [1, 1, 0, 1]
N = 1 * 2**0 + 1 * 2**1 + 0 * 2**2 + 1 * 2**3 = 1 + 2 + 8 = 11
```

# Factorial base

```
// big endian
N = [d0, d1, d2..., dn]
0 <= di <= i
N = sum(di * fact(i))
```

example
```
N = [0, 1, 0, 2, 4]
N = 0*0! + 1*1! + 0*2! + 2*3! + 4*4! = 1 + 2*6 + 4*24 = 109
```
