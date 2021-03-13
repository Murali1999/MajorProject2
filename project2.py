import argparse
import socket, subprocess
from subprocess import PIPE
import sys, textwrap
import os
import re
from termcolor import colored
from colored import fg, bg, attr
from terminaltables import AsciiTable, SingleTable
from prettytable import PrettyTable
from textwrap import fill, wrap

#ascii banner for the cli tool
ret=os.system('toilet --filter metal -f slant bugsploit')
print('')

if sys.version_info[0]<3:
  print('Python3 is needed to run the BugSploit. Try \"python3 project2.py\" instead\n")
  sys.exit(2)

#examples for reference
example = "\nEXAMPLES: \n"
example += "-------------------------------------------------------------------------------------------> \n" 
example += "spyder -s linkedin.com -d   \n"                   
example += "You can even add https:// or http:// to the target site \n"
example += "-------------------------------------------------------------------------------------------> \n"

def msg(name=None):
	return''' bugsploit -s site_name
	[This tool is an automated tool which requires only the target site name to 
	start the recon and fingerprinting process.] 
	'''

#description about the tool
parser = argparse.ArgumentParser(description='Recon and Fingerprinting Tool', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter, usage=msg())

#mutually exclusive group title
group1 = parser.add_argument_group('Recon and Fingerprinting Options')
#target site name (required flag)
group1.add_argument('-s', help='The target site or domain on which recon & fingerprinting has to be performed', action='store')

#mutually exclusive group title
#options for report generation

args = parser.parse_args()
site = args.s
if (args.s):
	print('-> Target site name: {}'.format(site))
	print()

def cmdline(command):
    process = subprocess.check_output(
        args = command,
        shell = True
    )
    return process
#ret=cmdline('nslookup {} && dig +noall +answer +multiline txt {}'.format(site, site)).decode('ascii')
ret1=cmdline('dnsrecon -d {}'.format(site)).decode('ascii')
ret2=cmdline('dig @8.8.8.8 +nocmd {} any +multiline +noall +answer'.format(site)).decode('ascii')
#ret3
#ret4


table = PrettyTable(padding_width=3)
table.title = 'Vulnerability Report'
table.align["Action Performed"] = 'c'
table.align["Output"] = 'c'
table.field_names = ["Action Performed", "Output"]
table.add_row(['DNS Lookup and Records: ', fill(ret1, width=60)])
table.add_row(['DNS Enumeration: ', fill(ret2, width=60)])
table.hrules = 1
table.align = 'l'
print(table)
