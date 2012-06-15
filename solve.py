#!/usr/bin/env python
import scramblesolver
import sys

if len(sys.argv) != 2:
	print 'Usage: ./scramblesolver abcdefghijklmnoqu'
	sys.exit(1)

board = sys.argv[1]
print "Input: " + board

s = scramblesolver.ScrambleSolver()
s.fast_solve(board)
