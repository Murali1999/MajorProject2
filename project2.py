import argparse
import socket
from subprocess import call
import sys
import os
import re
from termcolor import colored
from colored import fg, bg, attr

#ascii banner for the cli tool
ret=os.system('toilet --filter metal -f slant bugsploit')
print('')

if sys.version_info[0]<3:
  print('Python3 is needed to run the BugSploit. Try \"python3 project2.py\" instead\n")
  sys.exit(2)
