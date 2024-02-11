input = list(open('input.txt'))

# part 1
def is_valid_passphrase_part_1(passphrase):
    words = passphrase.strip().split()
    return len(set(words)) == len(words)

# part 2

# def permutations(s):
#     '''
#     >>> list(permutations('a'))
#     ['a']
#     >>> list(permutations('ab'))
#     ['ab', 'ba']
#     >>> list(permutations('abc'))
#     ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']
#     '''
#     if len(s) == 0:
#         yield s
#         return
    
#     for i in range(len(s)):
#         head = s[i]
#         rest = s[:i] + s[i+1:]
#         for sub_p in permutations(rest):
#             yield head + sub_p

# def is_anagram(a, b):
#     return sorted(a) == sorted(b)

def is_valid_passphrase_part_2(passphrase):
    words = passphrase.strip().split()
    sorted_words = [''.join(sorted(w)) for w in words]
    return len(set(sorted_words)) == len(sorted_words)

if __name__ == '__main__':
    part_1 = sum(map(is_valid_passphrase_part_1, input))
    print(part_1)

    part_2 = sum(map(is_valid_passphrase_part_2, input))
    print(part_2)