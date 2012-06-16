#!/usr/bin/env python
import scramblesolver
import sys

if len(sys.argv) < 2:
	print 'Usage: ./scramblesolver abcdefghijklmnoqu'
	sys.exit(1)

board = sys.argv[1]
special = '0000000000000000'
if len(sys.argv) > 2:
	special = sys.argv[2]

s = scramblesolver.ScrambleSolver()
s.fast_solve(board, special)
