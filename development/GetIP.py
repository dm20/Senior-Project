#GetIP.py
# This function requires having made the following bash script
# saved in the root foler (~/Users/Username/) prior to execution
# The contents of this bash script should be the following:
#-----------------------------------------------------------
# #!/bin/bash
# ifconfig > $(date '+%Y%m%d%H%m%S').txt
#-----------------------------------------------------------

import time
import subprocess

now = time.strftime("%Y%m%d%H%m%S")

cmd = ['./scr2.sh']
p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
p.wait()

filename = now + '.txt'

inetLines = []
with open(filename) as inputfile:
    for line in inputfile:
        if "inet " in line:
            inetLines.append(line.split(' '))

        IPAddresses = []
        for i in range(len(inetLines)):
            IPAddresses.append(inetLines[i][1])

# Next we assume the longer IP address is the active one
# and that there are exactly two to choose from
# (needs verification)            
for i in range(len(IPAddresses)):
    if len(IPAddresses[0]) > len(IPAddresses[1]):
        ans = IPAddresses[0]
    else:
        ans = IPAddresses[1]
print(ans)
