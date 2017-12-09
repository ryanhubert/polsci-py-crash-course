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

wdir = "" # Need to set your own working directory
os.chdir(wdir)

# Fun with variable definitions
test_integer = "0" # gives you a character zero
test_string = 0 # gives you an integer zero

test_integer = int(test_integer) # converts to integer
test_string = str(test_string) # converts to string



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
print(raised)

raised = {x.split('\t')[0] : x.split('\t')[1] for x in raised.split('\n') if len(x.split('\t')) > 1}
raised = {x : float(re.sub("[,\$]","",raised[x])) for x in raised}

with open(wdir + '/warren.csv', "w") as f:
    for x in raised:
        f.write("WARREN,MA," + x + ',' + str(raised[x]) + '\n')



# BOX INSTANCE SETUP

from BoxAuthenticate import BoxAuth

box_user = '' # need to put your ucd email address/ Box username
box_client = BoxAuth(box_user)
box_folder_id = '' # Find the ID number of the folder you want to save your stuff in

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
            return("NA")
        else:
            raise

# Save the fund raising data to Box
BoxSave(wdir + '/warren.csv',"warren_funding.csv",box_folder_id)
        
        
# SENATOR WARREN PRESS RELEASES

url = "https://www.warren.senate.gov/?p=press_releases"

browser = webdriver.Firefox()
browser.get(url)            
raw = UnicodeDammit(browser.page_source).unicode_markup

soup = BeautifulSoup(raw,"html.parser")

releases = [x.get("href") for x in soup.find_all('a')] # extract all links
releases = [x for x in releases if x != None] # remove empty strings
releases = [x for x in releases if 'press_release' in x] # remove links to things that are not press releases
releases = [x for x in releases if re.search("^/",x)] # look for relative links (as opposed to, eg, facebook)
releases = [x for x in releases if "id" in x] # search for specific pattern used in press release urls
releases = ['https://www.warren.senate.gov' + x for x in releases] # generate full url
releases = sorted(set(releases)) # remove duplicates by forcing it to be a set
       
udict = {'row_ids': [] }


def PressRelease(r):
    """
    This function processes a press release and adds word counts to 
    the dictionary udict. Each key in udict is a token, with a value 
    that is a list of word counts for each document. 
    The special key 'row_ids' yields the metadata for each press release.
    """
    doc_id = len(udict['row_ids']) + 1
    browser.get(r)            
    raw = UnicodeDammit(browser.page_source).unicode_markup
    soup = BeautifulSoup(raw,"html.parser")
    for script in soup(["script", "style"]):
        script.extract()
        
    text = soup.text[0:re.search("\#\#\#",soup.text).end()] # extracts text from beginning to the end of each PR w/ ###
    text = text.replace("\xa0"," ") # removes some bad characters
    text = re.sub('\t\t+','\t',text) # remove excess tabs
    text = text[re.search("Home.Newsroom.Press Releases",text).end():] # remove top of page stuff
    
    date = re.search("[A-Z][a-z]+ \d+, 20\d\d",text).group(0) # extract date
    date = datetime.datetime.strptime(date, '%b %d, %Y').date() # convert to date-time format
    
    pt = SnowballStemmer("english") # import porter stemmer from nltk
    
    # The following is commonly used "recipe" for text analysis. 
    # For your application, you may need to make changes
    tokens = text.lower() # remove capitalization
    tokens = re.sub('\n',' ',tokens) # remove line breaks, replace with space
    tokens = re.sub('\-',' ',tokens) # remove dashes, replace with space. (Keeps natural words apart)
    tokens = re.sub('[^a-z ]','',tokens) # remove anything except letters a-z and spaces
    tokens = tokens.split(' ') # split string into list of words, "tokens"
    tokens = [x for x in tokens if len(x) > 1] # remove single letters
    tokens = [pt.stem(x) for x in tokens] # stem each of the words
    
    stop_words = open(wdir + '/stopEnglish.txt').read() # import list of stop words
    stop_words = re.sub('\-',' ',stop_words) # apply same steps as above (need stop words to align in formatting)
    stop_words = re.sub('[^a-z \n]','',stop_words)
    stop_words = stop_words.split('\n')
    stop_words = [pt.stem(x) for x in stop_words]
    
    tokens = [x for x in tokens if x not in stop_words] # remove stop words from list of tokens
    
    for t in set(tokens): # make sure all tokens are in udict
        if t not in udict:
            udict[t] = [0] * (doc_id-1) # if adding a new word, put zeroes for previous press releases
    
    for t in udict: # add word counts
        if t == 'row_ids':
            continue
        if t in tokens:
            udict[t].append(tokens.count(t))
        else:
            udict[t].append(0)
    
    # save to box
    saved_to_box = BoxSave(text,
                           "WARREN-" + str(doc_id).zfill(2) + ".txt",
                           box_folder_id)
    
    udict['row_ids'].append('WARREN,' + str(date) + "," + str(saved_to_box))        

for x in releases[0:5]: # take the first  5. Process them and save to box.
    time.sleep(2)
    PressRelease(x)

# Generate a document term matrix for use in text analysis
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