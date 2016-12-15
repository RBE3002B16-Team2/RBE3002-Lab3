#!/usr/bin/env python

import rospy, tf, numpy, math, roslib, time

from newastar import aStar
from nav_msgs.msg import GridCells, Path, Odometry, OccupancyGrid
from std_msgs.msg import String, Header
from geometry_msgs.msg import Twist, Point, Pose, PoseStamped, PoseWithCovarianceStamped, Point, Quaternion
from kobuki_msgs.msg import BumperEvent
from tf.transformations import euler_from_quaternion, quaternion_from_euler

def checkerFrontier(maps, grid):
	frontiers = []
	width = maps.info.width
	height = maps.info.height
	resolution = maps.info.resolution
	offsetX = maps.info.origin.position.x
	offsetY = maps.info.origin.position.y
	x = 0
	for i in range(0, height): #height should be set to height of grid
		for j in range(0, width): #width should be set to width of grid
			#print k # used for debugging
			if (grid[i*width+j] == -1 and x == 0):
					point=Point()
					point.x=((j-3)*resolution)+offsetX + (.5 * resolution)
					point.y=((i-3)*resolution)+offsetY + (.5 * resolution)
					point.z=0
					
					frontiers.append(point)
					x = 5
			elif(x != 0):
				x -= 1
	return frontiers

def checkClosestFrontier(frontiers, current, grid, wall):
	cX = 0
	cY = 0
	pX = 0
	pY = 0
	closest = 0
	goal = 0
	for i in frontiers:
		cX = i.x
		cY = i.y
		if(closest == 0):
			pX = cX
			py = cY
			closest = (i.x, i.y)
		elif(len(cX) < len(pX) and len(cY) < len(pY)):
			pX = cX
			py = cY
			closest = (i.x, i.y)
	return closest


# Add def for publishing frontiers, and make them go 5 cells out from closest known point
