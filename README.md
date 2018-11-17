# MLinMS_project
Machine learning in materials science group project

stripsearch.py:
  Script for filtering through the database entries and writing truncated .txt files. Please download the database from github (see   link on massbank.eu front page), unzip in wanted location, and run this script as executable in 'Mass-Bank-data-master' directory. e.g. './stripsearch.py MS2 POSITIVE'. Script requires python3.x and numpy to run.

PLEASE USE 'stripsearch_v2.py'!!!!!

binary_classifier_v2.py: Binary classifier. Currently works for carbonyl oxygen classification. please run in 'Mass-Bank-data-master' directory after 'stripsearch_v2.py' as './binary_classifier_v2.py'. Prints error and final values of w to files. 


####### For fingerprinting (RDK default fingerprint)

RDKit can be installed via conda (see https://www.rdkit.org/docs/Install.html)

Creating a special environment in Triton (see http://scicomp.aalto.fi/triton/apps/python.html)

Putting these together one needs to run these on Triton (bolded headlines are just explanations)

# Move your package cache to your work directory.  The following does it automatically.
rsync -lrt ~/.conda/ $WRKDIR/conda/ && rm -r ~/.conda

ln -sT $WRKDIR/conda ~/.conda

quotafix -gs --fix $WRKDIR/conda

# create environment with RDKit package in it
module load teflon

conda create -c rdkit -n my-rdkit-env rdkit

module unload teflon

# activate your RDkit environment (your shell is after this in this environment)
source activate my-rdkit-env

# to exit from environment use (if you need to go back just reactivate ie use the above command)
source deactivate my-rdkit-env

# To run stripsearch_v3.py
python3 ./stripsearch_v3.py MS2 POSITIVE

# Some files causing errors
Just discard them :D

I found:

CO000210.txt  CO000300.txt  CO000350.txt  CO000420.txt  CO000500.txt  CO000510.txt in folder Univ_Connecticut

and

ET201104.txt in Eawag_Additional_Specs


# Added stuff in v3 vs. v2

# Modules
from rdkit import Chem

from rdkit import DataStructs

from rdkit.DataStructs.cDataStructs import BitVectToText

from rdkit.Chem.Fingerprints import FingerprintMols

from rdkit.Chem.Fingerprints.FingerprintMols import FingerprintsFromMols

from rdkit.Chem.Fingerprints.FingerprintMols import GetRDKFingerprint

# "Code"
o.write('#RDKFINGERPRINT: %s\n' % (BitVectToText(FingerprintMols.GetRDKFingerprint(Chem.MolFromSmiles(smiles)))))

just after writing $SMILES

# See these links

https://www.rdkit.org/docs/source/rdkit.Chem.Fingerprints.FingerprintMols.html

https://www.rdkit.org/docs/source/rdkit.Chem.rdFingerprintGenerator.html

I have used the RDK fingerprint with default settings



# stripsearch_v4.py added

Can be run as the previous. Fingerprinting switched to Morgan, with adjustable bit amount (now set to 1024).










