#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint, json, urllib2
import nltk, sys, urllib
from bs4 import BeautifulSoup
import csv

from googleapiclient.discovery import build

def link_score(link):
    if ('cv' in link or 'resume' in link) and 'job' not in link:
        return True

def process_file():
    try:
        
        with open('data1.json','r') as fl:
            data = json.load(fl)
        all_links = []    
    #     pprint.pprint(len(data['items']))
        for item in data['items']:
    #         print item['formattedUrl']
            all_links.append(item['formattedUrl'])
        return all_links
    except:
        return []

def main(istart, search_query):
    service = build("customsearch", "v1",
              developerKey="AIzaSyApK0athSzeKSUa8vCNWZe2R1IygAv4bP4")
    
    res = service.cse().list(
        q= search_query,
        cx='007420266948142075924:dsrt3pl0cju',
        num=10,
        gl='in', #in for india comment this for whole web
        start = istart,
      ).execute()
    import json
    with open('data1.json', 'w') as fp:
        json.dump(res, fp)
#     pprint.pprint(type(res))
#     pprint.pprint(res)

def get_email_ph(link_text, pdf=None):
    if pdf==True:
            
        from textract import process
        text = process(link_text)
    else:
        text = link_text
    # print text
    import re
    email = []
    ph = [] 
    valid_ph = re.compile("[789][0-9]{9}$")
    valid = re.compile("[A-Za-z]+[@]{1}[A-Za-z]+\.[a-z]+")
    for token in re.split(r'[,\s]',text):
#     for token in nltk.tokenize(text):
    #     print token
        a = valid.match(token)
        b = valid_ph.match(token)
        if a != None:
            print a.group()
            email.append(a.group())
        if b != None:
            print b.group()    
            ph.append(b.group())
    return email, ph

def process_pdf_link(link):
    html = urllib2.urlopen(link)
    file = open("document.pdf", 'w')
    file.write(html.read())
    file.close()
    return get_email_ph("document.pdf", pdf=True)

def process_doc_link(link):
    testfile = urllib.URLopener()
    testfile.retrieve(link, "document.doc")
    return get_email_ph("document.doc", pdf=False)

def process_docx_link(link):
    testfile = urllib.URLopener()
    testfile.retrieve(link, "document.docx")
    return get_email_ph("document.docx", pdf=False)

def process_links(all_links):
    with open('email_ph.csv', 'wb') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',')
           
        for link in all_links:
            if link[:4] !='http':
                link = "http://"+link
            print link
            try:    
                if link[-3:] == 'pdf':
                    try:
                        email, ph = process_pdf_link(link)
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
                    except:
                        print "error",link
                        print sys.exc_info()
                elif link[-4:] == 'docx':
                    try:
                        email, ph = process_docx_link(link)
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
                    except:
                        print "error",link
                        print sys.exc_info()
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
                elif link[-3:] == 'doc':
                    try:
                        email, ph = process_doc_link(link)
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
                    except:
                        print "error",link
                        print sys.exc_info()
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
                else:
                    try:
                        html = urllib2.urlopen(link)
                        email, ph = get_email_ph(BeautifulSoup(html.read()).get_text(), pdf=False)
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
                    except:
                        print "error",link
                        print sys.exc_info()
                        spamwriter.writerow([link, ' '.join(email), ' '.join(ph)])
            except:
                pass
                print "error",link
                print sys.exc_info()
        
if __name__ == '__main__':
    
#     if len(sys.argv) <2  :
#         print "Error : please pass query words e.g. python customsearch.py java developer"
#         sys.exit()
#     else:
#         search_query = " ".join(sys.argv[1:])
    
#     print search_query
    search_query = ' ASP .NET, C#, WebServices, HTML Chicago USA biodata cv'
#     
#     links = ['http://www.michaelminella.com/resume.html',
#              'www.indeed.com/resumes/Java-J2EE-Developer',
#              'www.slideshare.net/raghavanm/java-j2-eecvguide',
#              'www.gcreddy.com/2013/10/java-3-years-resume.html',
#              'www.naschenweng.info/cv/',
#             'www.shinkarenko.org/cv/IlyaShinkarenkoCV.pdf',
#              'stackoverflow.com/cv/anujpatel',
#             'www.hrishikesh.karambelkar.co.in/resume-hrishikesh-karambelkar.doc',
#             'www.oocities.org/rkbalgi/resume.pdf',
#              'adam.kahtava.com/resume/curriculum-vitae/software-developer/']
#     
    all_links = []
#     all_links.extend(links)
    for i in range(1,90,10):
        main(i, search_query)
        all_links.extend(process_file())
    
    process_links(all_links)
#     import csv
#     with open('email_ph.csv', 'wb') as csvfile:
#         spamwriter = csv.writer(csvfile, delimiter=',')
#         for i in range(1,90,10):
#             main(i)
#             all_links = process_file()
#             for link in all_links:
#                 if link_score(link):
#                     print link
#                     if link[:4] !='http':
#                         link = "http://"+link
#                     if link[-3:] == 'pdf':
#                         html = urllib2.urlopen(link)
#                         file = open("document.pdf", 'w')
#                         file.write(html.read())
#                         file.close()
#                         print("Completed")
#                         email, ph = get_email_ph("document.pdf", pdf=True)
#                         spamwriter.writerow([link, email, ph])
#                     elif link[-3:] == 'doc':
#                         try:
#                             email=[]
#                             ph = []
#                             html = urllib2.urlopen(link)
#                             file = open("document.doc", 'w')
#                             file.write(html.read())
#                             file.close()
#                             print("Completed")
#                             testfile = urllib.URLopener()
#                             testfile.retrieve(link, "document.doc")
#                             email, ph = get_email_ph("document.doc", pdf=True)
#                             spamwriter.writerow([link, email, ph])
#                         except:
#                             spamwriter.writerow([link, email, ph])
#                     else:
#                         try:
#                             email = []
#                             ph = []
#                             html = urllib2.urlopen(link)
#             #                 file = open("document.pdf", 'w')
#             #                 file.write(html.read())
#             #                 file.close()
#             #                 print("Completed")
#                             email, ph = get_email_ph(html.read(), pdf=False)
#                             spamwriter.writerow([link, email, ph])
#                         except:
#                             spamwriter.writerow([link, email, ph])
