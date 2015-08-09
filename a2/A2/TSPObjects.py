import sys, string, math
from random import *
from decimal import *

#Compute the Euclidean cost between two cities
def EuclideanCost(source, dest):
	x = (source.x-dest.x)
	y = (source.y-dest.y)
	result = math.sqrt((x*x)+(y*y))
	return float(result)

#ConstructCities: Read data from the specified file and return a list of City objects
def ConstructCities(filename):
	cities = []
	with open(filename, "r") as cityFile:
		for city in cityFile:
			data = city.split()
			if len(data) == 1:
				totalCities = data[0]
			if len(data) == 3:
				cities.append(City(data[0], data[1], data[2]))	
	cityFile.close()	
	return sorted(cities)

#ConstructRoads: Using a list of City, compute the edges and their costs
def ConstructRoads(cities):
	roads = []
	if len(cities) >= 2:
		for i in range(0, len(cities)):
			for j in range(1, len(cities)):
				if (cities[i] != cities[j]):
					roads.append(Road(cities[i], cities[j]))
	return sorted(roads)

#Objects
#City: Contains an id and coordinates, x and y
class City:
	def __init__(self, id, x, y):
		self.id = id
		self.x = int(x)
		self.y = int(y)

	def __repr__(self):
		return '\n' + "City {}: X: {}, Y: {}".format(self.id, self.x, self.y)

	def __eq__(self, other):
		return (self.id == other.id)

	def __lt__(self, other):
		return self.id < other.id

#Road: Contains a source city, a destination city and the euclidean cost between them
class Road:
	def __init__(self, source, dest):
		self.source = source.id
		self.dest = dest.id
		self.cost = EuclideanCost(source, dest)

	def __repr__(self):
		return '\n' + "Road {} <-> {}, Cost: {}".format(self.source, self.dest, self.cost)

	def __eq__(self, other):
		return (self.source == other.source and self.dest == other.dest) or (self.source == other.dest and self.dest == other.source)

	def __lt__(self, other):
		return self.cost < other.cost

#CostTuple: Used for A* Search
#Contains the current cost and the path to get there
class CostTuple:
	def __init__(self, cost, path):
		self.cost = cost
		self.path = path

	def __repr__(self):
		return '\n' + "Node: Cost: {}, Path: {}".format(self.cost, self.path)

	def __lt__(self, other):
		if self.cost == other.cost:
			return len(self.path) > len(other.path)
		else:
			return self.cost < other.cost 

#Tour: Used for annealing
#Contains cities in the tour and operations for swapping on that tour
class Tour:
	def __init__(self, other=None):
		if other:
			self.path = list(other.path)
			self.cost = other.cost
		else:
			self.path = []
			self.cost = float(0)

	def __repr__(self):
		pathstring = ""
		for i in range(0, len(self.path)):
			if i == 0:
				pathstring = pathstring + self.path[i].id
			else:
				pathstring = pathstring + "," + self.path[i].id

		return "Cost: {}, Path: {}".format(self.cost, pathstring)

	def __eq__(self, other):
		return (self.path == other.path) and (self.cost == other.cost)

	def __lt__(self, other):
		return self.cost < other.cost

	def __le__(self, other):
		return self.cost <= other.cost

	#Add a city to our path
	def AddCity(self, city):
		self.path.append(city)
		self.cost = self.cost + EuclideanCost(self.path[len(self.path)-1], self.path[len(self.path)-2])

	#Swap two cities along the path
	def SwapCities(self, combo):
		first = combo[0]
		second = combo[1]
		self.path[first], self.path[second] = self.path[second], self.path[first]
		self.UpdateCost(first, second)

	#Update the cost of our path
	#Note: We don't need to loop over here every time. We could instead calculate the difference
	#for relevant edges, but Python seems to have some trouble with Floating Point subtraction 
	#after only a few iterations.
	def UpdateCost(self, first, second):
		cost = 0
		for i in range(len(self.path)-1):
			cost += EuclideanCost(self.path[i], self.path[i+1])
		self.cost = cost

