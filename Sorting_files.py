import os, fnmatch
import numpy as np
import re
from shutil import copy



path = "/scratch/work/ibragir1/ML_project/MassBank-data/stripped_data/"
final_path = "/scratch/work/ibragir1/ML_project/dir/"
list_dir = os.listdir('.')
pattern = "*.txt"
for entry in os.listdir(path):
    if fnmatch.fnmatch(entry, pattern):
        f = open(entry)
        lines = f.readlines()
        first = lines[0]
        for line in first:
            words = first.split()
            formula = words[1]
        print (entry)
        elements = ["N", "S", "Cl", "P", "F", "Na", "Mg", "Ca", "K", "Al", "Mn", "Be", "Li", "Zn"]
        has_element=False
        for element in elements:
            has_element = has_element or element in formula

        f.close()
        if has_element:
            print ("Contain_heavy_elements")
        else:
            copy(entry,final_path)
            print ("Only OCH")
        print (formula)
