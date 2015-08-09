import sys, string, math, os
from SudokuSolver import *

result = open('results.txt', 'w')
for folder in range(1, 72):
	total = 0
	giveup = 0
	for puzzle in range (1, 11):
		assignments = sudoku("problems\{}\{}.sd".format(folder, puzzle))
		total += assignments
		if assignments == 10000:
			giveup += 1
	average = total/10
	result.write("{}".format(average) + '\n')
result.close()