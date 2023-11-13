from os import listdir
from os.path import isfile, join
import time

mypath = 'Stelleris/'
filename = 'Stelleris/planetarydiversity_l_english - ori.yml'

# allfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
# for f in allfiles:
#     print(f)

for x in range(10):
    print("adwadawdawd\r",x, end='\r')
    time.sleep(1)
print()


count = len(open(filename).readlines())
print(count)
