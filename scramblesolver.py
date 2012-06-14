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

	def set_board(self, board):
		self.board = board
		self.solutions = []
		self.solved = False

	def solve(self):
		self.solutions = [] 
		for pos in range(0, 15):
			self.solutions.append(self.solve_helper([pos], self.board[pos], self.dictionary))
		self.solved = True

	def solve_helper(self, sequence, word, words):
		found = []
		current = sequence[-1]
		neighbors = self.get_neighbors(current)
		for neighbor in neighbors:
			new_word = word + self.board[neighbor]
			new_words = self.starts_with(new_word, words)
			if len(words) > 0:
				found = self.solve_helper(sequence.append(neighbor), new_word, new_words)	
		if word in self.dictionary:
			return found.append(word)
		else:
			return found

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
			word = ''
			for pos in seq:
				word += self.board[pos]
			words.append(word)
		return words
