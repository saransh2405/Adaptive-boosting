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


def calCs(values,index,partition,probability):
	cp=0
	cn=0
	wp=0
	wn=0
	cps = []
	cns = []
	wps = []
	wns = []
	if partition == 1:
				for i in range(0,index+1):
					if int(values[i]) == -1:
						wn+=float(probability[i])
						wns.append(i)
						
					elif int(values[i]) == 1:
						cp+=float(probability[i])
						cps.append(i)
					else:
						pass

				for i in range(index+1,len(values)):
					if int(values[i]) == -1:
						cn+=float(probability[i])
						cns.append(i)
					elif int(values[i]) == 1:
						wp+=float(probability[i])
						wps.append(i)
					else:
						pass
	elif partition == -1:
				for i in range(0,index+1):
					if int(values[i]) == -1:
						cn+=float(probability[i])
						cns.append(i)
					elif int(values[i]) == 1:
						wp+=float(probability[i])
						wps.append(i)
					else:
						pass

				for i in range(index+1,len(values)):
					if int(values[i]) == -1:
						wn+=float(probability[i])
						wns.append(i)
					elif int(values[i]) == 1:
						cp+=float(probability[i])
						cps.append(i)
					else:
						pass

	return cp,cn,wp,wn,cps,cns,wps,wns


def calGs(cp,cn,wp,wn,epsilon):
	g = math.pow(cp*wn,0.5)+math.pow(wp*cn,0.5)
	ctp = 0.5*math.log((cp+epsilon)/(wn+epsilon))
	ctn = 0.5*math.log((wp+epsilon)/(cn+epsilon))
	return g,ctp,ctn


def newProb(g,ctp,ctn,cps,cns,wps,wns,probability):
	prob = []
	for i in range(0,len(probability)):
		prob.append(float(probability[i]))
	for each in cps:
		prob[each] = float(probability[each])*math.exp(-1*ctp)

	for each in cns:
		prob[each] = float(probability[each])*math.exp(1*ctn)

	for each in wps:
		prob[each] = float(probability[each])*math.exp(-1*ctn)

	for each in wns:
		prob[each] = float(probability[each])*math.exp(1*ctp)

	p=0
	for each in range(len(prob)):
		p+=prob[each]

	for each in range(len(prob)):
		prob[each]=prob[each]/p
	return prob,p


def calFt(ft,index,partition,ctn,ctp):
	
	if partition == 1:
		for each in range(len(ft)):
			if each <= index:
				ft[each] += ctp
			else:
				ft[each] += ctn

	if partition == -1:
		for each in range(len(ft)):
			if each <= index:
				ft[each] += ctn
			else:
				ft[each] += ctp

	return ft

def calerrs(ft,values):
	indx = 0
	errs = 0
	for each in ft:
		if each<0 and int(values[indx])==1:
			errs += 1
		elif each>=0 and int(values[indx])==-1:
			errs += 1
		else:
			pass
		indx+=1

	return float(errs)/len(values)

def main():
	f1 = open("initfile.txt",'r')
	print "-----REAL ADA BOOSTING----"
	f2 = open("realada.txt",'w')
	iterations,size,epsilon,intervals,values,probability = getData(f1.read()) 


	ft = []

	et = 1
	for i in range(len(values)):
		ft.append(0)
	for i in range(0,iterations):
		cl = []
		f2.write("Iteration "+str(i+1)+"\n")
		err,index,partition = calculateSplit(values,probability)
		
		if partition == 1:
			print "Selected weak classifier: x<"+str(((float(intervals[index])+float(intervals[index+1]))/2))
			f2.write("Selected weak classifier: x<"+str(((float(intervals[index])+float(intervals[index+1]))/2)))
		else:
			print "Selected weak classifier: x>"+str(((float(intervals[index])+float(intervals[index+1]))/2))
			f2.write("Selected weak classifier: x>"+str(((float(intervals[index])+float(intervals[index+1]))/2)))

		cp,cn,wp,wn,cps,cns,wps,wns = calCs(values,index,partition,probability)

		g,ctp,ctn= calGs(cp,cn,wp,wn,epsilon)

		f2.write("\nG error: "+str(g)+"\n")
		print "\nG error: "+str(g)+"\n"
		if partition == 1:
			print "Ctp: "+str(ctp)+"\n"
			print "Ctn: "+str(ctn)+"\n"
			f2.write("Ctp: "+str(ctp)+"\n")
			f2.write("Ctn: "+str(ctn)+"\n")
		else:
			print "Ctp: "+str(ctn)+"\n"
			print "Ctn: "+str(ctp)+"\n"
			f2.write("Ctp: "+str(ctn)+"\n")
			f2.write("Ctn: "+str(ctp)+"\n")


		probability,p = newProb(g,ctp,ctn,cps,cns,wps,wns,probability)

		f2.write("Z: "+str(p)+"\n")
		print "Z: "+str(p)+"\n"
		f2.write("Probability: ")
		print "Probability: "
		for each in probability:
			f2.write(str(each)+" ")
			print str(each)+" "
		f2.write("\n")

		et *= p
		ft = calFt(ft,index,partition,ctn,ctp)

		f2.write("ft(xt): ")
		print "ft(xt): "
		for each in ft:
			print str(each)+" "
			f2.write(str(each)+" ")
		f2.write("\n")

		errs = calerrs(ft,values)
		f2.write("Error of the boosted classifier:"+str(errs)+"\n")
		print "Error of the boosted classifier:"+str(errs)+"\n"
		

		f2.write("Bound: "+str(et)+"\n")
		print "Bound: "+str(et)+"\n"
		f2.write("===============================================================================================\n")
		print "===============================================================================================\n"






