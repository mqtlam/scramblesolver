#! /usr/bin/env python

class ScrambleSolver:
	"""ScrambleSolver solves a Scramble board configuration by 
	listing all the possible solutions."""

	def __init__(self, dictionary = 'dictionary.txt', points = 'points.txt'):
		# Load dictionary
		f = open(dictionary, 'r')
		self.dictionary = []
		for line in f:
			self.dictionary.append(line.strip())
		f.close()

		# Load points definitions
		f = open(points, 'r')
		self.points = {}
		for line in f:
			[letter, points] = line.strip().split(' ')
			self.points[letter] = int(points)
		f.close()
		
		# Current board configuration
		# List of 16 characters, where 'QU' is a character.
		self.board = []

		# Current solutions
		# List of pairs: (sequence of positions, word, points)
		self.solutions = []

		# Solved or not
		self.solved = False

	def fast_solve(self, board, special = '0000000000000000'):
		"""Solves the board and displays the results. Accepts a string of characters.
		Note: the letter qu should be represented like that."""
		board = board.upper()
		board_list = []
		for char in board:
			if char == 'Q':
				board_list.append('QU')
			elif len(board_list) == 0 or board_list[-1] != 'QU' or char != 'U':
				board_list.append(char)

		special_list = []
		for char in special:
			special_list.append(char)

		self.set_board(board_list, special_list)
		self.solve()
		solutions = self.show_solutions()
		points_words = self.format_solutions(self.show_solutions_sorted_by_points(), [1,2])

		print "\nSolutions: "
		print solutions
		print "\nSorted by Points: "
		print points_words

	def set_board(self, board, special = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
		"""Sets the board configuration. Accepts a list of characters/strings.
		Note: the letter 'QU' should be represented like that."""
		self.board = board
		self.special = special
		self.solutions = []
		self.solved = False

	def solve(self):
		"""Solves the board only and stores the results."""
		self.solutions = [] 
		for pos in range(0, 15):
			words = self.starts_with(self.board[pos], self.dictionary)
			self.solutions = self.solutions + self.solve_helper([pos], words)
		self.solved = True
		print "\nDone solving!"

	def solve_helper(self, sequence, words):
		"""Helper for solving the board."""
		results = []

		current = sequence[-1]
		if words != []:
			neighbors = self.get_neighbors(current)
			to_explore_list = [item for item in neighbors if item not in sequence]
			for to_explore in to_explore_list:
				new_sequence = sequence + [to_explore]
				new_words = self.starts_with(self.sequence_to_word(new_sequence), words)
				results = results + self.solve_helper(new_sequence, new_words)

		word = self.sequence_to_word(sequence)
		if word in words:
			results.append((sequence, word, self.compute_points(sequence)))

		return results

	def get_neighbors(self, position):
		"""Return the list of neighbor positions given a position."""
		neighbors = [[1,4,5], [0, 2, 4, 5, 6], [1, 3, 5, 6, 7], [2, 6, 7],
				[0, 1, 5, 8, 9], [0, 1, 2, 4, 6, 8, 9, 10], [1, 2, 3, 5, 7, 9, 10, 11], [2, 3, 6, 10, 11],
				[4, 5, 9, 12, 13], [4, 5, 6, 8, 10, 12, 13, 14], [5, 6, 7, 9, 11, 13, 14, 15], [6, 7, 10, 14, 15],
				[8, 9, 13], [8, 9, 10, 12, 14], [9, 10, 11, 13, 15], [10, 11, 14]]
		return neighbors[position] 

	def starts_with(self, substr, strings):
		"""Returns a list of words from a larger list of words that contain the substring."""
		result = []
		for string in strings:
			if string.startswith(substr):
				result.append(string)
		return result

	def show_solutions(self):
		"""Return the solutions.
		Solutions is a list of pairs of sequences and corresponding words."""
		if not self.solved:
			print "Board not solved yet!"
			return

		return self.solutions

	def show_solutions_sorted_by_word_length(self):
		"""Returns the list of words sorted by length in descending order.
		No duplicates returned."""
		if not self.solved:
			print "Board not solved yet!"
			return

		results = self.solutions
		results.sort(lambda x,y: cmp(len(x[1]), len(y[1])))
		results.reverse()
		return results

	def show_solutions_sorted_by_points(self):
		"""Returns the list of words sorted by point value in descending order."""
		if not self.solved:
			print "Board not solved yet!"
			return

		results = self.solutions
		results.sort(lambda x,y: cmp(x[2], y[2]))
		results.reverse()
		return results

	def format_solutions(self, solutions, params = [1]):
		"""Returns a list of tuples of partial information from the solutions list."""
		words = []
		for tup in solutions:
			if len(params) == 1:
				words.append(tup[params[0]])
			else:
				values = []
				for p in params:
					values.append(tup[p])	
				words.append(tuple(values))
		return words

	def print_solutions_xml(self):
		"""Prints an xml format of the solutions for website processing."""
		if not self.solved:
			print "Board not solved yet!"
			return

		print 'Content-type: application/xml\n\n'
		print '<?xml version="1.0" encoding="utf-8"?>'
		print '<solutions>'
		for tup in self.solutions:
			print '\t<answer>'
			print '\t\t<sequence>' + str(tup[0]) + '</sequence>'
			print '\t\t<word>' + tup[1] + '</word>'
			print '\t\t<points>' + str(tup[2]) + '</points>'
			print '\t</answer>'
		print '</solutions>'

	def sequence_to_word(self, sequence):
		"""Converts a given sequence of positions into the word."""
		word = ''
		for pos in sequence:
			word += self.board[pos]
		return word

	def compute_points(self, sequence):
		"""Computes the points of a word."""
		DEFAULT = '0'
		DOUBLE_LETTER = '1'
		DOUBLE_WORD = '2'
		TRIPLE_LETTER = '3'
		TRIPLE_WORD = '4'

		points = 0
		double_words = 0
		triple_words = 0
		for pos in sequence:
			multiply_factor = 1
			if self.special[pos] == DOUBLE_LETTER:
				multiply_factor = 2
			elif self.special[pos] == TRIPLE_LETTER:
				multiply_factor = 3
			elif self.special[pos] == DOUBLE_WORD:
				double_words += 1
			elif self.special[pos] == TRIPLE_WORD:
				triple_words += 1

			points += multiply_factor * self.points[self.board[pos]]

		for i in range(0, double_words):
			points = 2*points
		for i in range(0, triple_words):
			points = 3*points
		
		return points
