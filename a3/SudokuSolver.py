#CS486 Assignment #3, SudokuSolver.py
#Justin Franchetto
#20375706

#Purpose: Solve the CSP defined by the starting grid
#and the constraints outlined in Part A of the written question

import sys, string, math
from SudokuObjects import *
#NOTE: In some of the failing puzzles, the possible entries are
#slightly incorrect for some squares

def Solve(board):
	assignments = 0
	moves = []

	while assignments < 10000:
		#If at any point our sudoku puzzle is solved,
		#break and return
		if board.IsComplete():
			print("FIN")
			break

		#Step One: Find the MRV, breaking if we have backed up
		#to the point where there are no possible moves
		entry = board.MostConstrainedEntry()
		if not moves and assignments > 0 and len(entry.possibilities) == 0:
			print("GIVE UP")
			assignments = 10000
			break

		#We backtrack if our MRV is unassigned and has no possible moves
		if len(entry.possibilities) == 0 and entry.value == 0:
			badMove = moves.pop()
			board.Restore(badMove)
			if len(entry.possibilities) == 0:
				board.Reset(badMove)
			continue

		#Step Two: Find the least constraining value for that entry,
		#If it is 0 (unassigned), then we backtrack
		leastConstrainingValue = board.LeastConstrainingValue(entry)
		if not leastConstrainingValue or leastConstrainingValue == 0:
			badMove = moves.pop()
			board.Restore(badMove)
			if len(entry.possibilities) == 0:
				board.Reset(badMove)
			continue

		#Step Three: Make the assignment, put the move on our stack
		#and increment the assignments
		board.Update(entry.j, entry.i, leastConstrainingValue)
		moves.append(entry)
		assignments += 1

	return assignments

def sudoku(filename):
	# if len(sys.argv) == 2:							
	# 	filename = sys.argv[1]
	board = ConstructBoard(filename, 9)
	print("Starting board:")
	print(board)
	assignments = Solve(board)
	print("Final board:")
	print(board)
	print("Assignments made: {}".format(assignments))
	return assignments

# 		quit()
# main()
