#CS486 Assignment #2, Q1: TSP using A* Search
#Justin Franchetto
#20375706

#Purpose: Using A* Search with an admissible heuristic, solve TSP for a set of city data.

#f(n) = Cost from current city to closest univisted city
#	  + Cost to visit all unvisited cities (MST)
# 	  + Cost of closest unvisited city from the start city, to the start city 
#Heuristic: We will use the minimum spanning tree (MST) with the lowest cost.
#Cost: Cost of the path between two cities is the euclidean distance.

import sys, string, math, queue, datetime, heapq
from TSPObjects import *

#Helpers
#Calculates the total cost of the path
def CalculatePathCost(path):
	pathcost = 0
	for i in range(1, len(path)):
		pathcost = pathcost + EuclideanCost(path[i], path[i-1])

	return pathcost

#Minimum Spanning Tree
##################################################
#MinimumCostRoad: Given the visited cities, all roads and the current MST,
#find the lowest cost road that has one end in a visited city and one end in an univisted city
def MinimumCostRoad(visitedCities, roads, mst):
	for road in roads:
		if road not in mst:
			if (road.source not in visitedCities) and (road.dest in visitedCities):
				mst.append(road)
				visitedCities.append(road.source)
				return road.cost
			elif (road.dest not in visitedCities) and (road.source in visitedCities):
				mst.append(road)
				visitedCities.append(road.dest)
				return road.cost
	return 0

#PrimMST: Construct the MST of unvisited cities using Prim's algorithm,
#returning the cost to traverse that tree
def PrimMST(cities):
	if len(cities) <= 1:
		return 0

	roads = ConstructRoads(cities)
	firstRoad = roads.pop(0)
	mst = [firstRoad]

	visitedCities = [firstRoad.source, firstRoad.dest]
	mstCost = firstRoad.cost

	while len(visitedCities) < len(cities):
		mstCost = mstCost + MinimumCostRoad(visitedCities, roads, mst)

	return mstCost

#A* Search 
########################################################
#FindUnvisitedCities: Given a path and a list of cities, return a list
#of all cities not in the path
def FindUnvisitedCities(path, cities):
	unvisitedCities = []

	#If our path is not finished (a cycle), add the first city in the path
	#because we need to go back there
	if (len(path) > 1 and path[0] != path[-1]):
		unvisitedCities.append(path[0])

	for city in cities:
		if not city in path:
			unvisitedCities.append(city)

	return unvisitedCities

#FindSuccessors: Find the successors of a given city.
#We notice that the MST cost and Pathcost are the same for every succcessor of <node>.
#We can compute these only once and perform the f(n) calculation in this function
#f(n) contains the cost of the path so far, as well as the heurisitic (cost of MST) + cost to child
def FindSuccessors(node, cities):
	successors = []

	#We return an empty list if the path contains a cycle (we are done)
	if len(node.path) > 1 and (node.path[0] == node.path[-1]):
		return successors

	#Precompute static costs
	#Compute the cost of the current path
	pathcost = CalculatePathCost(node.path)

	#Compute the cost of the mst of all unvisited cities
	unvisitedCities = FindUnvisitedCities(node.path, cities)
	mstcost = PrimMST(unvisitedCities)
	########################################################

	#Skip all cities in the path, add the ones that are not as successors
	for city in cities:
		if city not in node.path:
			nPath = list(node.path)
			nPath.append(city)
			f = pathcost + mstcost + EuclideanCost(node.path[-1], city)
			successors.append(CostTuple(f, nPath))

	#If we found no successors, this means we have all cities in the path
	#in this case, we add the starting node so our path can go back home
	if not successors:
		nPath = list(node.path)
		nPath.append(node.path[0])
		f = pathcost + mstcost + EuclideanCost(node.path[-1], node.path[0])
		successors.append(CostTuple(f, nPath))

	return sorted(successors)

#Perform A* Search
def Search(cities):
	totalCities = len(cities)
	nodesGenerated = 0

	#If there is only one city, we generate 0 nodes
	if len(cities) == 1:
		return (nodesGenerated, [cities[0]])
	#We start with the first city, A, on our queue (priority queue on the cost)
	#A is first because cities are sorted by letter when they are made
	fringe = queue.PriorityQueue()
	startingNode = CostTuple(0, [cities[0]])
	fringe.put(startingNode)

	while fringe:
		node = fringe.get()
		#Get the first city off the queue, and check if it satisfies the goal state:
		#There are all the cities in the path, plus an extra copy of the first city
		#For the cycle to be complete, the first and last nodes must be the same.
		if (len(node.path) == (totalCities+1)) and (node.path[0] == node.path[-1]):
			return (nodesGenerated, node.path)

		#Get the successors of this city, add their count to our node count
		#then, add them all to the fringe
		successors = FindSuccessors(node, cities)
		nodesGenerated = nodesGenerated + len(successors)

		#Is there a way to optimize this?
		for successor in successors:
			fringe.put(successor)

	return (nodesGenerated, node.path)

########################################################
def PrintPath(path):
	pathstring = ""
	for i in range(0, len(path)):
		if i == 0:
			pathstring = pathstring + path[i].id
		else:
			pathstring = pathstring + "," + path[i].id

	return "Path: {}".format(pathstring)

def main():
	if len(sys.argv) == 2:							
		filename = sys.argv[1]
		#Compile a list of cities based on input data
		cities = ConstructCities(filename)

		#Start the timer and begin our A* Search
		starttime = datetime.datetime.now()
		results = Search(cities)
		endtime = datetime.datetime.now()

		#Print out useful information about our search
		pathcost = CalculatePathCost(results[1])
		
		print("Nodes: " + str(results[0]))
		print(PrintPath(results[1]))
		print("Cost: " + str(pathcost))
		elapsedtime = (endtime - starttime).total_seconds()
		print("Time: " + "{0:.4}".format(elapsedtime) + " seconds")
	else:
		print("Incorrect parameters. Usage: A2Q1 <filepath>")
		quit()

main()
