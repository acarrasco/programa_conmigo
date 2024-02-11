#!/usr/bin/python

import hashlib
import sys
import curses
from itertools import count
import random

input = sys.argv[1]

PROOF_OF_WORK_SIZE = 5
LEADING_ZEROES = '0' * PROOF_OF_WORK_SIZE
PASSWORD_SIZE = 8
RANDOM_CHARACTERS = [chr(i) for i in range(ord('0'), ord('z') + 1)] 

def calculate_valid_hashes(input, progress_callback, progress_tick):
    for i in count():
        if i % progress_tick == 0:
            progress_callback(i)
        text_to_check = input + str(i)
        hash = hashlib.md5(text_to_check.encode('utf-8')).hexdigest()
        if hash.startswith(LEADING_ZEROES):
            yield hash


part_1_password = []
part_2_password = [None] * PASSWORD_SIZE

def solve(stdscr):
    stdscr.clear()

    part_1_windows = [
        stdscr.derwin(2, 2, 1, 2 * i, ) for i in range(PASSWORD_SIZE)
    ]
    part_2_windows = [
        stdscr.derwin(2, 2, 2, 2 * i,) for i in range(PASSWORD_SIZE)
    ]

    def show_password(password, windows):
        for c, w in zip(password, windows):
            w.addch(0, 0, c or random.choice(RANDOM_CHARACTERS))
            w.refresh()

    def progress(i):
        password_1_padded = part_1_password + [None] * (PASSWORD_SIZE - len(part_1_password))
        show_password(password_1_padded, part_1_windows)
        show_password(part_2_password, part_2_windows)

    for hash in calculate_valid_hashes(input, progress, 10**5):
        if len(part_1_password) < PASSWORD_SIZE:
            part_1_password.append(hash[PROOF_OF_WORK_SIZE])
        position = int(hash[PROOF_OF_WORK_SIZE], base=16)
        if position < PASSWORD_SIZE and part_2_password[position] == None:
            part_2_password[position] = hash[PROOF_OF_WORK_SIZE + 1]
            if all(part_2_password):
                break

curses.wrapper(solve)
print(''.join(part_1_password))
print(''.join(part_2_password))
