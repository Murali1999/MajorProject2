#!/usr/bin/env python3

import argparse
import socket
import subprocess
from subprocess import PIPE
import sys
import os
import time
import re
import random
import texttable
import json
import stdiomask
import requests
import datetime
from fpdf import FPDF
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
example += "root@kali:~/# bugsploit -s facebook.com -g  #Generate a report of the result in pdf format \n"
example += "You can even add https:// or http:// to the target site \n"
example += "---------------------------------------------------------------------------------------------------> \n"

def msg(name=None):
	return''' -> bugsploit -s site_name
	[This tool is an automated tool which requires only the target site name 
	to start the recon and fingerprinting process. Performs all the scans and 
	displays the result in a tabular format.] 
	
	-> bugsploit -d google_dork
	[This option can be used to choose the target for the reconnaissance and 
	fingerprinting process.]
		
	-> bugsploit -d site_name -g 
	[This option displays the result in tabular format and also generates a 
	report of the result in pdf format.]
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

def cmdline(command):
	process = subprocess.check_output(
	args = command,
	shell = True
	)
	return process

def wappalyzer(url):
	urls = 'https://'+url
	api_key = '9NObxFYB5jZf7z8SdyC1xmrc1Wfk27cCZRmV5f00'
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

ret1=cmdline('dnsrecon -d {}'.format(site)).decode('ascii')
ret2=cmdline('dig @8.8.8.8 +nocmd {} any +multiline +noall +answer'.format(site)).decode('ascii')
ret3=cmdline('python3 /root/Desktop/major1/cms-detector.py -s {}'.format(site)).decode('ascii')
ret4=cmdline('nmap -O {}'.format(site)).decode('ascii')
ret5=cmdline('uniscan -u {} -e | grep "Scan date:" -A30'.format(site)).decode('ascii')
ret6=cmdline('uniscan -u {} -g | grep "Scan date:" -A800'.format(site)).decode('ascii')
ret7=wappalyzer(site)
	
#recon and fingerprinting option
if (args.s):
	print('-> Target site name: {}'.format(site))
	print()

	#ret=cmdline('nslookup {} && dig +noall +answer +multiline txt {}'.format(site, site)).decode('ascii')
	
	ret1=cmdline('dnsrecon -d {}'.format(site)).decode('ascii')
	print(ret1)
	os.system('clear')
	print('(1/7) DNS Lookup completed..... ')
	ret2=cmdline('dig @8.8.8.8 +nocmd {} any +multiline +noall +answer'.format(site)).decode('ascii')
	print(ret2)
	os.system('clear')
	print('(2/7) DNS Enumeration completed.....')
	ret3=cmdline('python3 /root/Desktop/major1/cms-detector.py -s {}'.format(site)).decode('ascii')
	print(ret3)
	os.system('clear')
	print('(3/7) CMS Detection completed.....')
	ret4=cmdline('nmap -O {}'.format(site)).decode('ascii')
	print(ret4)
	os.system('clear')	
	print('(4/7) OS Fingerprinting completed.....')
	ret5=cmdline('uniscan -u {} -e | grep "Scan date:" -A30'.format(site)).decode('ascii')
	print(ret5)
	os.system('clear')
	print('(5/7) Static Checks completed.....')
	ret6=cmdline('uniscan -u {} -g | grep "Scan date:" -A800'.format(site)).decode('ascii')
	print(ret6)
	os.system('clear')
	print('(6/7) Web Fingerprinting completed.....')
	ret7=wappalyzer(site)
	print(ret7)
	os.system('clear')
	print('(7/7) Technologies used found.....')
	print('All scans are completed, generating report now.')
	time.sleep(2)
	os.system('clear')
	
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
		["Technologies Used:", ret7]])
	print(table.draw() + "\n")

#google dorking option
query = args.d
if (args.d):
	print('Getting google dork results....')
	os.system('clear')
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

#pdf generation option
if (args.g):
	from datetime import date
	today=date.today()
	now=today.strftime('%A, %B %d, %Y')

	pdf = FPDF()
	
	pdf.add_page()
	pdf.set_font("Arial",size=28)
	pdf.multi_cell(190,90,txt='         ',align='J')
	pdf.multi_cell(190,18,txt='Reconnaissance &',align='C')
	pdf.multi_cell(190,18,txt='Fingerprinting',align='C')
	pdf.multi_cell(190,18,txt='Report',align='C')
	pdf.multi_cell(190,18,txt=now,border=1,align='C')

	pdf.add_page()
	pdf.set_font("Arial",size=8.5)
	pdf.multi_cell(200,30,txt='         ',align='J')
	pdf.cell(50,5, txt='DNS Lookup and Records:',align='L')  
	pdf.multi_cell(200,5,txt=ret1,align='L')
	pdf.multi_cell(200,5,txt='         ',align='J')
	pdf.cell(50,5, txt='DNS Enumeration:', align='L')
	pdf.multi_cell(200,5,txt=ret2,align='L')

	pdf.add_page()
	pdf.set_font("Arial",size=8.5)
	pdf.cell(30,5, txt='CMS Detection:',align='L')
	pdf.multi_cell(200,5,txt=ret3,align='L')
	pdf.multi_cell(200,10,txt='         ',align='J')
	pdf.cell(30,5, txt='OS Fingerprinting:',align='L')  
	pdf.multi_cell(200,5,txt=ret4,align='L')
	pdf.multi_cell(200,20,txt='         ',align='J')
	pdf.cell(30,5, txt='Static Checks:',align='L')  
	pdf.multi_cell(200,5,txt=ret5,align='L')

	pdf.add_page()
	pdf.set_font("Arial",size=9)
	pdf.cell(30,5, txt='Web Fingerprinting:',align='L')
	pdf.multi_cell(200,5,txt=ret6,align='L')

	pdf.add_page()
	pdf.set_font("Arial",size=9)
	pdf.cell(30,5, txt='Technologies used:',align='L')
	pdf.multi_cell(200,5,txt=ret7,align='L')

	pdf.output("myresult.pdf")
