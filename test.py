#!/usr/bin/env python
import scramblesolver

board = ['A', 'S', 'B', 'E', 'I', 'R', 'U', 'A', 'H', 'E', 'N', 'T', 'O', 'I', 'D', 'E']

s = scramblesolver.ScrambleSolver()

s.set_board(board)
s.solve()
solutions = s.show_solutions()
words = s.show_words()

print "Solutions: "
print solutions
print "Words: "
print words
