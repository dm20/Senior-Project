#GetIP.py

import time # for file name matching
import subprocess # to execute bash scripts

now = time.strftime("%Y%m%d%H%m")

# create the text file containing ifconfig data
# obtain ifconfig as a text file with executable ifconfig_to_txt.sh:
#-----------------------------------------------------------
# #!/bin/bash
# ifconfig > $(date '+%Y%m%d%H%m').txt
#-----------------------------------------------------------
cmd1 = ['./ifconfig_to_txt.sh']
p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
p1.wait()

# get relavent contents
filename = now + '.txt'
inetLines = []
with open(filename) as inputfile:
    for line in inputfile:
        if "inet " in line:
            line = line.strip(' ')
            inetLines.append(line.split(' '))

# delete the text file with executable garbage_collection.sh
#-----------------------------------------------------------
# #!/bin/bash
# rm $(date '+%Y%m%d%H%m').txt
#-----------------------------------------------------------
cmd2 = ['./garbage_collection.sh']
p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
p2.wait()

# Now we assume that the IP Address is located in the line that has
# the most information (maximum length) since the boadcast
# information is usually stored in the relevant line
# (needs verification)
inetLineLengths=[]      
IPAddresses = []
for i in range(len(inetLines)):
    inetLineLengths.append(len(inetLines[i]))

ithLine = inetLineLengths.index(max(inetLineLengths))

ans = inetLines[ithLine][1]
print(ans)
