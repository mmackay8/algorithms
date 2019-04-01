#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

import math
import time
from MatrixSquare import MatrixSquare

# Used to compute the bandwidth for banded version
MAXINDELS = 3

# Used to implement Needleman-Wunsch scoring
MATCH = -3
INDEL = 5
SUB = 1

#used to get the correct values from the tuple created for each square of the matrix
value = 0
prevSquare = 1
previousText = 2

class GeneSequencing:

	def __init__( self ):
		pass

	def alignOne(self, sequence1, sequence2):
		#This funciton takes in two sequences and creates the unrestricted algorithm returning the last square of the matrix
		matrixCompare = []
		firstRow = []
		firstRow.append((0, None, None))
		for i in range(1, len(sequence1) + 1):
			firstRow.append((i * INDEL, firstRow[i-1], "left"))
		matrixCompare.append(firstRow)

		for i in range(1, len(sequence2) + 1):
			row = []
			for j in range(0, len(sequence1)+1):
				if j == 0:
					aboveSquare = matrixCompare[i-1][j]
					above = matrixCompare[i-1][j][value] + INDEL
					row.append((above, aboveSquare, "above"))
				else:
					minOpt = float("inf")
					MinSquare = None
					if i > len(sequence2) or j > len(sequence1):
						break
					else:
						diagnolSquare = matrixCompare[i - 1][j - 1]

						if sequence2[i - 1] == sequence1[j - 1]:
							diagnol = MATCH + matrixCompare[i - 1][j - 1][value]
							if diagnol < minOpt:
								minOpt = diagnol
								MinSquare = (diagnol, diagnolSquare, "diagnol")
						else:
							diagnol = SUB + matrixCompare[i - 1][j - 1][value]
							if diagnol < minOpt:
								minOpt = diagnol
								MinSquare = (diagnol, diagnolSquare, "diagnol")

					leftSquare = row[j - 1]
					aboveSquare = matrixCompare[i - 1][j]

					above = matrixCompare[i - 1][j][value] + INDEL
					left = row[j - 1][value] + INDEL


					if above < minOpt:
						minOpt = above
						MinSquare = (above, aboveSquare, "above")

					if left < minOpt:
						minOpt = left
						MinSquare = (left, leftSquare, "left")

					row.append(MinSquare)

			matrixCompare.append(row)
		return matrixCompare[-1][-1]

	def getSequences(self, lastSquare, sequence1, sequence2):
		#This funciton takes in the two sequences and the last square of the matrix
		#It uses the backtrace to be able to get the new alignment sequences for both of the given sequences

		seq1 = ""
		seq2 = ""
		indexSeq1 = len(sequence1)
		indexSeq2 = len(sequence2)
		prev = lastSquare
		prevText = lastSquare[previousText]

		while prev != None:
			if prevText == "diagnol":
				indexSeq1 -= 1
				indexSeq2 -= 1
				seq1 = sequence1[indexSeq1] + seq1
				seq2 = sequence2[indexSeq2] + seq2

				prev = prev[prevSquare]
				prevText = prev[previousText]

			elif prevText == "left":
				indexSeq1 -= 1
				seq1 = sequence1[indexSeq1] + seq1
				seq2 = "-" + seq2
				prev = prev[prevSquare]
				prevText = prev[previousText]
			elif prevText == "above":
				indexSeq2 -= 1
				seq2 = sequence2[indexSeq2] + seq2
				seq1 = "-" + seq1
				prev = prev[prevSquare]
				prevText = prev[previousText]
			elif prevText == None:
				break

		return seq1, seq2

	def alignBanded(self, seq1, seq2):
		# This function does the banded alignment of 2 sequences
		if len(seq1) > len(seq2):
			diff = len(seq1) - len(seq2)
		else:
			diff = len(seq2) - len(seq1)

		if diff > MAXINDELS:
			return "No Alignment Possible", float('inf')
		matrixCompare = []
		firstRow = []
		for i in range(MAXINDELS):
			firstRow.append((None, None, None))
		firstRow.append((0, None, None))

		for i in range(MAXINDELS):
			firstRow.append((firstRow[-1][value] + INDEL, firstRow[-1], "left"))
		matrixCompare.append(firstRow)

		for i in range(1, len(seq1) + 1):
			row = []
			for j in range(2 * MAXINDELS + 1):
				minVal = 10000000
				minSquare = (None, None, None)

				diag = matrixCompare[i - 1][j][value]
				if diag != None:
					if j - MAXINDELS + i - 1 < len(seq2):
						diagSquare = matrixCompare[i - 1][j]
						if seq1[i - 1] == seq2[j - MAXINDELS + i - 1]:
							diag = matrixCompare[i - 1][j][value] + MATCH
						else:
							diag = matrixCompare[i - 1][j][value] + SUB
						if diag < minVal:
							minVal = diag
							minSquare = (diag, diagSquare, "diagnol")
				if j + 1 < MAXINDELS * 2 + 1:
					aboveSquare = matrixCompare[i - 1][j + 1]
					above = matrixCompare[i - 1][j + 1][value]
					if above != None:
						above += INDEL
						if above < minVal:
							minVal = above
							minSquare = (above, aboveSquare, "above")
				if len(row) > 0:
					leftSquare = row[j - 1]
					left = row[j - 1][value]
					if left != None:
						left += INDEL
						if left < minVal:
							minVal = left
							minSquare = (left, leftSquare, "left")

				row.append(minSquare)
			matrixCompare.append(row)
		return matrixCompare, matrixCompare[-1][MAXINDELS+diff]



	def align( self, sequences, table, banded, align_length):
		self.banded = banded
		self.MaxCharactersToAlign = align_length
		results = []

		for i in range(len(sequences)):
			jresults = []
			for j in range(len(sequences)):

				if(j < i):
					s = {}
				else:
					if(len(sequences[i])) > self.MaxCharactersToAlign:
						sequences[i] = sequences[i][:self.MaxCharactersToAlign]
					if(len(sequences[j]))> self.MaxCharactersToAlign:
						sequences[j] = sequences[j][:self.MaxCharactersToAlign]
					if self.banded:
						if len(sequences[i]) >= len(sequences[j]):
							matrix, square = self.alignBanded(sequences[i], sequences[j])
							if matrix == "No Alignment Possible":
								score = square
								alignment2 = matrix
								alignment1 = matrix
							else:
								score = square[value]
								alignment2, alignment1 = self.getSequences(square, sequences[j], sequences[i])
						else:
							matrix, square = self.alignBanded(sequences[i], sequences[j])
							if matrix == "No Alignment Possible":
								score = square
								alignment1 = matrix
								alignment2 = matrix
							else:
								score = square[value]
								alignment2, alignment1 = self.getSequences(square, sequences[j], sequences[i])
					else:
						if len(sequences[i]) <= len(sequences[j]):
							square = self.alignOne(sequences[i], sequences[j])
							score = square[value]
							alignment1, alignment2 = self.getSequences(square, sequences[i], sequences[j])
						else:
							square = self.alignOne(sequences[j], sequences[i])
							score = square[value]
							alignment2, alignment1 = self.getSequences(square, sequences[j], sequences[i])
					s = {'align_cost':score, 'seqi_first100':alignment1[:100], 'seqj_first100':alignment2[:100]}
					table.item(i,j).setText('{}'.format(int(score) if score != math.inf else score))
					table.repaint()	
				jresults.append(s)
			results.append(jresults)
		return results





