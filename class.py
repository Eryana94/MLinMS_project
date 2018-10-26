#!/usr/bin/env python3


#
#
#
# Basic binary classifier 

import numpy as np
import math
import os
import random
from glob import glob

wd = os.getcwd()
# initiate random number generator
random.seed(42)


# split data into training set and test set

print("Splitting data into training and test data sets.")

frac = 0.8 # Fraction of training data set of whole data
i = 0
trg = []
test = []

dd = wd + '/stripped_data/'

fnames = glob('./stripped_data/data*.txt')
random.shuffle(fnames)

cut = math.trunc(frac * len(fnames))

for a in fnames:
	if (i < cut):
		trg.append(a)
	else:
		test.append(a)
	i = i+1 

print("Size of training data set is %d" % (len(trg)))
print("Size of test data set is %d" % (len(test)))

# Initiate weights for classifier
w = np.random.rand(1000,1) # generates random numbers [0,1]
# add truncating one to w
w = np.append(w, 1)

    
# Train model
for dt in trg:
	o = open(dt, 'r')
	for line in o:
		if line.startswith('#SMILES'):
			line=line.strip()
			line=line.split()
			if 'C(=O)' in line[1]:
				class_r = 1
			else:
				class_r = 0
	o.close()
	
	mz = np.loadtxt(dt, comments='#', usecols=[0])
	mz= np.rint(mz) # rounds the mz to integers.
	ri = np.loadtxt(dt, comments='#', usecols=[2])
	data = np.column_stack((mz, ri))
	mzf= np.arange(0,1000,1)# create m/z vector of same lenght as w-1 
	f=np.zeros(1000)
	f= np.column_stack((mzf, f))
	for i in data:
		ii = 0
		while(ii < len(f)):
			if i[0]==f[ii,0]:
				f[ii,1]=f[ii,1]+i[1]
			ii = ii + 1
		
	x = f[:,0]*f[:,1]
	# x = mz * ri # feature vector
	# add truncating zero to feature vector
	y = np.append(x, 0)
	# Calculate dot product y * w
	yw = np.dot(y, w)

	# Generate c > C=(W*Y)/(Y*Y)

	C = np.dot(w,y) / np.dot(y,y)
	c = C + 0.0001
	
	# test which side of hyperplane y * w<0 for cat 1 or y * w>0 for cat 0, compare to correct classification
	# Correct weights w if classification is incorrect
	# w' = w + c*y if y should have been cat 1
	# w' = w - c*y if y should have been cat 0
	w0 = w
	if (yw > 0 and class_r != 0 ):
		w = w - c*y
	elif (yw < 0 and class_r != 1):
		w = w + c*y
	
	# Calculate change in vector: e = w' - w
	e = w - w0
	# Claculate |e|
	enorm = np.linalg.norm(e, 2)
	print(enorm)

print(w)
	

