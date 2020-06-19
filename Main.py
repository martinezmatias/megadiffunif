import sys
from  UnifDiff2Patched import *

input = sys.argv[1]
output = sys.argv[2]
print("input {} output {}".format(input, output))
runvisit(input,output, removeZipFile=True)