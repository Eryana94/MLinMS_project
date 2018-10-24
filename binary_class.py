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

fnames = os.listdir(dd)
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
w = 
# add truncating one to w
w = np.append(w, 1)

# Train model
for dt in trg:
	dt_path = dd + dt
	mz = np.loadtxt(dt_path, comments='#', usecols=[0])
	ri = np.loadtxt(dt_path, comments='#', usecols=[2])
	x = mz * ri # feature vector
	# add truncating zero to feature vector
	y = np.pad(x, (0, 1), 'constant')
	# Calculate dot product y * w
	yw = numpy.dot=(y, w)

	# Generate c > (W*Y)/(Y*Y)
	
	# test which side of hyperplane y * w<0 for cat 1 or y * w>0 for cat 2, compare to correct classification
	# Correct weights w if classification is incorrect
	# w' = w + c*y if y should have been cat 1
	# w' = w - c*y if y should have been cat 2
	if (yw >0):
		
	else:

	# Calculate change in vector: e = w' - w
	# Claculate |e|

	

