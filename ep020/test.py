#!/usr/bin/python

import hashlib
import sys
import curses
from itertools import count
import random

def main(stdscr):
    stdscr.clear()

    window = curses.newwin(10, 10, 1, 1)
    window.addstr('hola')
    # stdscr.refresh()
    window.refresh()

    input()

curses.wrapper(main)