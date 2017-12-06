#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Ryan Hübert
# Department of Political Science
# University of California, Davis

# Website: https://www.ryanhubert.com/

"""
Python crash course -- UC Davis Political Science
"""

import os
import re
import time
import datetime
import smtplib
import keyring
from getpass import getpass
from io import StringIO
from selenium import webdriver
from bs4 import UnicodeDammit, BeautifulSoup
from nltk import SnowballStemmer

wdir = ""
os.chdir(wdir)



# SENATOR WARREN FUNDRAISING DATA

url = "https://www.fec.gov/data/candidate/S2MA00170/"

browser = webdriver.Firefox()
browser.get(url)            
raw = UnicodeDammit(browser.page_source).unicode_markup

soup = BeautifulSoup(raw,"html.parser")

raised = [x.text for x in soup.find_all("table") if 'Total receipts' in x.text]
raised = raised[0]

raised = re.sub("  +", "", raised)
raised = re.sub("\n\n+", "\n", raised)
raised = re.sub("\n\$", "\t$", raised)

raised = {x.split('\t')[0] : x.split('\t')[1] for x in raised.split('\n') if len(x.split('\t')) > 1}
raised = {x : float(re.sub("[,\$]","",raised[x])) for x in raised}

with open(wdir + '/warren.csv', "w") as f:
    for x in raised:
        f.write("WARREN,MA," + x + ',' + str(raised[x]) + '\n')



# BOX INSTANCE SETUP

from BoxAuthenticate import BoxAuth

box_user = ''
box_client = BoxAuth(box_user)
box_folder_id = ''

def BoxSave(to_save,box_filename,box_folder_id):
    box_folder = box_client.folder(box_folder_id)
    try:
        if re.search('\.(txt|csv|html|json|md) *$',to_save):
            newfile = box_folder.upload(to_save, file_name = box_filename)
            return(newfile.id)
        else:
            to_write = StringIO()
            to_write.write(to_save)
            newfile = box_folder.upload_stream(to_write, box_filename)
            return(newfile.id)
    except Exception as e:
        if 'Item with the same name already exists' in str(e):
            print("Warning: already created a file with this name\nContinuing...")
        else:
            raise

        
        
# SENATOR WARREN PRESS RELEASES

url = "https://www.warren.senate.gov/?p=press_releases"

browser = webdriver.Firefox()
browser.get(url)            
raw = UnicodeDammit(browser.page_source).unicode_markup

soup = BeautifulSoup(raw,"html.parser")

releases = [x.get("href") for x in soup.find_all('a')]
releases = [x for x in releases if x != None]
releases = [x for x in releases if 'press_release' in x]
releases = [x for x in releases if re.search("^/",x)]
releases = [x for x in releases if "id" in x]
releases = ['https://www.warren.senate.gov' + x for x in releases]
       
udict = {'row_ids': [] }

r = releases[0]

doc_id = len(udict['row_ids']) + 1
browser.get(r)            
raw = UnicodeDammit(browser.page_source).unicode_markup
soup = BeautifulSoup(raw,"html.parser")
for script in soup(["script", "style"]):
    script.extract()
    
text = soup.text[0:re.search("\#\#\#",soup.text).end()]
text = text.replace("\xa0","")
text = re.sub('\t\t+','\t',text)
text = text[re.search("Home.Newsroom.Press Releases",text).end():]

date = re.search("[A-Z][a-z]+ \d+, 20\d\d",text).group(0)
date = datetime.datetime.strptime(date, '%b %d, %Y').date()

pt = SnowballStemmer("english")

tokens = text.lower()
tokens = re.sub('\n',' ',tokens)
tokens = re.sub('\-',' ',tokens)
tokens = re.sub('[^a-z ]','',tokens)
tokens = tokens.split(' ')
tokens = [x for x in tokens if len(x) > 1]
tokens = [pt.stem(x) for x in tokens]

stop_words = open(wdir + '/stopEnglish.txt').read()
stop_words = re.sub('\-',' ',stop_words)
stop_words = re.sub('[^a-z \n]','',stop_words)
stop_words = stop_words.split('\n')
stop_words = [pt.stem(x) for x in stop_words]

tokens = [x for x in tokens if x not in stop_words]

for t in set(tokens):
    if t in udict:
        udict[t].append(tokens.count(t))
    else:
        udict[t] = [0] * (doc_id-1) + [tokens.count(t)]

saved_to_box = BoxSave(text,
                       "WARREN-" + str(doc_id).zfill(2) + ".txt",
                       box_folder_id)

udict['row_ids'].append('WARREN,' + str(date) + "," + str(saved_to_box))        

#time.sleep(2)

for u in udict:
    if len(udict[u]) == len(udict['row_ids']) - 1:
        udict[u].append(0)

with open(wdir + '/dtm.csv', "w") as f:
    header = [x for x in sorted(udict.keys()) if x != 'row_ids']
    f.write('SENATOR,DATE,BOX_FILE_ID,' + ','.join(header) + '\n')
    for x in range(0,len(udict['row_ids'])):
        row = [str(udict[u][x]) for u in header]
        f.write(udict['row_ids'][x] + ',' + ','.join(row) + '\n')

saved_to_box = BoxSave(wdir + "/dtm.csv","dtm.csv",box_folder_id)
browser.get('https://ucdavis.app.box.com/file/' + str(saved_to_box))



# SEND AN EMAIL

from_address = input("From: ")
to_address = input("To: ")
subject = input("Subject Line: ")
message = input("Message: ")
msg = "\r\n".join([
      "From: " + from_address,
      "To: " + to_address,
      "Subject: " + subject,
      "",
      message
      ])
   
try:
    password = keyring.get_password('python_gmail', from_address)
except:
    print("Type your password:")
    password = getpass()
    keyring.set_password('python_gmail', from_address, password)

server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(from_address,password)
server.sendmail(from_address, to_address, msg)
server.quit()