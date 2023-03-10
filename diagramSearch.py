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

'''
3/9/2023 Diagram thought
Find solution that minimizes number of steps

Eventually we will need to store a list of faces and map lines to the face set

One problem is that multiple folds can accomplish the same amount as one in a different collapsed configuraiotn

perhaps we can naturally find the correct collapsed configuration by searching on the heuristic of minum nunber of steps
'''
'''
3/10/2023 Search thought
Specify search depth
This should give the program leeway to add lines that may help us reach new creases
Current problem is that we only continue while we can reach new creases from the immediate step
However, some crease patterns won't specify references
I think we can do the reference finder method where we just search with smart heuristics
'''
import argparse
from util import *
#from geomUtil import *
from render import *

'''
lineSet : target set of lines, we want startSet to eventually match lineSet
startSet : lines we start with, will likely include the square, can include other references

Start with startSet, use known constructions to see what lines we can possible construct (maybe we can use a heuristic function to guide?)
When we find a line that we can reach with the currentSet, add it to the currentSet and search again until we reach lineSet

O(lines ^ 2 maybe lines ^ 3)

TODO: Implememnt the rest of the Huzita Justin Axioms https://langorigami.com/article/huzita-justin-axioms/

# each tuple is a set of colinear lines to be added at once
[(line 1, line 2) , (line 3), (line4 , line 5, line 6), ...]
'''
def bottomUpOrder(lineSet, startSet):
	print("target set")
	print(lineSet)
	# consider storing on the changes, we should be able to piece it together afterwards
	currentSet = startSet#.copy()
	# print('getSquare')
	# print(currentSet.minX)
	# print(currentSet.maxX)
	# print(currentSet.minY)
	# print(currentSet.maxY)
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
		print('i:',i)
		print('current point set:',currentSet.pointSet)
		print('current line set:', currentSet)
		i += 1
		foldsFound = False
		for line in colinearLines:
			p1, p2, lineType = line
			# skip this line if it already exists
			if line in currentSet:
				#i+=1
				continue
			# first check if the line can be reached with existing points
			# this likely needs to be revisitied
			#lineAdded = False
			checkExistingLine = checkExisting(currentSet, line)
			if checkExistingLine is not None:
				print("found connecting existing points")
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
				break
				
			# check if this line can be reached with the current pointset by searching for two perpendicualr bisectors
			pbPoints = checkPerpendicularBisectors(currentSet, line)
			if pbPoints is not None:
				print("found perpendicular bisector")
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
				break
				
			# check if this line can be reached by an existing angle bisector
			# abLines = None
			# if i == 1:
			abLines = checkAngleBisector(currentSet, line)
			if abLines is not None:
				print("found angle bisector")
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
				break
			#render(currentSet, addOrder, 'progress.png')
				
		print('folds found: ',foldsFound)
		#render(currentSet, addOrder, 'progress.png')

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
Check if we can reach line on the current lineSet by searching for two equidistant perpendicular points,
points must exist on an existing perpendicular line

maybe want to return the points we are using to bisect
This is a good idea, I can use them for rendering later

'''

def checkPerpendicularBisectors(lineSet, line):

	'''
	check the distnace and slope to every point in the point set
	if two distances matchw with opposite slope, we can form a perpendicular bisector between these points
	'''
	pointDistance = {} # distance : point,slope
	for point in lineSet.pointSet:
		# get the shortest distance from the point to the line
		# get the point on the line from the perpendicular distance to the line from the point
		cd = pointLineDistance (point, line)
		if cd not in pointDistance:
			pointDistance[cd] = [point]
		else:
			# check if the slope formed by the two points
			# if it is perpendicular to the current line slope, return the two points

			# line slope

			for p in pointDistance[cd]:
				#print('check:',Line(point, p,1), line)
				if perpendicularLines(Line(point, p,1), line):
					print(line,'is a perpendicular bisector of ',point,p, 'distance:',cd)
					print(pointDistance)
					return (point,p)

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

	# create the target set
	targetSet = cpToLineSet(pathToCP)

	# intialize the start set with a square
	startSet = getSquare(targetSet)
	lineSetProgression, lineOrder = bottomUpOrder(targetSet, startSet)
	#render(lineSetProgression, lineOrder,pathToDiagrams)
	if pathToDiagrams == '':
		pathToDiagrams = 'diagrams/' + pathToCP.split('.')[0] + '.png'
	render(targetSet,lineOrder,pathToDiagrams)


if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Choose an input crease pattern')
	parser.add_argument('pathToCp', type=str, help='path to image of crease pattern')
	parser.add_argument('-s','--pathToDiagrams', type=str, default='', help='path to save diagrams to')
	args = parser.parse_args()

	#main(args)

	#createDiagrams('chess_knight.cp')
	#createDiagrams('square_rabbit_ear.cp')
	createDiagrams(args.pathToCp, args.pathToDiagrams)

'''
Current set needs to add entire line and only gets to use intersections as future references


One way is to make the target set the set of lines that intersect with the edges of the square
and just render the parts you need to fold


Target set can just be a set of start and end points, 
'''