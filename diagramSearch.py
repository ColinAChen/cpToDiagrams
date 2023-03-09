'''
Origami diagram creation experiments
Colin Chen
Started June 2021
'''


# bottom up
# start from a square and possible some reference points
# input: set of lines to reach with known rules
# output: order of lines, maybe with references? this should be able to be rendered afterwards

# top down
# start from a set of lines
# choose lines to remove based on known rules

# two endpoints,

from util import *
#from geomUtil import *
from render import *

'''
lineSet : target set of lines, we want startSet to eventually match lineSet
startSet : lines we start with, will likely include the square, can include other references

Start with startSet, use known constructions to see what lines we can possible construct (maybe we can use a heuristic function to guide?)
When we find a line that we can reach with the currentSet, add it to the currentSet and search again until we reach lineSet

O(lines ^ 2 maybe lines ^ 3)

# each tuple is a set of colinear lines to be added at once
[(line 1, line 2) , (line 3), (line4 , line 5, line 6), ...]
'''
def bottomUpOrder(lineSet, startSet):
	print(lineSet)
	# consider storing on the changes, we should be able to piece it together afterwards
	currentSet = startSet#.copy()
	addOrder = []
	lineOrder = []
	#print('start')
	#print(currentSet)
	foldsFound = True
	#prevOrder = 0
	colinearLines = lineSet.getSortOrder()
	#print(len(colinearLines.keys()))
	# for key in colinearLines.keys():
	# 	print(key)
	#print(colinearLines)
	
		# if we find we can add this line, automatically include all colinear lines
	i = 0
	while foldsFound:
		print(i)
		print(currentSet.pointSet)
		i += 1
		foldsFound = False
		for line in colinearLines:
			#print('candiate line: ', line)
	#while currentSet != lineSet and foldsFound:
		#print(currentSet)
		# check the current set, see what line we can add
		# search again with the new current set until it is the same as the line set
		# keep track of the order
		# ideally add all colinear lines at the same time?

			
		#i = 0
		#sortOrder = lineSet.getSortOrder()
		#print(sortOrder)
		#while i < len(sortOrder):
			#line = sortOrder[i]
			#print(lineOrder)
			#print('candiate line: ', line)
		#for line in lineSet:
			
			
			p1, p2, lineType = line
			
			# skip this line if it already exists
			if line in currentSet:
				#i+=1
				continue
			#print('candiate line: ', line)
			#print(len(currentSet))
			#print(len(addOrder))
			# if len(addOrder) != prevOrder:
			# 	print(currentSet)
			#prevOrder = len(addOrder)

			# first check if the line can be reached with existing points
			# this likely needs to be revisitied
			#lineAdded = False
			checkExistingLine = checkExisting(currentSet, line)
			if checkExistingLine is not None:
				p1, p2 = checkExistingLine
				foldsFound = True
				#print('add existing: ', line, ' between: ', p1, p2)
				step = [line]
				step.extend(colinearLines[line])
				currentSet.add(line)
				#print(currentSet.getPointSet())
				for addLine in step:
					#currentSet.add(addLine)
					addOrder.append(currentSet.copy())
				lineOrder.append(step)
				continue
				# print('checkExisting')
				# step = [line]
				# currentSet.add(line)
				# #lineOrder.append([line])
				# #print(currentSet)
				# addOrder.append(currentSet.copy())
				# #print(len(addOrder))
				# foldsFound = True
				# lineAdded = True
				# i+=1
				# while i < len(sortOrder) and colinear(line, sortOrder[i]):
				# 	print('in loop')
				# 	addOrder.append(currentSet.copy())
				# 	currentSet.add(sortOrder[i])
				# 	step.append(sortOrder[i])

				# 	i+=1
				# lineOrder.append(step)
				# print('add existing: ', step)
				# continue
			
			# check if this line can be reached with the current pointset by searching for two perpendicualr bisectors
			pbPoints = checkPerpendicularBisectors(currentSet, line)
			if pbPoints is not None:
				foldsFound = True
				p1, p2 = pbPoints
				#print('add perpendicular bisector: ', line, ' between ', p1, p2)
				step = [line]
				step.extend(colinearLines[line])
				currentSet.add(line)
				for addLine in step:
					#currentSet.add(addLine)
					addOrder.append(currentSet.copy())
				lineOrder.append(step)
				continue
				# print('check perpendicualr bisectors')
				# step = [line]
				# currentSet.add(line)
				# #step.append(line)
				# #lineOrder.append(line)
				# #print(currentSet)
				# addOrder.append(currentSet.copy())
				# #print(len(addOrder))
				# foldsFound = True
				# lineAdded = True
				# # add all colinear lines now
				# i+=1
				# while i < len(sortOrder) and colinear(line, sortOrder[i]):
				# 	print('in loop')
				# 	addOrder.append(currentSet.copy())
				# 	currentSet.add(sortOrder[i])
				# 	step.append(sortOrder[i])

				# 	i+=1
				# lineOrder.append(step)
				# print('add perpendicularBisectors: ', step)
				# continue

			# check if this line can be reached by an existing angle bisector
			# abLines = None
			# if i == 1:
			abLines = checkAngleBisector(currentSet, line)
			if abLines is not None:
				foldsFound = True
				l1, l2 = abLines
				print('add angle bisector: ', line, 'between ', l1,l2)
				step = [line]
				step.extend(colinearLines[line])
				currentSet.add(line)
				for addLine in step:
					#currentSet.add(addLine)
					addOrder.append(currentSet.copy())
				lineOrder.append(step)
				continue
				# print('check angle bisectors')
				# #print('add angle bisector: ', line)
				# step = [line]
				# currentSet.add(line)
				# #lineOrder.append(line)
				# #step.append(line)
				# #print(currentSet)
				# addOrder.append(currentSet.copy())
				# foldsFound = True
				# lineAdded = True
				# # add all colinear lines now
				# i+=1
				# while i < len(sortOrder) and colinear(line, sortOrder[i]):
				# 	print('in loop')
				# 	addOrder.append(currentSet.copy())
				# 	currentSet.add(sortOrder[i])
				# 	step.append(sortOrder[i])

				# 	i+=1
				# lineOrder.append(step)
				# print('add angle bisector: ', step)
				# continue
			#i+=1
			# if not lineAdded:
			# 	i+=1
			# continue
		print('folds found: ',foldsFound)

	# if currentSet == lineSet:
	# 	print('finished cp')
	# else:
	# 	print('cp incomplete')
	# for key in currentSet.getSortOrder().keys():
	# 	print(key)
	return addOrder, lineOrder

# check shortest distance to this line and all points in point set
# if any match, just perp bisector between the points that match
'''
Check if a line exits in the line set
fold a line between two points
'''
def checkExisting(lineSet, line):
	first = None
	for point in lineSet.getPointSet():
		if pointOnLine(point, line):
			if first:
				return (first,point)
			else:
				first=point
	return None
	# check if any two points in the point set exist on the line
	# p1, p2, lineType = line
	# return p1 in lineSet.getPointSet() and p2 in lineSet.getPointSet()
	#return (p1,p2, lineType) in lineSet #or (p2,p1, lineType) in lineSet


'''
Return the perpendiclar bisector of point1 and point2

fold in half between two points


'''
def perpendicularBisect(point1, point2):
	# rotate 90 by translate to center
	# swap x,y
	# negate y
	# (x,y) -> (y,-x)
	# do this for both points to get the slope of the perpendicualr slope
	# one point on the line is midpoint
	# another point on the line can be found with the slope
	x1,y1 = point1
	x2,y2 = point2
	

	#rotate1 = (y1, -x1)
	#rotate2 = (y2, -x2)
	# delta y / delta x
	# point1 - point2
	dy = x2 - x1
	dx = y1 - y2
	#slope = (-x1 + x2) / (y1-y2)
	midpoint = ((x1 + x2)/2, ((y1 + y2)/2))
	slopePoint = ((x1 + x2)/2 + dx, (y1+y2)/2 + dy)
	return midpoint, slopePoint

'''
check if we can reach line with the current point set by searching for two equidistnace points,
if two pairs of equidistance points, we can just find the midpoints of each pair to get the line

# not sure if this is actually foldable

O(n) on n points in pointset
'''
def checkBisectors(pointSet, line):
	# get distance to each point in pointSet
	# return true if there are 
	pointDistance = {} # distanceToPoint : point
	#p1, p2, tl = line
	#checkLine = (p1, p2)
	# need 4 points, 2 sets of equidstant points
	ret1 = (-1,-1)
	ret2 = (-1,-1)

	ret3 = (-1,-1)
	ret4 = (-1,-1)

	for point in pointSet:
		checkDistance = pointLineDistance(point, line)
		if checkDistance in pointDistance:
			if ret1 == (-1,-1):
				# first pair to be found
				ret1 = pointDistance[checkDistance]
				ret2 = point
				# remove in case the next pair is the same distance
				pointDistance.remove(checkDistance)
			else:
				ret3 = pointDistance[checkDistance]
				ret4 = point
				# we have found enough points to create a bisector
				return True
				#break
		else:
			pointDistance[checkDistance] = point
		pointDistance[pointLineDistance(point, line)] = []
		pointDistance[point] = pointLineDistance(point, line)
	'''
	if ret1 != (-1,-1) and ret3 != (-1,-1):
		# we have found enough points
		x1,y1 = ret1
		x2,y2 = ret2
		midpoint1 = ((x1+x2)/2,(y1+y2)/2)
		x1,y1 = ret3
		x2,y2 = ret4
		midpoint2 = ((x1+x2)/2,(y1+y2)/2)
		return midpoint1, midpoint2
	'''
		

	return False


'''
Check if we can reach line on the current lineSet by searching for two equidistance perpendicular points,
points must exist on an existing perpendicular line

maybe want to return the points we are using to bisect

# don't actually need to be on perpendicual lines, just need to be perpendicular relative to each other and the line
'''
def checkPerpendicularBisectors(lineSet, line):
	p1, p2, lt = line
	x1, y1 = p1
	x2, y2 = p2
	dy = y2-y1
	dx = x2-x1
	slope = None if dx == 0 else dy/dx
	# if dx == 0:
	# 	slope = None
	# else:
	# 	slope = dy/dx
	pointDistance = {} # distance : point
	# perpendicular if dy/dx == -cdx/cdy
	for checkLine in lineSet:
		cp1, cp2, clt = checkLine
		cx1, cy1 = cp1
		cx2, cy2 = cp2
		cdy = cy2 - cy1
		cdx = cx2 - cx1
		checkSlope = None if cdy == 0 else -cdx/cdy
		# only check the distance if the point exists on a line perpendicualr to the candiate line
		if slope == checkSlope:
			checkDistance = pointLineDistance(cp1, line)
			if checkDistance in pointDistance:
				return (pointDistance[checkDistance], cp1) 
			else:
				pointDistance[checkDistance] = line

			checkDistance = pointLineDistance(cp2, line)
			if checkDistance in pointDistance:
				return (pointDistance[checkDistance], cp2)
			else:
				pointDistance[checkDistance] = line
	return None

'''
Look for angle bisectors

# find the intersection point for each line in line set
# save intersections such that {intersection point : lines that intersect with line at this point}
# see if any of these lines are equidistnat


See if the endpoints exist in the point set
check an any lines that start from the point set start/end at that point O(lines)
check if any of those lines are eqidistnat from this line O(lines)

# maybe need to check for lines that don't actually meet
'''
def checkAngleBisector(lineSet, line):
	#print('check angle bisector for ', line)
	p1, p2, lt = line
	checkSet = []
	intersectionLines = {} # point : lines that go through point
	# find lines that start or end at one of the endpoints

	for checkLine in lineSet:
		#print('checkLine', checkLine)
		cp1, cp2, lt = checkLine
		intersection = lineIntersection(checkLine, line)
		#print('intersection', intersection)
		#print(lineSet.pointInSquare(intersection))
		if intersection is None or not lineSet.pointInSquare(intersection):
			# reject intersections outside the square?
			continue
		if intersection not in intersectionLines:
			intersectionLines[intersection] = [checkLine]
		else:
			intersectionLines[intersection].append(checkLine)
	for point in intersectionLines:
		#print(point)
		if len(intersectionLines[point]) < 2:
			#print('not enough intersecting lines')
			continue
		# distance to a point on line : check line
		distanceLine = {}
		for checkLine in intersectionLines[point]:
			### MIGHT NEED TO MORE CAREFUL THAN THIS
			checkDistance = pointLineDistance(p1, checkLine)
			if checkDistance == 0:
				#print('using p2')
				checkDistance = pointLineDistance(p2, checkLine)
			if checkDistance not in distanceLine:
				distanceLine[checkDistance] = checkLine
			else:
				return (checkLine, distanceLine[checkDistance])
		# for distance in distanceLine:
		# 	print('distance: ', distance, 'line: ', distanceLine[distance])
	return None
	# 	#if p1 == cp1 or p1 == cp2:

	# 		if p1 in intersectionLines:
	# 			intersectionLines[p1].append(checkLine)
	# 		else:
	# 			intersectionLines[p1] = [checkLine]
	# 	if p2 == cp1 or p2 == cp2:
	# 		if p2 in intersectionLines:
	# 			intersectionLines[p2].append(checkLine)
	# 		else:
	# 			intersectionLines[p2] = [checkLine]
	# if p1 in intersectionLines:
	# 	distanceP1 = {} # distance : line
	# 	for checkDistanceLine in intersectionLines[p1]:
	# 		checkDistance = pointLineDistance(p2, checkDistanceLine)
	# 		if checkDistance in distanceP1:
	# 			# maybe return the two lines
	# 			return True
	# 		else:
	# 			distanceP1[checkDistance] = checkDistanceLine
	# if p2 in intersectionLines:
	# 	distanceP2 = {}
	# 	for checkDistanceLine in intersectionLines[p2]:
	# 		checkDistance = pointLineDistance(p1, checkDistanceLine)
	# 		if checkDistance in distanceP2:
	# 			# maybe return the two lines
	# 			return True
	# 		else:
	# 			distanceP2[checkDistance] = checkDistanceLine
	return False

def test():

	test1 = (1,2)
	test2 = (3,4)

	line1 = Line(test1, test2,1)
	line2 = Line(test2, test1,2)
	line3 = Line(test2, test1,3)
	line4 = Line(test2, test1, 1)
	t1, t2, lineType = line1
	print(t1)
	print(t2)
	print(line1 == line2)
	print(line1 == line1)
	print(line2 == line3)
	print(line1)
	print(line2)
	print(line3)
	testSet = set()
	testSet.add(line1)
	testSet.add(line2)
	testSet.add(line3)
	testSet.add(line1)
	testSet.add(line4)
	print(testSet)
	print(perpendicularBisect(test1, test2))
	print(cpToLineSet('bird.cp'))

#print(startSet)
#print(startSet.getPointSet())
#print(bottomUpOrder(targetSet, startSet))
# birdOrder, renderOrder = bottomUpOrder(targetSet, startSet)
#print(birdOrder)
# createSteps(birdOrder, 'birdSteps')
# render(birdOrder, renderOrder)

def createDiagrams(pathToCP, pathToDiagrams=''):

	targetSet = cpToLineSet(pathToCP)
	#print('targetSet')
	#print(targetSet)
	print('square')
	print(targetSet.minX, targetSet.maxX,targetSet.minY, targetSet.maxY)
	print('keys')
	print(targetSet.sortOrder.keys())
	startSet = getSquare(targetSet)
	lineSetProgression, lineOrder = bottomUpOrder(targetSet, startSet)
	#render(lineSetProgression, lineOrder,pathToDiagrams)
	if pathToDiagrams == '':
		pathToDiagrams = pathToCP.split('.')[0] + '.png'
	render(targetSet,lineOrder,pathToDiagrams)
createDiagrams('boxpleat_16.cp')