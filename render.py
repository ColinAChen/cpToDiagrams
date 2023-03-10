import cv2
from util import *
import math
import numpy as np
# squares per row
ROW = 8
LINE_WIDTH = 2
SQUARE_LENGTH = 100
BUFFER = 20
SQUARE_SIZE = (SQUARE_LENGTH, SQUARE_LENGTH, 3)
WHITE = (255,255,255)
BLACK = (0,0,0)
#OpenCV uses BGR
BLUE = (255,0,0)
RED = (0,0,255)
# determine how many squares we need
# create a canvas that can fit all the squares based on ROW

def createFirst():
	pass
def renderNext(lineSet, square, nextLine):
	#print('render', nextLine)
	#print(square.shape)
	# first turn all pixels black
	colorMin = np.minimum(square[:,:,0], square[:,:,2])
	square[:,:,0] = colorMin
	square[:,:,1] = colorMin
	square[:,:,2] = colorMin
	# draw the next line on the square with the correct colors
	for line in nextLine:
		#print(line)
		p1, p2, lineType = line
		x1,y1 = p1
		x2,y2 = p2
		# new point locations are translate then scale
		nx1, ny1, nx2, ny2 = rescalePoints((x1, y1, x2, y2), lineSet.getCorners())
		lineColor = getColor(lineType)
		# draw the line
		cv2.line(square, (nx1, ny1), (nx2, ny2), lineColor, LINE_WIDTH)
	#showImage(square)
	return square
# def renderNext(prevLineSet, nextLine):
# 	canvas = np.zeros(SQUARE_SIZE)
# 	canvas[:,:] = WHITE
# 	# fill in all previous lines as contours
# 	for line in prevLineSet:
# 		p1, p2, lineType = line
# 		x1,y1 = p1
# 		x2,y2 = p2
# 		# new point locations are translate then scale
# 		nx1, ny1, nx2, ny2 = rescalePoints((x1, y1, x2, y2), prevLineSet.getCorners())

# 		# draw the line
# 		cv2.line(canvas, (nx1, ny1), (nx2, ny2), BLACK, LINE_WIDTH)
# 	# draw the new line
# 	p1, p2, lineType = nextLine
# 	x1,y1 = p1
# 	x2,y2 = p2
# 	nx1, ny1, nx2, ny2 = rescalePoints((x1, y1, x2, y2), prevLineSet.getCorners())
# 	lineColor = getColor(lineType)
# 	cv2.line(canvas, (nx1, ny1), (nx2, ny2), lineColor, LINE_WIDTH)
# 	return canvas


'''
Use this to draw the final crease pattern
'''
def drawLineSet(square, lineSet):
	#print(lineSet)
	for line in lineSet:
		#print('line:',line)
		p1, p2, lineType = line
		x1,y1 = p1
		x2,y2 = p2
		# new point locations are translate then scale
		nx1, ny1, nx2, ny2 = rescalePoints((x1, y1, x2, y2), lineSet.getCorners())
		lineColor = getColor(lineType)
		# draw the line
		cv2.line(square, (nx1, ny1), (nx2, ny2), lineColor, LINE_WIDTH)
	#showImage(square)
	return square

def getColor(lineType):
	if lineType == CONTOUR:
		return BLACK
	if lineType == VALLEY:
		return BLUE
	if lineType == MOUNTAIN:
		return RED

def rescalePoints(points, corners):
	#print(corners)
	# in the future allow points to be any length
	# get square size to determine the scale
	topLeft, bottomRight = corners
	
	# these will be the same in a square, not sure why I'm trying to future proof against this
	x1, y1 = topLeft
	x2, y2 = bottomRight
	length = x2 - x1
	height = y2 - y1
	lScale = SQUARE_LENGTH/length
	hScale = SQUARE_LENGTH/height
	# need to translate before
	tx = 0
	if x1 != 0:
		# translate x
		tx = -x1
	ty = 0
	if y1 != 0:
		# translate y
		ty = -y1
	x1, y1, x2, y2 = points
	nx1 = x1 + tx
	ny1 = y1 + ty
	nx2 = x2 + tx
	ny2 = y2 + ty

	nx1 *= lScale
	nx2 *= lScale

	ny1 *= hScale
	ny2 *= hScale

	nx1 = int(nx1)
	nx2 = int(nx2)
	ny1 = int(ny1)
	ny2 = int(ny2)
	return nx1, ny1, nx2, ny2

'''
render a square by drawing lines
the new canvas is the previous square but all black

'''
def render(lineSet, lineOrder, savePath):
	# start with a square
	squares = len(lineOrder) + 2 #+2 accounts for blank square and the final square
	print(squares)
	cols = math.ceil(squares/ROW)
	print(cols)
	length = (SQUARE_LENGTH * ROW) + (BUFFER * (ROW+1))
	height = (SQUARE_LENGTH * cols) + (BUFFER * (cols+1))
	canvasSize = (height, length,3)
	canvas = np.zeros(canvasSize)
	print(canvas.shape)
	canvas[:,:] = WHITE
	row = 0
	col = 0
	rowOff = BUFFER
	colOff = BUFFER

	square = np.zeros((SQUARE_LENGTH, SQUARE_LENGTH, 3))
	square[:,:] = WHITE
	
	# draw the first square
	cv2.line(square, (0,0), (0,SQUARE_LENGTH), BLACK, LINE_WIDTH)
	cv2.line(square, (0,0), (SQUARE_LENGTH,0), BLACK, LINE_WIDTH)
	cv2.line(square, (0,SQUARE_LENGTH), (SQUARE_LENGTH,SQUARE_LENGTH), BLACK, LINE_WIDTH)
	cv2.line(square, (SQUARE_LENGTH,0), (SQUARE_LENGTH,SQUARE_LENGTH), BLACK, LINE_WIDTH)
	
	# determine where to draw the next square
	row = 0
	col = 0
	rowOff = BUFFER
	colOff = BUFFER
	canvas[colOff: colOff+SQUARE_LENGTH, rowOff:rowOff+SQUARE_LENGTH] = square
	row+=1
	if row >= ROW:
		row = 0
		col+=1
	rowOff = BUFFER + ((SQUARE_LENGTH + BUFFER) * row)
	colOff = BUFFER + ((SQUARE_LENGTH + BUFFER) * col)
	for step in lineOrder:
		square = renderNext(lineSet,square, step)
		#showImage('square', square)
		canvas[colOff: colOff+SQUARE_LENGTH, rowOff:rowOff+SQUARE_LENGTH] = square
		row+=1
		if row >= ROW:
			row = 0
			col+=1
		rowOff = BUFFER + ((SQUARE_LENGTH + BUFFER) * row)
		colOff = BUFFER + ((SQUARE_LENGTH + BUFFER) * col)
	finalSquare = np.zeros((SQUARE_LENGTH, SQUARE_LENGTH,3))
	finalSquare[:,:] = WHITE
	canvas[colOff: colOff+SQUARE_LENGTH, rowOff:rowOff+SQUARE_LENGTH] = drawLineSet(finalSquare, lineSet)
	showImage(canvas, 'diagrams')
	cv2.imwrite(savePath, canvas)
'''

buffer square buffer square ...


buffer
square
buffer

'''
# def render(lineSetOrder, nextLineOrder, savePath='diagrams.png'):
# 	# determine the canvas size
# 	squares = len(lineSetOrder)
# 	print(squares)
# 	cols = math.ceil(squares/ROW)
# 	print(cols)
# 	length = (SQUARE_LENGTH * ROW) + (BUFFER * (ROW+1))
# 	height = (SQUARE_LENGTH * cols) + (BUFFER * (cols+1))
# 	canvasSize = (height, length,3)
# 	canvas = np.zeros(canvasSize)
# 	#print(canvas.shape)
# 	canvas[:,:] = WHITE
# 	row = 0
# 	col = 0
# 	rowOff = BUFFER
# 	colOff = BUFFER
# 	for lineSet, nextLine in zip(lineSetOrder[:-1], nextLineOrder):
# 		print(row, col)
# 		drawSquare = renderNext(lineSet, nextLine)
# 		#showImage(drawSquare, 'square')
# 		canvas[colOff: colOff+SQUARE_LENGTH, rowOff:rowOff+SQUARE_LENGTH] = drawSquare
# 		row+=1
# 		if row >= ROW:
# 			row = 0
# 			col+=1
# 		rowOff = BUFFER + ((SQUARE_LENGTH + BUFFER) * row)
# 		colOff = BUFFER + ((SQUARE_LENGTH + BUFFER) * col)
# 	showImage(canvas, 'diagrams')
# 	cv2.imwrite(savePath, canvas)

def showImage(image,title='image'):
	cv2.imshow(title, image)
	cv2.waitKey(0)
	cv2.destroyAllWindows()