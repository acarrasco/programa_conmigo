import re
import heapq

ROOM_EXP = r'([a-z-]+)-([0-9]+)\[([a-z]{5})\]'

def parse_room(line):
    m = re.match(ROOM_EXP, line.strip())
    encrypted_name, sector, checksum = m.groups()
    return encrypted_name, int(sector), checksum

def is_valid_room(encrypted_name, checksum):
    '''
    >>> is_valid_room('aaaaa-bbb-z-y-x', 'abxyz')
    True
    >>> is_valid_room('a-b-c-d-e-f-g-h', 'abcde')
    True
    >>> is_valid_room('not-a-real-room', 'oarel')
    True
    >>> is_valid_room('totally-real-room', 'decoy')
    False
    '''
    def key(c):
        if c == '-':
            return (0, c)
        return -encrypted_name.count(c), c
    calculated_checksum = heapq.nsmallest(5, set(encrypted_name), key=key)
    return ''.join(calculated_checksum) == checksum

def get_valid_room_sector(room):
    '''
    >>> get_valid_room_sector(('aaaaa-bbb-z-y-x', 12345, 'abxyz'))
    12345
    >>> get_valid_room_sector(('totally-real-room', 2526, 'decoy'))
    0
    '''
    encrypted_name, sector, checksum = room
    if is_valid_room(encrypted_name, checksum):
        return sector
    else:
        return 0

def part_1(rooms):
    return sum(map(get_valid_room_sector, rooms))


LAST_CHARACTER = ord('z')
FIRST_CHARACTER = ord('a')
ALPHABET_SIZE = LAST_CHARACTER - FIRST_CHARACTER + 1

def decrypt_room_name(encrypted_name, sector):
    '''
    >>> decrypt_room_name('abcd', 1)
    'bcde'
    >>> decrypt_room_name('abcd', 26)
    'abcd'
    >>> decrypt_room_name('abcd', 27)
    'bcde'
    >>> decrypt_room_name('qzmt-zixmtkozy-ivhz', 343)
    'very encrypted name'
    '''
    def shift(c):
        if c == '-':
            return ' '
        i = ord(c) - FIRST_CHARACTER
        return chr((i + sector) % ALPHABET_SIZE + FIRST_CHARACTER)
    return ''.join(map(shift, encrypted_name))

def part_2(rooms):
    for room in rooms:
        encrypted_name, sector, checksum = room
        decrypted_room_name = decrypt_room_name(encrypted_name, sector)
        if "north" in decrypted_room_name:
            print(decrypted_room_name, sector)

if __name__ == '__main__':
    input = open('input.txt').readlines()
    rooms = [parse_room(line) for line in input]
    print(part_1(rooms))
    part_2(rooms)
