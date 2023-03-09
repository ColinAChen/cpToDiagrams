import math
'''
Need to figure out when to round
'''
#https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line
def pointLineDistance (point, line):
	x0,y0 = point
	p1, p2, lt = line
	x1,y1 = p1
	x2,y2 = p2
	numerator = abs(((x2-x1) * (y1-y0)) - ((x1-x0) * (y2-y1)))
	denominator = math.sqrt(( (x2-x1) * (x2-x1) ) + ( (y2-y1) * (y2-y1) ))
	return round(numerator / denominator , 5)
def distance(point1, point2):
	retSum = 0
	for p1, p2 in zip(point1, point2):
		retSum += (p1 - p2) * (p1 - p2)
	return math.sqrt(retSum)

	
'''
Check if point is on line
'''
def pointOnLine(point, line):
	#print('check ',point, ' on line ,',line)
	start, end, lt = line
	if point == start or point == end:
		# might need to change to a threshold
		return True
	startX, startY = start
	endX, endY = end
	pointX, pointY = point
	# delta y / delta x
	dy = endY - startY
	dx = endX - startX
	if dy < 0 and dx < 0:
		dy = -dy
		dx = -dx
	
	#vert = False
	if endX - startX == 0 and endX - pointX == 0:
		return True
	elif endX - startX == 0 or endX - pointX == 0:
		return False
		#vert=True
	slope = (endY - startY) / (endX - startX)
	# this point is on the line if the slope formed from the point to a point on the line is the same
	cdy = endY - pointY
	cdx = endX - pointX
	if cdy < 0 and cdx < 0:
		cdy = -cdy
		cdx = -cdx
	# if vert and endX - pointX == 0:
	# 	return True
	# elif vert:
	# 	return False
	# elif endX - pointX == 0:
	# 	return False
	checkSlope = (endY - pointY) / (endX - pointX)

	# might need to adjust to account for rounding
	# abs(checkSlope - slope) < SLOPE_THRESHOLD
	return checkSlope == slope
	#return dy == cdy and dx == cdx

'''
# check if two lines are colinear
'''
def colinear(line1, line2):
	p1, p2,lt = line1
	return pointOnLine(p1, line2) and pointOnLine(p2, line2)

def lineIntersection(line1, line2):
	# https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
	p1,p2,lt = line1
	x1,y1 = p1
	x2,y2 = p2

	p3,p4,lt = line2
	x3,y3 = p3
	x4,y4 = p4

	denominator = ((x1 - x2) * (y3 - y4)) - ((y1-y2) * (x3-x4))
	if denominator == 0:
		return None
	numx = (((x1 * y2) - (y1 * x2)) * (x3 - x4)) - ((x1 - x2) * ((x3 * y4) - (y3 * x4)))
	numy = (((x1 * y2) - (y1 * x2)) * (y3 - y4)) - ((y1 - y2) * ((x3 * y4) - (y3 * x4)))
	# print('numx: ', numx)
	# print('numy: ', numy, (((x1 * y2) - (y1 * x2)) * (y3 - y4)) - ((y1 - y2)), ((y1 - y2) - ((x3 * y4) - (y3 * x4))) )
	# print('denominator: ', denominator)
	return (round(numx/denominator, 10), round(numy/denominator,10))