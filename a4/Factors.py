from decimal import *

class Label:
	def __init__(self, string):
		data = string.split("~")
		self.letter = data[-1].upper()
		self.isNegated = True if len(data) == 2 else False

	def Negated(self):
		n = Label(str(self))
		n.isNegated = not n.isNegated
		return n

	def __eq__(self, other):
		return self.letter == other.letter and self.isNegated == other.isNegated

	def __lt__(self, other):
		if self.letter == other.letter:
			return self.isNegated > other.isNegated
		else:
			return self.letter < other.letter

	def __str__(self):
		if self.isNegated:
			return "~{}".format(self.letter)
		else:
			return "{}".format(self.letter)

	def __repr__(self):
		return str(self)

	def __hash__(self):
		return hash(str(self.letter))

class Parameters:
	def __init__(self, strings, l=None, other=None):
		if other:
			self.labels = list(other.labels)
			self.count = other.count
		elif l:
			self.labels = list(l)
			self.count = len(l)
		else:
			self.labels = []
			for string in strings:
				l = Label(string)
				self.labels.append(l)
			self.count = len(self.labels)

	def __eq__(self, other):
		return self.labels == other.labels

	def __contains__(self, label):
		return label in self.labels

	def __repr__(self):
		return str(self.labels)

	def __iter__(self):
		return iter(self.labels)

	def __hash__(self):
		return hash(tuple(self.labels))

	def Remove(self, label):
		self.labels.remove(label)

	def ReturnLabels(self):
		return [x for x in self.labels]

	def ReturnLetters(self):
		return [x.letter for x in self.labels]

	def IsEmpty(self):
		return not self.labels

class Factor:
	def __init__(self, other=None):
		if other:
			self.values = dict(other.values)
		else:
			self.values = {}

	def AddEntry(self, parameters, value):
		self.values[parameters] = value

	def GetEntry(self, key):
		return self.values[key]

	def SetEntry(self, key, value):
		self.values[key] = value

	def ReplaceEntry(self, target, new):
		self.values[new] = self.values.pop(target)

	def __iter__(self):
		return iter(self.values)

	def __eq__(self, other):
		print("B")
		return list(self.values.keys()) == list(other.values.keys())

	def __repr__(self):
		string = ""
		for key in self.values:
			string += "{} -> {}".format(key, self.values[key]) + '\n'
		return string

	def __mul__(self, other):
		sharedLetters = set(list(self.values.keys())[0].ReturnLetters()).intersection(set(list(other.values.keys())[0].ReturnLetters()))
		h = Factor()
		for mlabels in list(self.values.keys()):
			for tlabels in list(other.values.keys()):
				mine = set(mlabels.ReturnLabels())
				theirs = set(tlabels.ReturnLabels())
				common = mine.intersection(theirs)
				difference = mine.difference(theirs)

				if len(sharedLetters) == len(common):
					param = list(mine.union(theirs))
					h.AddEntry(Parameters("", param, None), self.values[mlabels]*other.values[tlabels])
		return h

	def __contains__(self, var):
		for param in list(self.values.keys()):
			if var in param:
				return True
		return False

	def Multiply(self, other):
		return self*other

	def Add(self, other):
		s = Factor()
		for param in list(self.values.keys()):
			s.AddEntry(param, self.GetEntry(param)+other.GetEntry(param))
		return s

	def Restrict(self, label):
		mine = list(self.values.keys())[0].ReturnLetters()
		if label.letter not in mine:
			return self

		n = Factor()
		for parameter in self.values:
			if label in parameter:
				newlabels = Parameters("", None, parameter)
				newlabels.Remove(label)
				n.AddEntry(newlabels, self.values[parameter])
		return n

	def Sumout(self, label):
		h = Factor()
		negatedLabel = label.Negated()
		for parameter in self.values.keys():
			remainder = None
			if label in parameter:
				remainder = Parameters("", None, parameter)
				remainder.Remove(label)
			elif negatedLabel in parameter:
				remainder = Parameters("", None, parameter)
				remainder.Remove(negatedLabel)

			if remainder in list(h.values.keys()):
				h.values[remainder] += self.values[parameter]
			else:
				h.values[remainder] = self.values[parameter]
		return h

	def Normalize(self):
		h = Factor(self)
		tablesum = 0
		for param in h.values.keys():
			tablesum += h.values[param]

		normalizer = 1/tablesum
		for param in h.values.keys():
			h.values[param] = normalizer*h.values[param]

		return h

	def IsEmpty(self):
		for param in list(self.values.keys()):
			if not param.IsEmpty():
				return False
		return True

def FactorsWithVariable(factorlist, var):
	l = []
	for factor in factorlist:
		if var in factor:
			l.append(Factor(factor))
	return l

def RemoveFactorsWithVariable(factorlist, var):
	l = []
	for factor in factorlist:
		if var not in factor:
			l.append(Factor(factor))
	return l

def CleanUpFactors(factorlist):
	result = factorlist[0]
	for f in factorlist[1:]:
		result = result.Multiply(f)
	return result

def PrintFactorList(factorlist):
	string = ""
	for x in range(0, len(factorlist)):
		if not factorlist[x].IsEmpty():
			if x == len(factorlist)-1:
				string += str(factorlist[x])
			else:
				string += str(factorlist[x]) + '\n'
	return string

def Inference(factors, queryvars, hiddenvars, evidence):
	print("Starting Inference, with:")
	print("Factors: "+ '\n' + PrintFactorList(factors))
	print("Query: " + str(queryvars))
	print("Hidden: " + str(hiddenvars))
	print("Evidence: " + str(evidence) + '\n')
	print("--------------------------------------")

	print("1: Restrict Factors based on Evidence " + str(evidence))
	for x in range(0, len(factors)):
		for label in evidence:
			r = factors[x].Restrict(label)
			factors[x] = r

	print("Factors after restrictions: "+ '\n' + PrintFactorList(factors))
	print("--------------------------------------")
	print("2: Multiply Factors with hidden variables and sum out from the product")
	for hidden in hiddenvars:
		print("Hidden Variable: " + str(hidden))
		containing = FactorsWithVariable(factors, hidden)
		print("Multiplying: " + '\n' + PrintFactorList(containing))
		#Multiply together all factors that have the hidden variable in them
		product = containing[0]
		for f in containing[1:]:
			product = product.Multiply(f)
		print("Product: " + '\n' + str(product))

		print("Sumout: " + str(hidden))
		result = product.Sumout(hidden)
		print("Result: " + '\n' + str(result))

		factors = RemoveFactorsWithVariable(factors, hidden)
		# if not result.IsEmpty():
		factors.append(result)

	print("--------------------------------------")
	print("3: Multiply remaining factors: "+ '\n' + PrintFactorList(factors))
	f = CleanUpFactors(factors)
	print("Result: " + '\n' + str(f))

	print("--------------------------------------")
	print("4: Normalizing result: ")
	n = f.Normalize()
	print(n)

	print("--------------------------------------")
	return n.GetEntry(Parameters("", queryvars, None))

def ConstructFactors(filename):
	data = open(filename)
	factor = Factor()
	for line in data:
		f = line.split()
		parameters = Parameters(f[0:-1])
		factor.SetEntry(parameters, Decimal(f[-1]))
	return factor

def main():
	getcontext().prec = 10
	ndg = ConstructFactors("ndg.pt")
	fm = ConstructFactors("fm.pt")
	fh = ConstructFactors("fh.pt")
	fs = ConstructFactors("fs.pt")
	fb = ConstructFactors("fb.pt")
	na = ConstructFactors("na.pt")
	ab = ConstructFactors("ab.pt")

	factors = [ndg, fm, fh, fs, fb, na]

	query = [Label("FS")]
	hidden = [Label("NDG"), Label("NA"), Label("FB")]
	evidence = [Label("FH"), Label("FM")]
	inf = Inference(factors, query, hidden, evidence)

	print("P ({} | {}) = {} or {}%".format(query, evidence, inf, inf*100))

main()