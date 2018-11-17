#!/usr/bin/env python3

#
#
# A very crude Python 3.x script for filtering MassBank.eu data
# By: Maisa Vuorte
# 22.10.2018
# Modified by E.M.
# 16.11.2018

from rdkit import Chem
from rdkit import DataStructs
from rdkit.DataStructs.cDataStructs import BitVectToText
from rdkit.Chem.Fingerprints import FingerprintMols
from rdkit.Chem.Fingerprints.FingerprintMols import FingerprintsFromMols
from rdkit.Chem.Fingerprints.FingerprintMols import GetRDKFingerprint
import os
from glob import glob
import sys
import math
import numpy as np
import time
from rdkit.Chem import AllChem



try:
	# Read command line imput parameters for ms-type and ion-mode
	ms_type = str(sys.argv[1])
	ion_mode = str(sys.argv[2])
	col_eng = 50 # default value for testing purposes
	#col_eng = int(sys.argv[3])


	owd = os.getcwd()
	print("Removing existing directory ./stripped_data, this may take a while.")
	os.system('rm -f -r ./stripped_data')
	os.system('mkdir stripped_data')
	out_path = './stripped_data'


	i = 1
	nf = 0

	for sd in glob('./*/'):
		if (sd != './stripped_data/'):
			files = glob(sd+'*.txt')
			nf = nf + len(files) 
			for f_name in files:
				print("Reading file %s" % (f_name))
				f = open(f_name, 'r')
				lines = f.readlines()
				f.close()
				col = False; ion = False; mst = False; read_peaks = False; peaks = []; intens = [];
				for line in lines:
					line = line.strip()
					line = line.split()
					#print(line)
					if (read_peaks == True):
						if (line[0] == '//'):
							break
						else:
							peaks.append(float(line[0]))
							intens.append(float(line[1]))

					elif (line[0]=='CH$FORMULA:'):
						formula = line[1]
					elif (line[0]=='CH$SMILES:'):
						smiles = line[1]
					elif (line[0]=='CH$EXACT_MASS:'):
						mass = line[1]
					elif (line[0]=='AC$MASS_SPECTROMETRY:'):
						if (line[1]=='MS_TYPE'):
							if (line[2]==str(ms_type)):
								mst = True
						if (line[1]=='ION_MODE'):
							if (line[2]==str(ion_mode)):
								ion = True
						if (line[1]=='COLLISION_ENERGY'):
							if (line[2]==str(col_eng)):
								col = True
					elif (line[0]=='PK$PEAK:'):
						if (ion == True and mst == True and col == True):
							read_peaks = True
				ii=0
				if (read_peaks == True):
					o = open(out_path+'/data'+str(i)+'.txt', 'w')
					o.write('#Formula: %s\n' % (formula))
					o.write('#Mass: %.4f\n' % (float(mass)))
					o.write('#SMILES: %s\n' % (smiles))
					o.write('#RDKFINGERPRINT: %s\n' % (BitVectToText(AllChem.GetMorganFingerprintAsBitVect(Chem.MolFromSmiles(smiles),2,nBits=1024))))
					o.write('#Peaks\tm/z\tintensity\trelative_intens\n')
					s = np.sum(intens)
					for a in peaks:
						o.write('%.4f\t%.4f\t%.4f\n' % (a, intens[ii], intens[ii]/s))
						ii = ii + 1
					o.close()
					i = i+1

	t1 = time.process_time()
	print('\n')
	print('**********************FINISHED**********************')
	print("Filtered a total of %d files.\nWrote %d files in directory %s." % (nf, i-1, out_path))
	print("Filtering took %.4f s cpu time\nAverage cpu time per file: %.8f s" % (t1, (t1)/nf))
				
except(IndexError):
	print("!!!!AN ERROR OCCURRED!!!!")
	print("Detected error in input parameters")
	print("Usage: ./stripsearch.py [MS-TYPE] [ION-MODE]")
	print("Example: ./stripsearch.py MS2 POSITIVE")
	print("Exiting program, please try again!")

except(ZeroDivisionError):
	print("!!!!AN ERROR OCCURRED!!!!")
	print("Could not find any files matching search criteria.")
	print("Please make sure you are running the script in the correct directory MassBank-data-master")
	print("Exiting program, please try again!")
