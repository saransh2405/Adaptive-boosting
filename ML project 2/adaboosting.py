import math

def getData(data):
	data = data.split("\n")
	iterations = int(data[0].split(" ")[0])
	size = int(data[0].split(" ")[1])
	epsilon = float(data[0].split(" ")[2])
	intervals = data[1].split(" ")
	values = data[2].split(" ")
	probability = data[3].split(" ")
	return iterations,size,epsilon,intervals,values,probability

def calculateSplit(values,probability):
	i = 0
	val = 2
	minimum = 2
	minval = 2
	for each in range(0,len(values)-1):
		errneg = 0
		errpos = 0
		for x in range(i+1):
			if int(values[x])==-1:
				errneg += float(probability[x])
			if int(values[x])==1:
				errpos += float(probability[x])

		
		for x in range(i+1,len(values)):
			if int(values[x])==1:
				errneg += float(probability[x])
			if int(values[x])==-1:
				errpos += float(probability[x])

		
		if errpos < minval or errneg < minval:
			if errpos<errneg:
				minval = errpos
				minimum = i
				val = -1
			elif errpos>=errneg:
				minval = errneg
				minimum = i
				val = 1
		i=i+1
		'''print "negetive error:",errneg
		print "positive error:",errpos'''
	return minval,minimum,val

def calAlpha(err):
	a = 0.5*math.log((1-err)/err)
	q = []
	q.append(math.exp(-a))
	q.append(math.exp(a))
	x = err*(1-err)
	z = 2*math.pow(x,0.5)

	return q,z,a


def newProbs(values,probability,index,partition,q,z):
	newprob = []
	for x in range(0,index+1):
		if int(values[x]) != partition:
			newprob.append(float(probability[x])*q[1]/z)
		else:
			newprob.append(float(probability[x])*q[0]/z)

	for x in range(index+1,len(values)):
		if int(values[x]) != -partition:
			newprob.append(float(probability[x])*q[1]/z)
		else:
			newprob.append(float(probability[x])*q[0]/z)

	return newprob

def errorcalculate(booster,values):
	indx = 0
	cplus = 0
	cneg = 0
	errs = 0
	for val in values:
		cplus = 0
		cneg = 0
		for each in booster:

			if each[2] == 1 and int(each[1])>=indx:
				cplus += each[0]
			elif each[2] == -1 and int(each[1])>=indx:
				cneg += each[0]
			elif each[2] == -1 and int(each[1])<indx:
				cplus += each[0]
			else:
				cneg += each[0]
		indx +=1

		if cplus > cneg:
			if int(val) == -1:
				errs +=1
		else:
			if int(val) == 1:
				errs +=1

	return errs



def main():
	f1 = open("initfile.txt",'r')
	f2 = open("binaryada.txt",'w')
	iterations,size,epsilon,intervals,values,probability = getData(f1.read()) 
	booster = []
	zs = 1

	for i in range(0,iterations):

		err,index,partition = calculateSplit(values,probability)
		cl = []

		f2.write("Iteration "+str(i+1)+"\n")

		if partition == 1:
			f2.write("Selected weak classifier: x<"+str((float(intervals[index])+float(intervals[index+1]))/2)+"\n")
		else:
			f2.write("Selected weak classifier: x>"+str((float(intervals[index])+float(intervals[index+1]))/2)+"\n")


		f2.write("Error:"+str(err)+"\n")
		q,z,a = calAlpha(err)
		f2.write("Weight:"+str(a)+"\n")
		f2.write("Probability normalization factor: "+str(z)+"\n")

		cl.append(a)
		cl.append(index)
		cl.append(partition)
		booster.append(cl)

		probability = newProbs(values,probability,index,partition,q,z)
		f2.write("Probability after normalization: ")
		for each in probability:
			f2.write("  "+str(each))

		f2.write("\nft: ")
		f = ""
		for each in booster:
			if each[2] == 1:
				f += str(each[0])+" I(x<"+str(((float(intervals[each[1]])+float(intervals[each[1]+1]))/2))+")+"
			else:
				f += str(each[0])+" I(x>"+str(((float(intervals[each[1]])+float(intervals[each[1]+1]))/2))+")+"


		f2.write(f.strip("+")+"\n")
		errs = errorcalculate(booster,values)


		zs = zs*z
		f2.write("error of the boosted classifier: "+str(errs)+"\n")
		f2.write("bound on Et: "+str(zs)+"\n")
		f2.write("===============================================================================================\n")





