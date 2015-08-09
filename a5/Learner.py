# Problems to solve:

# 1) Data structures for the tree (recursive) and for the data
# 2) Deciding which attribute to test (entropy function -> information gain)
# 3) Compute the threshold to test on:
#   At each step, find all values that exist for an attribute in remaining instances,
#   Order these values and try threshold values that are halfway between successive attribute values.
#   Use the threshold value that gives the highest information gain. 
# 4) Allow this attribute to be tested later in the tree if needed (with a new threshold)

#Node: A single node in our decision tree, containing the following:
    # Attribute: The attribute being tested at this node,
    # Threshold: The threshold for splitting that attribute
    # Label: True/False label given at the leaves of the tree
    # Left: The left subtree
    # Right: The right subtree

import math, random, sys

class Node:
    def __init__(self, attribute=None, threshold=None, gain=None, label=None, left=None, right=None):
        self.attribute = attribute
        self.threshold = threshold
        self.gain = gain
        self.label = label
        self.left = left
        self.right = right

    def __repr__(self):
        return "Attribute: {}, Threshold: {}, Gain: {}, Label: {}".format(self.attribute, self.threshold, self.gain, self.label)

class Data:
    def __init__(self, data=None):
        if data:
            self.points = list(data)
        else:
            self.points = []

    def __repr__(self):
        string = ""
        for point in self.points:
            string += str(point) + '\n'
        return string

    def Sort(self, attribute):
        self.points.sort(key=lambda point: point[attribute])

    def AddPoint(self, point):
        self.points.append(point)

    def IsEmpty(self):
        return not self.points

    def PositiveExamples(self):
        found = 0
        for point in self.points:
            if point[-1]:
                found += 1
        return found

    def NegativeExamples(self):
        found = 0
        for point in self.points:
            if not point[-1]:
                found += 1
        return found

    def Mode(self):
        if self.PositiveExamples() > self.NegativeExamples():
            return True
        elif self.PositiveExamples() < self.NegativeExamples():
            return False
        else:
            if random.uniform(0, 1) < 0.5:
                return True
            else:
                return False

    def TotalExamples(self):
        return len(self.points)

    def NumberAttributes(self):
        return len(self.points[0])-1

    def SameLabels(self):
        label = self.points[0][-1]
        for point in self.points:
            if point[-1] != label:
                return False
        return True

    def GetLabel(self):
        if self.SameLabels():
            return self.points[0][-1]

    def Entropy(self):
        total = self.TotalExamples()
        if total == 0:
            return 0

        positive = self.PositiveExamples()
        negative = self.NegativeExamples()

        positiveFraction = positive/total
        negativeFraction = negative/total

        if positiveFraction == 0:
            return -((negativeFraction)*math.log(negativeFraction, 2))
        elif negativeFraction == 0:
            return (-positiveFraction*math.log(positiveFraction, 2))
        else:
            return (-positiveFraction*math.log(positiveFraction, 2))-\
                  ((negativeFraction)*math.log(negativeFraction, 2))

    def Split(self, attribute, threshold):
        good = Data()
        bad = Data()
        for point in self.points:
            if point[attribute] < threshold:
                good.AddPoint(point)
            else:
                bad.AddPoint(point)
        return [good, bad]

    def Remainder(self, sets):
        remainder = 0
        for dataset in sets:
            weight = (dataset.PositiveExamples() + dataset.NegativeExamples())/self.TotalExamples()
            entropy = dataset.Entropy()
            remainder += weight*entropy

        return remainder

    def InformationGain(self, attribute, threshold):
        entropy = self.Entropy()
        remainder = self.Remainder(self.Split(attribute, threshold))
        return entropy-remainder

    def FindThresholds(self, attribute):
        thresholds = []
        for i in range(1, self.TotalExamples()):
            if self.points[i][attribute] != self.points[i-1][attribute]:
                t = self.points[i][attribute]+self.points[i-1][attribute]
                thresholds.append(t/2)

        return thresholds

    #This function finds the attribute to split the data on and the 
    #threshold to use when splitting
    def ChooseAttribute(self, attributes):
        best = (-1, -1, -1)
        for attribute in attributes:
            self.Sort(attribute)
            thresholds = self.FindThresholds(attribute)
            for threshold in thresholds:
                gain = self.InformationGain(attribute, threshold)
                if gain > best[2]:
                    best = (attribute, threshold, gain)
        return Node(best[0], best[1], best[2])

def DTL(examples, attributes, default):
    if examples.IsEmpty():
        return Node(None, None, None, default)
    elif examples.SameLabels():
        return Node(None, None, None, examples.GetLabel())
    elif not attributes:
        return Node(None, None, None, examples.Mode())
    else:
        print("Selecting best attribute: ")
        best = examples.ChooseAttribute(attributes)
        print("Attribute: " + AttributeToString(best.attribute, examples.NumberAttributes()))
        print("Threshold: " + str(best.threshold))
        print("Information Gain: " + str(best.gain) + "\n")
        result = examples.Split(best.attribute, best.threshold)
        best.left = DTL(result[0], attributes, examples.Mode())
        best.right = DTL(result[1], attributes, examples.Mode())
        return best

def TestPoint(tree, point):
    if tree.label != None:
        return tree.label
    elif (point[tree.attribute] < tree.threshold):
        return TestPoint(tree.left, point)
    elif (point[tree.attribute] >= tree.threshold):
        return TestPoint(tree.right, point)

def PrintTree(tree, length, isHorse, depth=0):
    treeString = ""
    if tree.right != None:
        treeString += PrintTree(tree.right, length, isHorse, depth + 1)

    if tree.attribute != None:
        treeString += "\n" + ("  "*depth) + "{}, {}".format(tree.attribute, str(tree.threshold))
    else:
        treeString += "\n" + ("  "*depth) + LabelToString(tree.label, isHorse)

    if tree.left != None:
        treeString += PrintTree(tree.left, length, isHorse, depth + 1)

    return treeString

def AttributeToString(attribute, length):
    horseStrings = ["K", "Na", "CL", "HCO3", "Endotoxin", "Aniongap",\
                        "PLA2", "SDH", "GLDH", "TPP", "Breath Rate", "PCV",\
                        "Pulse Rate", "Fibrinogen", "Dimer", "FibPerDim"]

    mathStrings = ["School Attended", "Sex", "Age", "Home", "Family Size",\
                    "Parent's status", "Mother's education", "Father's education",\
                    "Primary caretaker", "Gender of caretaker", "Travel time",\
                    "Study time", "Previous failures", "Extra educational support",\
                    "Family educational support", "Extra paid classes for subject",\
                    "Extra-curricular activities", "Nursery school", "Higher education",\
                    "Internet acccess", "Romantic relationship", "Quality of family relationships",\
                    "Free time after school", "Frequency of seeing friends", "Weekday alcohol consumption",\
                    "Weekend alcohol consumption", "Health status", "Days of class missed"]

    if length == len(horseStrings):
        return horseStrings[attribute]
    else:
        return mathStrings[attribute]

def LabelToString(label, isHorse):
    if isHorse:
        return "Healthy" if label else "Colic"
    else:
        return "Passed" if label else "Failed"

def ConstructHorseData(filename):
    f = open(filename)
    data = Data()
    for line in f:
        s = [float(x) for x in line.split(",")[0:-1]]
        condition = line.split(",")[-1]
        s.append(False if ("colic" in condition) else True)
        data.AddPoint(s)
    return data

def ConstructMathData(filename):
    f = open(filename)
    data = Data()
    lines = []
    for line in f:
        lines.append(line)

    for l in lines[1:]:
        s = [float(x) for x in l.split(",")[0:-1]]
        condition = l.split(",")[-1]
        s.append(True if ("1" in condition) else False)
        data.AddPoint(s)
    return data

def Math(testFlag):
    print("-------------------------------------------------------")
    print("Phase #1: Building decision tree for Math Student Performance classification" + "\n")
    train = ConstructMathData("porto_math_train.csv")

    attributes = list(range(0, train.NumberAttributes()))
    dt = DTL(train, attributes, train.Mode())
    print("Decision Tree:")
    print(PrintTree(dt, len(attributes), False, 0))

    test = None
    if testFlag:
        test = ConstructMathData("porto_math_test.csv")
    else:
        test = ConstructMathData("porto_math_train.csv")

    print("-------------------------------------------------------")
    print("Phase #2: Classification of Math Student Performance" + "\n")
    correct = 0
    for point in test.points:
        #print("Testing point: " + "\n" + str(point[0:-1]))
        r = TestPoint(dt, point)
        #print("Learner labelling: " + LabelToString(r, False))
        if r == point[-1]:
            correct += 1
        #print("Correct labelling: " + LabelToString(point[-1], False) + "\n")

    print("Correct labels: " + str(correct))
    print("Total data points: " + str(test.TotalExamples()))
    print("Accuracy: {}%".format((correct/test.TotalExamples())*100))
    print("-------------------------------------------------------")

def Horses(testFlag):
    print("-------------------------------------------------------")
    print("Phase #1: Building decision tree for Equine Colic classification" + "\n")
    train = ConstructHorseData("horseTrain.txt")
    attributes = list(range(0, train.NumberAttributes()))
    dt = DTL(train, attributes, train.Mode())
    print("Decision Tree:")
    print(PrintTree(dt, len(attributes), True, 0))

    test = None
    if testFlag:
        test = ConstructHorseData("horseTest.txt")
    else:
        test = ConstructHorseData("horseTrain.txt")
    

    print("-------------------------------------------------------")
    print("Phase #2: Classification of Equine Colic disease" + "\n")
    correct = 0
    for point in test.points:
        #print("Testing point: " + "\n" + str(point[0:-1]))
        r = TestPoint(dt, point)
        #print("Learner labelling: " + LabelToString(r, True))
        if r == point[-1]:
            correct += 1
        #print("Correct labelling: " + LabelToString(point[-1], True) + "\n")

    print("Correct labels: " + str(correct))
    print("Total data points: " + str(test.TotalExamples()))
    print("Accuracy: {}%".format((correct/test.TotalExamples())*100))
    print("-------------------------------------------------------")

def main():
    if len(sys.argv) == 3:
        test = False
        if sys.argv[2] == "train":
            test = False
        elif sys.argv[2] == "test":
            test = True
        else:
            print("Invalid run type {}. Use 'train' or 'test'".format(sys.argv[2]))

        if sys.argv[1] == "equine":
            Horses(test)
        elif sys.argv[1] == "math":
            Math(test)
        else:
            print("Invalid data type: {}. Use 'equine' or 'math'".format(sys.argv[1]))
    else:
        print("Invalid arguments. Usage: Learner.py <equine/math> <train/test>")

main()