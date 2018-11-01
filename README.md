# MLinMS_project
Machine learning in materials science group project

stripsearch.py:
  Script for filtering through the database entries and writing truncated .txt files. Please download the database from github (see   link on massbank.eu front page), unzip in wanted location, and run this script as executable in 'Mass-Bank-data-master' directory. e.g. './stripsearch.py MS2 POSITIVE'. Script requires python3.x and numpy to run.

PLEASE USE 'stripsearch_v2.py'!!!!!

binary_classifier_v2.py: Binary classifier. Currently works for carbonyl oxygen classification. please run in 'Mass-Bank-data-master' directory after 'stripsearch_v2.py' as './binary_classifier_v2.py'. Prints error and final values of w to files. 
