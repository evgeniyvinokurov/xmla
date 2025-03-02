import sys
import os
import shutil

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))
 
# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)
 
# adding the parent directory to 
# the sys.path.
sys.path.append(parent)

from codes.xmla import base

for d in os.listdir(base.orderspath):
    dd = base.orderspath + d
    if os.path.isdir(dd):
        shutil.rmtree(dd)

for d in os.listdir(base.preorderspath):
    dd = base.preorderspath + d
    if os.path.isdir(dd):
        shutil.rmtree(dd)