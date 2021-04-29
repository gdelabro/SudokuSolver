import sys
import os
import re

class Sudoku():
	def __init__(self, puzzle: str):
		puzzleList = []
		puzzleList[:0] = puzzle
		self.unsolved = puzzleList
		self.puzzle = puzzleList
		self.integrity = self.check_integrity()
		if self.integrity == 0:
			print("integrity check did not pass")
			return

	def check_integrity(self):
		puzzle = "".join(self.puzzle)
		result = re.match("^[0-9]{81}$", puzzle)
		if result == None:
			return 0
		if self.check_all() == 0:
			return 0
		return 1

	def display(self):
		puzzle = "".join(self.puzzle)
		to_display = ""
		for i in range(len(puzzle) // 3):
			to_display += puzzle[i*3:i*3 + 3] + " "
			if (i + 1) % 3 == 0:
				to_display += "\n"
			if (i + 1) % 9 == 0 and (i + 1) != 3 * 9:
				to_display += "\n"
		print(to_display, end="")
	
	def check_column(self, col_num):
		if not 0 <= col_num < 9:
			return 0
		numbers = [0 for i in range(9)]
		for i in range(9):
			piece = int(self.puzzle[col_num + i*9])
			if piece != 0:
				numbers[piece-1] += 1
		for i in numbers:
			if i > 1:
				return 0
		return 1

	def check_line(self, line_num):
		if not 0 <= line_num < 9:
			return 0
		numbers = [0 for i in range(9)]
		for i in range(9):
			piece = int(self.puzzle[9*line_num + i])
			if piece != 0:
				numbers[piece-1] += 1
		for i in numbers:
			if i > 1:
				return 0
		return 1

	def check_block(self, block_num):
		if not 0 <= block_num < 9:
			return 0
		numbers = [0 for i in range(9)]
		for i in range(9):
			col = (block_num % 3) * 3
			line = (block_num // 3) * 3
			col += (i % 3)
			line += (i // 3)
			index = line * 9 + col
			piece = int(self.puzzle[index])
			if piece != 0:
				numbers[piece-1] += 1
		for i in numbers:
			if i > 1:
				return 0
		return 1
	
	def check_all(self):
		for i in range(9):
			if self.check_line(i) != 1\
				or self.check_column(i) != 1\
				or self.check_block(i) != 1:
				return 0
		return 1
	
	def solve(self):
		cursor = 0
		pieces_index = []
		for i in range(len(self.puzzle)):
			if self.puzzle[i] == '0':
				pieces_index.append(i)
		while 0 <= cursor < len(pieces_index):
			i = pieces_index[cursor]
			while True:
				nb = int(self.puzzle[i]) + 1
				if nb == 10:
					self.puzzle[i] = '0'
					cursor -= 1
					break
				self.puzzle[i] = str(nb)
				if self.check_all() == 1:
					cursor += 1
					break
		if cursor == -1:
			print("unsolvable")


def main():
	if len(sys.argv) != 2:
		print("usage: python3 SudokuSolver.py file")
		sys.exit(0)
	try:
		with open(sys.argv[1], "r") as f:
			content = f.read()
	except:
		print("couldn't open ", sys.argv[1])
		sys.exit(0)
	puzzle = ""
	for line in content.split():
		puzzle += line

	sudoku = Sudoku(puzzle)
	if sudoku.integrity == 0:
		sys.exit(0)
	sudoku.solve()
	sudoku.display()

if __name__ == "__main__":
	main()