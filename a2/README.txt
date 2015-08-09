CS 486 - Assignment 2
Justin Franchetto
20375706

README:

NOTE: This must be done on a machine with Python 3 installed. Trying to run on a machine with Python 2 will cause issues
The written answers are included in the PDF submitted to the dropbox.

1) In order to run the programs for A2, extract the zip and ensure that the following files are in the same folder as the randTSP folder.
The directory should look like this:

	randTSP [folder]
	InformedSearch.py
	LocalSearch.py
	TSPObjects.py

2) Open a command prompt and navigate to the location of the files, then simply run one of the following commands:

	For the A* Informed Search, run:
		"python InformedSearch.py randTSP/<cities>/<instance>"
	For the Simulated Annealing Local Search, run:
		"python LocalSearch.py randTSP/<cities>/<instance>"

	Where <cities> is the number of cities (1-16) you want to run and <instance> is the name of the file
	of a particular instance in those cities (1-10). In the case of the 36 city problem, replace the
	<cities>/<instance> with problem36. 

