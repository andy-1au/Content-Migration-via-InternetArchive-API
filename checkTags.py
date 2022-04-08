import csv
import os
import xml.etree.ElementTree as XET
import pandas as pd
import datetime
from internetarchive import download


def Diff(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))


originalTags = {'language', 'subject', 'volume', 'date', 'call_number', 'publisher', 'description',
                'possible-copyright-status', 'identifier', 'ppi', 'camera',
                'scandate'}

newTags = {'language', 'subject', 'volume', 'pub_date', 'call_number', 'publisher', 'description',
           'copyright_status', 'possible_copyright_status', 'identifier', 'ppi', 'camera',
           'scandate'}

whatChanged = "date changed to pub_date, possible-copyright-status to copyright_status"

# ---------------------CHANGE--------------------#
wantedArray = ['language', 'subject', 'volume', 'pub_date', 'call_number', 'publisher', 'description',
               'copyright_status', 'possible_copyright_status', 'identifier', 'ppi', 'camera',
               'scandate']
# ---------------------CHANGE--------------------#

itemList = 'S:/Digital Projects/Internet Archive Downloads/Burr/burr_itemlist.txt'  # itemlist directory (CHANGE)

with open(itemList) as file:  # opens the file directory
    lines = file.readlines()  # reads in the text file
    lines = [line.rstrip() for line in
             lines]  # puts each line of the text file into a list, using a for loop and rstrip to remove any whitespace
    print(lines)

txtLength = len(lines)  # returns the length of the list
print(str(txtLength) + " files in the list")  # DEBUG, prints out how many files there are

xmlDP = 'S:/Digital Projects/Internet Archive Downloads/Burr/XML'  # String to capture a longer directory address cause API call has some restrictions (CHANGE)

for i in range(txtLength):
    download(lines[i], verbose=True, glob_pattern='*meta.xml', destdir=xmlDP, ignore_existing=True, no_directory=True) #MAKE SURE TO COMMENT THIS LINE OUT IF XML EXISTS
    xmlFileName = lines[i] + '_meta.xml'  # Adds xml extension for file reading reasons
    fullXMLPath = xmlDP + '/' + xmlFileName  # creates full directory path to access the XML file, combines path + name
    tree = XET.parse(fullXMLPath)  # parses the XML data
    root = tree.getroot()  # gets the root of the XML file
    existingTags = []
    for child in root:  # for loop to go through every tag in XML file and matches with the set
        tag = child.tag  # tags are basically header titles, appended only once
        if tag in newTags:
            existingTags.append(tag)  # only appends what the set specified
    print(xmlFileName)
    print(Diff(wantedArray, existingTags))
