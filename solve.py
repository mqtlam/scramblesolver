#!/usr/bin/env python
import scramblesolver
import sys

board = sys.argv[1]
print "Input: " + board

s = scramblesolver.ScrambleSolver()
s.fast_solve(board)
