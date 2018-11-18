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


def train_model(trg,dd,fl):

	# Initiate weights for classifieri
	ind = 0

	while (ind < fl ):
		print("Training %d of %d binary classifier." %(ind+1, fl))
		pit = 1000 # length of weigth vector
		w = np.random.rand(pit,1) # generates random numbers [0,1]
		# add truncating one to w
		w = np.append(w, 1)

		err_o = open('./errors/error'+str(ind)+'.dat', 'w')
		err_o.write('iteration\terror\tcum_error\n')

		q = 1
		cum_e=0    
		# Train model
		for dt in trg:
			dt_path = dd + dt
			o = open(dt_path, 'r')
			#print(dt)
			for line in o:
				if line.startswith('#RDKFINGERPRINT:'):
					line=line.strip()
					line=line.split()
					fprint = line[1]
					if (int(fprint[ind])==1):
						luokka = 1
					else:
						luokka = 0
			o.close()

			mz = np.loadtxt(dt_path, comments='#', usecols=[0])
			mz= np.rint(mz) # rounds the mz to integers.
			ri = np.loadtxt(dt_path, comments='#', usecols=[2])
			data = np.column_stack((mz, ri))
			mzf= np.arange(0,pit,1)# create m/z vector of same lenght as w-1 
			f=np.zeros(pit)
			f= np.column_stack((mzf, f))
			for i in data:
				for a in f:
					if i[0]==a[0]:
						a[1]=a[1]+i[1]


			x = f[:,0]*f[:,1]
			# x = mz * ri # feature vector
			# add truncating zero to feature vector
			y = np.pad(x, (0, 1), 'constant')
			# Calculate dot product y * w
			yw = np.dot(y, w)

			# Generate c > C=(W*Y)/(Y*Y)

			C = np.dot(w,y)/np.dot(y,y)
			c = C + 0.01

			# test which side of hyperplane y * w<0 for cat 1 or y * w>0 for cat 0, compare to correct classification
			# Correct weights w if classification is incorrect
			# w' = w + c*y if y should have been cat 1
			# w' = w - c*y if y should have been cat 0
			w0 = w
			if (yw > 0 and luokka != 0 ):
				w = w - c*y
			elif (yw < 0 and luokka != 1):
				w = w + c*y

			# Calculate change in vector: e = w' - w
			e = w - w0
			# Claculate |e|
			enorm = np.linalg.norm(e, 2)
			cum_e = cum_e + enorm
			#print(enorm)
			err_o.write('%d\t%.4f\t%.4f\n' % (q,enorm, cum_e))
			q = q + 1

		err_o.close()
		np.savetxt('./weights/weights'+str(ind)+'.dat', w)
		ind = ind+1

def tanimoto(a,b):
	i = 0
	times = 0
	norm_a = 0
	norm_b = 0
	while(i < len(a)):
		times = times + int(a[i])*int(b[i])
		norm_a = norm_a + int(a[i])**2
		norm_b = norm_b + int(b[i])**2
		i = i+1	
	
	if (norm_a == 0) and (norm_b == 0):
		tanimoto = 1
	else:
		tanimoto = times / (norm_a + norm_b - times)
	
	return tanimoto
		
def test_model(test, dd, fl):
	pit = 1000
	fi = 0
	os.system('rm -r ./pred_fps')
	os.system('mkdir pred_fps')
	
	o2 = open('./pred_fps/tanimoto.dat', 'w')
	
	for dt in test:
		ofp = './pred_fps/fp'+str(fi)+'.dat'
		fp_pred = [] # predicted fingerprint
		dt_path = dd + dt
		o = open(dt_path, 'r')
		#print(dt)
		for line in o:
			if line.startswith('#RDKFINGERPRINT:'):
				line=line.strip()
				line=line.split()
				fprint = line[1]
		o.close()
		# create feature vector

		mz = np.loadtxt(dt_path, comments='#', usecols=[0])
		mz= np.rint(mz) # rounds the mz to integers.
		ri = np.loadtxt(dt_path, comments='#', usecols=[2])
		data = np.column_stack((mz, ri))
		mzf= np.arange(0,pit,1)# create m/z vector of same lenght as w-1 
		f=np.zeros(pit)
		f= np.column_stack((mzf, f))
		for i in data:
			for a in f:
				if i[0]==a[0]:
					a[1]=a[1]+i[1]


		x = f[:,0]*f[:,1]
		# x = mz * ri # feature vector
		# add truncating zero to feature vector
		y = np.pad(x, (0, 1), 'constant')

		i = 0

		while(i<fl):
			# load weight vector from file
			weights = './weights/weights'+str(i)+'.dat'
			w = np.loadtxt(weights)			

			yw = np.dot(y, w)
			if (yw > 0):
				fp_pred.append(0)
			else:
				fp_pred.append(1)			

			i = i+1
		tanimoto_coeff = tanimoto(fp_pred, fprint)
		print('Similarity of predicted fingerprints for %s is %.4f' %(dt, float(tanimoto_coeff)))
		o2.write('%.4f\n' % (float(tanimoto_coeff)))
		# print results to file
		o = open(ofp, 'w')
		ii = 0
		o.write('#Correct fp: ')
		while (ii<len(fp_pred)):
			o.write('%d' % (int(fprint[ii])))
			ii = ii+1	
		o.write('\n')
		ii = 0
		o.write('#Predicted fp: ')
		while (ii<len(fp_pred)):
			o.write('%d' % (int(fp_pred[ii])))
			ii = ii+1	
		o.write('\n')
		o.write('Tanimoto coefficient: %.4f\n' % (float(tanimoto_coeff)))
		o.close()
		fi = fi + 1
	o2.close()



def main ():
	wd = os.getcwd()
	# initiate random number generator
	random.seed(42)

	os.system('rm -r ./weights')
	os.system('rm -r ./errors')

	os.system('mkdir weights')
	os.system('mkdir errors')
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

	fl = 3 # length of finger print
	train_model(trg, dd, fl)
	test_model(test, dd, fl)


main()


















#	corr = 0

#	for da in test: 
#		dt_path = dd + da
#		o = open(dt_path, 'r')
#		for line in o:
#			if line.startswith('#SMILES'):
#				line=line.strip()
#				line=line.split()
#				if 'C(=O)' or 'O=CC' or 'C1=0' or 'O=C1' in line[1]:
#					luokka = 1
#				else:
#					luokka = 0
#		o.close()
#	
#		mz = np.loadtxt(dt_path, comments='#', usecols=[0])
#		mz= np.rint(mz) # rounds the mz to integers.
#		ri = np.loadtxt(dt_path, comments='#', usecols=[2])
#		data = np.column_stack((mz, ri))
#		mzf= np.arange(0,pit,1)# create m/z vector of same lenght as w-1 
#		f=np.zeros(pit)
#		f= np.column_stack((mzf, f))
#		for i in data:
#			for a in f:
#				if i[0]==a[0]:
#					a[1]=a[1]+i[1]
	
	
#		x = f[:,0]*f[:,1]
		# x = mz * ri # feature vector
		# add truncating zero to feature vector
#		y = np.pad(x, (0, 1), 'constant')
		# Calculate dot product y * w
#		yw = np.dot(y, w)
	
		# test which side of hyperplane y * w<0 for cat 1 or y * w>0 for cat 0, compare to correct classification
		# Correct weights w if classification is incorrect
		# w' = w + c*y if y should have been cat 1
		# w' = w - c*y if y should have been cat 0
#		if (yw > 0 and luokka == 0 ):
#			corr = corr + 1
#		elif (yw < 0 and luokka == 1):
#			corr = corr + 1

#	print('Classified %d (%.2f percent) out of %d samples correctly' % (corr, float(corr/len(test)*100),len(test)))









