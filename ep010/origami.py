from functools import reduce

def my_map(func, seq):
    def map_f(acc, v):
        return acc + [func(v)]
    
    return reduce(map_f, seq, [])

print(list(map(lambda x: x*x, range(10))))
print(my_map(lambda x: x*x, range(10)))


def my_filter(func, seq):
    def filter_f(acc, v):
        if func(v):
            return acc + [v]
        else:
            return acc

    return reduce(filter_f, seq, [])

print(list(filter(lambda x: x % 2, range(10))))
print(my_filter(lambda x: x % 2, range(10)))
