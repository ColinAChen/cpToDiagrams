import os
from geomUtil import *
CONTOUR = 1
MOUNTAIN = 2
VALLEY = 3

class Line():
	def __init__(self, point1, point2, lineType):
		self.point1 = point1
		self.point2 = point2
		self.lineType = lineType
	def __eq__(self, checkLine):
		# maybe check if points are close enough?
		if ((self.point1 == checkLine.point1 and self.point2 == checkLine.point2) 
			or (self.point1 == checkLine.point2 and self.point2 == checkLine.point1)):# and self.lineType == checkLine.lineType:
			return True
		return False
	def __repr__(self):
		if self.lineType == CONTOUR:
			lineTypeStr = 'Contour'
		elif self.lineType == MOUNTAIN:
			lineTypeStr = 'Mountain'
		elif self.lineType == VALLEY:
			lineTypeStr = 'Valley'
		return str(self.point1) + ', ' + str(self.point2) + ', type: ' + lineTypeStr
	def __getitem__(self, indices):
		#print(indices)
		# convert a simple index x[y] to a tuple for consistency
		#if not isinstance(indices, tuple):
		#	indices = tuple(indices)
		if indices == 0:
			return self.point1
		elif indices == 1:
			return self.point2
		else:
			return None
	def __iter__(self):
		return iter((self.point1, self.point2, self.lineType))
	def __hash__(self):
		# the hash for both
		hash1 = hash((self.point1, self.point2, self.lineType))
		hash2 = hash((self.point2, self.point1, self.lineType))
		return hash1 + hash2
	def getLineType(self):
		return self.lineType

class LineSet():
	def __init__(self):
		self.lineSet = set()
		self.pointSet = set()
		self.minX = None
		self.minY = None
		self.maxX = None
		self.maxY = None
		self.sortOrder = {}
		# consider grouping colinear lines together? {interection with the edge of the square? endpoints? : colinear lines}
		#self.lineDict = {} # line to lineType lookup
	def __repr__(self):
		out = ''
		#for line in self.lineSet:
		for line in self.sortOrder:
			out += str(line)
			out += '\n'
		return out
	def __contains__(self, check):
		if type(check) ==  type(Line((0,1),(1,0),1)):
			return check in self.lineSet
		elif len(check) == 2:
			# hopeflly this is a point
			return check in self.pointSet
	def __iter__(self):
		# consider sorting by colinearity so we can combine steps at the end
		#return iter(self.lineSet)
		return iter(self.sortOrder)
	def copy(self):
		outSet = LineSet()
		for line in self:
			outSet.add(line)
		return outSet
	def __len__(self):
		return len(self.lineSet)
	def __eq__(self, checkSet):
		for line in self.lineSet:
			if line not in checkSet:
				return 
	def add(self, line):
		# if a line with different type replace it
		#line = Line(point1, point2, lineType)
		#lineType = line.getLineType()
		# check if this line is colinear with any lines
		# this will determine the insertion order

		# addIndex = 0
		# for i,checkColinear in enumerate(self.sortOrder):
		# 	if checkColinear == line:
		# 		continue
		# 	if colinear(checkColinear, line):
		# 		# insert here to be grouped with other colinear lines
		# 		#self.sortOrder.insert(i, line)
		# 		#added=True
		# 		addIndex = i
		foundColinear = False
		for checkLine in self.sortOrder:
			if colinear(checkLine, line):
				foundColinear = True
				self.sortOrder[checkLine].append(line)
				saveKey = self.getEndpoints(checkLine, line)
				if checkLine != saveKey:
					self.sortOrder[saveKey] = self.sortOrder[checkLine]
					del(self.sortOrder[checkLine])
				break
		if not foundColinear:
			# no colinear lines, initialize so that we can find others later
			self.sortOrder[line] = [line]
		#if not added:
		#self.sortOrder.insert(addIndex, line)
		#print(self.sortOrder)
		if line in self.lineSet:
			# replace line type, we shouldn't have duplicate lines
			self.lineSet.remove(line)
		self.lineSet.add(line)
		p1, p2, lt = line
		self.pointSet.add(p1)
		self.pointSet.add(p2)
		# add any intersections to the point set
		# consider breaking up segments here?
		for checkIntersect in self.lineSet:
			if checkIntersect == line:
				continue
			intersect = lineIntersection(checkIntersect, line)
			# if intersect is not None:
			# 	print('intersect: ', intersect, ' in square: ', self.pointInSquare(intersect))
			# if intersect is not None:
			# 	print('intersection of ',checkIntersect, ' and ', line, ' is ', intersect)
			if intersect is not None and intersect not in self.pointSet and self.pointInSquare(intersect):
				self.pointSet.add(intersect)
				#print('add ', intersect)
		x1, y1 = p1
		x2, y2 = p2
		for x in (x1,x2):
			if self.minX is None or x < self.minX:
				self.minX = x
			if self.maxX is None or x > self.maxX:
				self.maxX = x
		for y in (y1, y2):
			if self.minY is None or y < self.minY:
				self.minY = y
			if self.maxY is None or y > self.maxY:
				self.maxY = y
		#if line in lineDict:
		#lineDict[line] = lineType

		# maybe need to replace lines that are colinear since lines must be divided into line segments

		# maybe add all intersections to point set
		

	# def getList(self):
	# 	retList = []
	# 	for line in self.lineSet:
	# 		p1,p2, lineType = line
	# 		#lineType = self.lineDict[line]
	# 		line = (lineType, p1, p2)
	# 		retList.append(line)
	# 	return retList
	def getPointSet(self):
		return self.pointSet
	def getCorners(self):
		return ((self.minX, self.minY), (self.maxX, self.maxY))
	def getSortOrder(self):
		return self.sortOrder
	def getEndpoints(self, line1, line2):
		#print('get endpoints', line1, line2)
		p1,p2,lt = line1
		x1,y1 = p1
		x2,y2 = p2
		p3,p4,lt = line2
		x3,y3 = p3
		x4,y4 = p4
		minX = min(x1,x2,x3,x4)
		maxX = max(x1,x2,x3,x4)
		minY = min(y1,y2,y3,y4)
		maxY = max(y1,y2,y3,y4)

		# there are only two orientations that can produce such a boundary
		if (pointOnLine((minX,minY), line1)):
			return Line((minX, minY), (maxX, maxY), lt)
		return Line((minX, maxY), (maxX, minY), lt)
	def pointInSquare(self,point):
		if point is None:
			return False
		x,y = point
		# print(point, (self.minX, self.minY, self.maxX, self.maxY))
		# print(x >= self.minX, x <=self.maxX, y >=self.minY, y <= self.maxY)
		return x >= self.minX and x <= self.maxX and y >= self.minY and y <= self.maxY
def lineSetToCP(lineSet, pathToCP):
	# (linetype: 1.Contour, 2.Mountain, 3.Valley) (start x) (start y) (end x) (end y)
	with open(pathToCP, 'w+') as writeFile:
		#lineList = lineSet.getList()
		for line in lineSet:
			p1, p2, lineType = line
			x1,y1 = p1
			x2,y2 = p2
			writeLine = str(lineType) + ' ' + str(x1) + ' ' + str(y1) + ' ' + str(x2) + ' ' + str(y2) + '\n'
			writeFile.write(writeLine)
def cpToLineSet(pathToCP):
	lineSet = LineSet()
	with open (pathToCP) as readFile:
		lines = readFile.readlines()
	#print(lines)
	for line in lines:
		split = line.split(' ')
		#print(split)
		lineType = int(split[0])
		p1 = (float(split[1]), float(split[2]))
		p2 = (float(split[3]), float(split[4]))
		#print(lineType)
		#print(p1)
		#print(p2)
		addLine = Line(p1, p2, lineType)
		lineSet.add(addLine)
	return lineSet

'''
Get the square dimensions from a target line set

return a set of

0 . . . max
.
.
.
max

'''
def getSquare(lineSet):
	minX = None
	minY = None
	maxX = None
	maxY = None
	for point in lineSet.getPointSet():
		cx, cy = point
		if minX is None or cx < minX:
			minX = cx
		if minY is None or cy < minY:
			minY = cy
		if maxX is None or cx > maxX:
			maxX = cx
		if maxY is None or cy > maxY:
			maxY = cy
	top = Line((minX, minY),(maxX,minY), CONTOUR)
	bottom = Line((minX, maxY), (maxX, maxY), CONTOUR)
	left = Line((minX, minY), (minX, maxY), CONTOUR)
	right = Line((maxX, minY), (maxX, maxY), CONTOUR)
	retLineSet = LineSet()
	retLineSet.add(top)
	retLineSet.add(bottom)
	retLineSet.add(left)
	retLineSet.add(right)
	return retLineSet
def createSteps(order, pathToSteps):
	for i,lineSet in enumerate(order):
		# maybe check for colinearity here?
		savePath = os.path.join(pathToSteps, (str(i+1) + '.cp'))
		#print(savePath)
		#print(lineSet)
		#print('\n')
		lineSetToCP(lineSet, savePath)