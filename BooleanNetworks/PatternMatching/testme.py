import test_walllabels as twl
import test_preprocess as tpp
import test_patternmatch as tpm

twl.testme()
tpp.testme()
tpm.testme()

# command line call: 
# coverage run --include=fileparsers.py,walllabels.py,preprocess.py,patternmatch.py testme.py
# coverage report -m
