# ScrambleSolver solves a Scramble board configuration by 
# listing all the possible solutions.

class ScrambleSolver:
	def __init__(self, dictionary = 'dictionary.txt'):
		f = open(dictionary, 'r')
		self.dictionary = []
		for line in f:
			self.dictionary.append(line.strip())
		f.close()
		self.board = []
		self.solutions = []
		self.solved = False

	def fast_solve(self, board):
		board = board.upper()
		board_list = []
		for char in board:
			if char == 'Q':
				board_list.append('QU')
			elif len(board_list) == 0 or board_list[-1] != 'QU' or char != 'U':
				board_list.append(char)

		self.set_board(board_list)
		self.solve()
		solutions = self.show_solutions()
		words = self.show_words()
		sorted_words = self.show_words_sorted_by_length()

		print "Solutions: "
		print solutions
		print "Words: "
		print words
		print "Sorted Words: "
		print sorted_words

	def set_board(self, board):
		self.board = board
		self.solutions = []
		self.solved = False

	def solve(self):
		self.solutions = [] 
		for pos in range(0, 15):
			words = self.starts_with(self.board[pos], self.dictionary)
			self.solutions = self.solutions + self.solve_helper([pos], words)
		self.solved = True
		print "Done solving!"

	def solve_helper(self, sequence, words):
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
			results.append(sequence)

		return results

	def get_neighbors(self, position):
		neighbors = [[1,4,5], [0, 2, 4, 5, 6], [1, 3, 5, 6, 7], [2, 6, 7],
				[0, 1, 5, 8, 9], [0, 1, 2, 4, 6, 8, 9, 10], [1, 2, 3, 5, 7, 9, 10, 11], [2, 3, 6, 10, 11],
				[4, 5, 9, 12, 13], [4, 5, 6, 8, 10, 12, 13, 14], [5, 6, 7, 9, 11, 13, 14, 15], [6, 7, 10, 14, 15],
				[8, 9, 13], [8, 9, 10, 12, 14], [9, 10, 11, 13, 15], [10, 11, 14]]
		return neighbors[position] 

	def starts_with(self, substr, strings):
		result = []
		for string in strings:
			if string.startswith(substr):
				result.append(string)
		return result

	def show_solutions(self):
		if not self.solved:
			print "Board not solved yet!"
			return

		return self.solutions

	def show_words(self):
		if not self.solved:
			print "Board not solved yet!"
			return

		words = []
		for seq in self.solutions:
			words.append(self.sequence_to_word(seq))
		return words

	def show_words_sorted(self):
		if not self.solved:
			print "Board not solved yet!"
			return

		return list(set(self.show_words()))

	def show_words_sorted_by_length(self):
		if not self.solved:
			print "Board not solved yet!"
			return

		return self.show_words_sorted().sort(lambda x,y: cmp(len(x), len(y)))

	def sequence_to_word(self, sequence):
		word = ''
		for pos in sequence:
			word += self.board[pos]
		return word

