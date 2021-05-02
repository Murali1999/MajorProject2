#!/usr/bin/env python3

import argparse
import socket, subprocess
from subprocess import PIPE
import sys, textwrap
import os
import re, random
import texttable
import requests
import json
import stdiomask
from bs4 import BeautifulSoup

#ascii banner for the CLI tool
ret=os.system('toilet --filter metal -f slant bugsploit')
print('')

if sys.version_info[0] < 3:
    print("Python3 is needed to run BugSploit, Try \"python3 project2.py\" instead\n")
    sys.exit(2)

#examples for reference
example = "\nEXAMPLES: \n"
example += "---------------------------------------------------------------------------------------------------> \n" 
example += "root@kali:~/# bugsploit -s facebook.com   #Perform recon and fingerprinting on the target provided \n"                   
example += "You can even add https:// or http:// to the target site \n"
example += "---------------------------------------------------------------------------------------------------> \n"

def msg(name=None):
	return''' -> bugsploit -s site_name
	[This tool is an automated tool which requires only the target site name to 
	start the recon and fingerprinting process. Performs all the scans.] 
	
	-> bugsploit -d google_dork
	[This option can be used to choose the target for the reconnaissance and 
	fingerprinting process.]
	'''

#description about the tool
parser = argparse.ArgumentParser(description='Recon and Fingerprinting Tool', epilog=example, formatter_class=argparse.RawDescriptionHelpFormatter, usage=msg())

#mutually exclusive group title
group1 = parser.add_argument_group('Recon and Fingerprinting Options')
#target site name
group1.add_argument('-s', help='The target site or domain on which recon & fingerprinting has to be performed (if already selected)', action='store')
#google dork option
group1.add_argument('-d', help='Query that you want to dork using google search engine', action='store')

#mutually exclusive group title
#options for report generation
group2 = parser.add_argument_group('Report Generation Options')
#option to generate report
group2.add_argument('-g', help='Generate the report in PDF format', action='store')

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
	
	def wappalyzer(url):
		urls = 'https://'+url
		api_key = 'dhVj82iF6Y81BaXZHnGEY7BH9pAxdoLraID1ePdn'
		endpoint = "https://api.wappalyzer.com/lookup/v2/?urls="
		cmd1 = 'curl -s -H "x-api-key: '
		cmd2 = '" '+ endpoint + urls
		cmd = cmd1 + api_key + cmd2
		resource_response = subprocess.check_output(cmd, shell=True)
		response = json.loads(resource_response)
		ret = json.dumps(response,sort_keys=True, indent=4)
		if "crawl" in ret:
	        	ret = "Website being crawled, please try again in a few minutes."
	        	return ret
		else:
	        	return ret
	
	#ret=cmdline('nslookup {} && dig +noall +answer +multiline txt {}'.format(site, site)).decode('ascii')
	
	ret1=cmdline('dnsrecon -d {}'.format(site)).decode('ascii')
	ret2=cmdline('dig @8.8.8.8 +nocmd {} any +multiline +noall +answer'.format(site)).decode('ascii')
	ret3=cmdline('python3 /root/Desktop/major1/cms-detector.py -s {}'.format(site)).decode('ascii')
	ret4=cmdline('nmap -O {}'.format(site)).decode('ascii')
	ret5=cmdline('uniscan -u {} -e | grep "Scan date:" -A30'.format(site)).decode('ascii')
	ret6=cmdline('uniscan -u {} -g | grep "Scan date:" -A800'.format(site)).decode('ascii')
	ret7=wappalyzer(site)
	
	table = texttable.Texttable()
	table.set_cols_align(["c", "l"])
	table.set_cols_valign(["t", "t"])
	table.set_cols_width([20,100])
	table.add_rows([["Operation Performed", "Output Generated"],
                ["DNS Lookup & Records:", ret1],
		["DNS Enumeration:", ret2],
		["CMS Detection:", ret3],
		["OS Fingerprinting:", ret4],
		["Static Checks and Robots.txt and Sitemap.xml Check:", ret5],
		["Web fingerprinting:", ret6],
		["Technologies used:", ret7]])
	print(table.draw() + "\n")
	
query = args.d
if (args.d):
	print('Google Dork Results:')
	print()
	query = query.replace(' ','+')
	A = ("Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
       	"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
       	"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
        )
	Agent = A[random.randrange(len(A))]
	headers = {'user-agent': Agent}
	i=0
	for i in range(1,21):
		page = requests.get("https://www.google.dz/search?q={}&start={}".format(query,i), headers=headers)
		soup = BeautifulSoup(page.content,'lxml')
		links = soup.findAll("a")
		for link in  soup.find_all("a",href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
    			print(re.split(":(?=http)",link["href"].replace("/url?q=","")))
