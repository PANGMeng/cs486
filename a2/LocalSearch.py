#CS486 Assignment #2, Q2: TSP using Simulated Annealing
#Justin Franchetto
#20375706

#Purpose: Using Simulated Annealing, solve TSP for a given instance
import sys, string, math, datetime, itertools
from TSPObjects import *
from random import *

#GenerateRandomTour: Generate an initial random solution
#for this problem instance.
def GenerateRandomTour(cities):
	remainingCities = cities
	start = remainingCities.pop(0)
	tour = Tour()
	tour.AddCity(start)

	for i in range(0, len(remainingCities)):
		nextCity = randint(0, len(remainingCities)-1)
		tour.AddCity(remainingCities.pop(nextCity))

	tour.AddCity(start)
	return tour

#Accept: Accept a given move if it creates a better path with 100% probability, 
#otherwise accept it with a probability according to Boltzmann distribution
def Accept(currentTour, newTour, temperature):
	delta = newTour.cost-currentTour.cost
	if (delta <= 0):
		return True
	else:
		probability = math.exp(-delta/temperature)
		return probability > uniform(0, 1)
	
	return False

#Generate the cooling schedule, using the Fitzpatrick method
def CoolingSchedule(startingTemperature, coolingRate):
	schedule = []
	t = startingTemperature
	while t > 1:
		schedule.append(t)
		t = t*coolingRate
	return schedule

#GenerateRandomSwapMoves: Generates all size k combinations of random indicies
def GenerateRandomSwapMoves(tourLength, k):
	#This is for k vericies such that we can find their neighbour (2-opt)
	indicies = list(range(1, tourLength-1))
	return [list(x) for x in itertools.combinations(indicies,k)]

#Execute Simulated Annealing on a set of cities, using the given starting temperature and cooling rate. 
def SimulatedAnnealing(cities, initialTemperature, coolingRate, k):
	numberCities = len(cities)

	#Generate an initial tour, randomly
	currentTour = GenerateRandomTour(cities)
	bestTour = Tour(currentTour)
	print("Initial: " + '\n' + str(currentTour))

	if numberCities <= 2:
		return bestTour

	#Create a cooling schedule
	coolingSchedule = CoolingSchedule(initialTemperature, coolingRate)
	temperature = initialTemperature

	#Generate all possible index swaps
	randomSwaps = GenerateRandomSwapMoves(len(currentTour.path), k)

	iterations = 0
	for temperature in coolingSchedule:
		newTour = Tour(currentTour)

		#Random 2-swap
		move = randomSwaps[randint(0, len(randomSwaps)-1)]	
		newTour.SwapCities(move)

		#Should we accept this move?
		if(Accept(currentTour, newTour, temperature)):
			currentTour = Tour(newTour)
		
		#Update best tour if needed
		if (currentTour < bestTour):
			bestTour = Tour(currentTour)

		iterations += 1
		if (iterations % 50000 == 0):
			print(currentTour.cost)

	return bestTour

def SetupAnnealing(cities):
	initialTemperature = 15000
	coolingRate = 0.999985
	tour = SimulatedAnnealing(cities, initialTemperature, coolingRate, 2)
	return tour

def main():
	if len(sys.argv) == 2:							
		filename = sys.argv[1]
		#Compile a list of cities based on input data
		cities = ConstructCities(filename)
		starttime = datetime.datetime.now()
		tour = SetupAnnealing(cities)
		endtime = datetime.datetime.now()
		elapsedtime = (endtime - starttime).total_seconds()
		print('\n' + "Final: " + '\n' + str(tour))
		print("Time: " + "{0:.4f}".format(elapsedtime) + " seconds")

main()