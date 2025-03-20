#!/usr/bin/env python3

from cmd_ai import config
from cmd_ai.version import __version__
import json
import os
import datetime as dt
"""

##

#### return json



"""

#from googlesearch import search

from fire import Fire
import datetime as dt
#import requests
#from bs4 import BeautifulSoup
#from bs4.element import Comment


#from selenium import webdriver
#from selenium.webdriver.firefox.options import Options
#from selenium.webdriver.firefox.service import Service
#from subprocess import getoutput

from console import fg


# def tag_visible(element):
#     if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
#         return False
#     if isinstance(element, Comment):
#         return False
#     return True


# def fetch_url_content(url):
#     print("D...  requesting", url)
#     response = requests.get(url)
#     cont = []
#     res=""
#     if response.status_code == 200:
#         print("D...  response is OK")
#         soup = BeautifulSoup(response.text, 'html.parser')
#         texts = soup.findAll(string=True)
#         visible_texts = filter(tag_visible, texts)
#         print(visible_texts)
#         for i in visible_texts:
#             i = i.strip()
#             if len(i)==0: continue
#             cont.append(i)
#         res =  "\n".join(cont)
#         return json.dumps(  {"url_content":res } , ensure_ascii=False)  # MUST OUTPUT FORMAT

#     else:
#         return json.dumps(  {"url_content":res } , ensure_ascii=False)  # MUST OUTPUT FORMAT
#         #return f"Error: Unable to fetch the URL. Status code: {response.status_code}"

def make_dir_with_date( NEWDIR):
    LDIR = os.path.expanduser("/tmp/")
    LILE = "yyymmdd_.org"
    LFILE = "gpt_calendar.log"
    with open( LDIR+LFILE, "a") as f:
        f.write("*************************************************************\n")
        f.write(f"... making folder ........ {NEWDIR}\n")
    os.makedirs(NEWDIR, exist_ok=True)
#
#
#
def setMeetingRecord(  date_, time_, hint, content ):
    """
    All this should be given by AI
    """
    DIR = os.path.expanduser("~/01_Dokumenty/01_Urad/08_pozvani/")
    DIR = DIR.rstrip("/")
    LDIR = os.path.expanduser("/tmp/")
    LFILE = "gpt_calendar.log"
    NEWDIR = (date_)#dt.datetime.strftime("%Y%m%d_%H%M%S")
    NEWDIR = f"{DIR}/{NEWDIR}"

    newhint = hint.replace(" ", "_")

    NEWDIR = f"{date_}_{newhint}"
    NEWDIR = NEWDIR.rstrip("/")
    #NEWDIR = dt.datetime.strftime("%Y%m%d_%H%M%S")
    now = dt.datetime.now().strftime("%Y%m%d_%H%M%S")


    FILE = f"{DIR}/{NEWDIR}/{now}_{newhint}.org"

    make_dir_with_date( f"{DIR}/{NEWDIR}" ) # REALLY MAKE IT

    with open( LDIR+LFILE, "a") as f:
        f.write(f"... ... writing content to {FILE} \n")
        f.write(f"... ... CONTENT:\n")
        f.write(f"... ...    {content} \n\n")
        f.write("\n")

    with open( FILE, "a") as f:
        f.write(content)

    return json.dumps(  {"result":"ok" } , ensure_ascii=False)  # MUST OUTPUT FORMAT

#
#
#
def calendar_update(  date_, hint):
    DIR = os.path.expanduser("~/01_Dokumenty/01_Urad/08_pozvani/")
    DIR = os.path.expanduser("/tmp/")
    NEWDIR = dt.datetime.strftime("%Y%m%d_%H%M%S")
    FILE = "yyymmdd_.org"
    LFILE = "gpt_calendar.log"

    with open( LDIR+LFILE, "a") as f:
        f.write(f"... updating calendar {date_} {hint} \n")
        f.write("\n")

    return json.dumps(  {"result":"ok" } , ensure_ascii=False)  # MUST OUTPUT FORMAT

# def get_google_urls(searchstring):
#     pool = search( searchstring, num_results=5)
#     urls = []
#     cont = []
#     for i in pool:
#         urls.append(i)
#     urls = list(set(urls))
#     for i in urls:
#         #cont.append("# URL ADDRESS:")
#         cont.append(i)
#     res = cont#"\n".join( cont)

#     # must return json for GPT
#     return json.dumps(  {"urls":res } , ensure_ascii=False)  # MUST OUTPUT FORMAT



if __name__=="__main__":
    Fire({'m':make_dir_with_date,
          'f':setMeetingRecord,
          'c':calendar_update})
