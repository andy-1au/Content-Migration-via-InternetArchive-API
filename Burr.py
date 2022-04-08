import csv
import os
import xml.etree.ElementTree as XET
import pandas as pd
import datetime
from internetarchive import download

TAGS_WANTED = {'language', 'subject', 'volume', 'pub_date', 'call_number', 'publisher', 'description',
               'copyright_status', 'possible_copyright_status', 'identifier', 'ppi', 'camera',
               'scandate'}  # SET used to search for specific tags in XML file
                            # the pub date might be different for certain files --- search through the XML files to see what it is (CHANGE "pub_date")
                            # copyright-status may be different  (CHANGE)

replaceList = {'language': 'Language-Code', 'subject': 'Subject-Topic', 'volume': 'Volume-Number',
               'date': 'Date-Created', 'pub_date': 'Date-Created', 'call_number': 'Call-Number', 'publisher': 'Publisher',
               'description': 'Description-Abstract',
               'possible-copyright-status': 'Rights', 'copyright_status': 'Rights', 'mediatype': 'Type', 'identifier': 'Identifier', 'ppi': 'PPI',
               "camera": 'Capture-Device',
               'scandate': 'Date-Captured'}  # dictionary similar to set above, used to replace header array elements with more specific rules
                                             # (CHANGE) the 'date' or 'pubdate' tag 

additionalHeadersList = ["pid", "parent_object", "cmodel", "object_location", "label", "Title", "Type", "Year",
                         "Language-Code",
                         "Language-Text", "Format", "Format-URL", "File-Format", "Digital-Origin",
                         "Rights"]  # adding the other needed headers

itemList = 'S:/Digital Projects/Internet Archive Downloads/Burr/burr_itemlist.txt'  # itemlist directory (CHANGE)

with open(itemList) as file:  # opens the file directory
    lines = file.readlines()  # reads in the text file
    lines = [line.rstrip() for line in lines]  # puts each line of the text file into a list, using a for loop and rstrip to remove any whitespace
    print(lines)

txtLength = len(lines)  # returns the length of the list
print(str(txtLength) + " files in the list")  # DEBUG, prints out how many files there are

xmlDP = 'S:/Digital Projects/Internet Archive Downloads/Burr/XML'  # String to capture a longer directory address cause API call has some restrictions (CHANGE)

for i in range(txtLength):
    download(lines[i], verbose=True, glob_pattern='*meta.xml', destdir=xmlDP, ignore_existing=True, no_directory=True)

    csvPath = 'S:/Digital Projects/Internet Archive Downloads/Burr/CSV/'  # (CHANGE) directory path for where CSV file is located
    xmlFileName = lines[i] + '_meta.xml'  # Adds xml extension for file reading reasons
    fullXMLPath = xmlDP + '/' + xmlFileName  # creates full directory path to access the XML file, combines path + name
    # print(xmlFileName)  # DEBUG
    # print(fullXMLPath)  # DEBUG
    csvFileName = lines[i] + '.csv'  # creates the same file name with CSV format
    fullCSVPath = csvPath + csvFileName
    # print(csvFileName)  # DEBUG
    # print(fullCSVPath)  # DEBUG
    tree = XET.parse(fullXMLPath)  # parses the XML data
    root = tree.getroot()  # gets the root of the XML file

    # Write Headers ---------------------
    CSV_Data = open(fullCSVPath, 'w', encoding='utf-8',
                    newline='')  # creates a new CSV file for writing with parameters
    # newline is made so that there aren't any empty lines after what is written
    # encoding matches what is on the XML File
    CSVWriter = csv.writer(CSV_Data)  # allows for writing in the CSV File
    CSV_Header = []  # creates a list for the header of the CSV File

    for child in root:  # for loop to go through every tag in XML file and matches with the set
        tag = child.tag  # tags are basically header titles, appended only once
        if tag in TAGS_WANTED:
            CSV_Header.append(tag)  # only appends what the set specified

    listToReplace = CSV_Header
    newList = (pd.Series(listToReplace)).map(replaceList)  # convert the list to a pandas series temporarily before mapping and replacing values
    # this func accepts a dict or a series
    # values that are not found in the dict are converted to NaN, unless the dict has a default value (defaultdict)
    listReplaced = list(newList)
    for x in range(len(additionalHeadersList)):
        listReplaced.append(additionalHeadersList[x])  # ADD ADDITIONAL HEADERS
    # print(listReplaced) #DEBUG
    CSVWriter.writerow(listReplaced)
    # Write Headers -----------------

    # Write Main DATA(first row) - different for the other rows -----------------
    CSV_Main = []  # list for main data

    # Additional DATA
    pid = "digitalcollections:" + lines[i]
    parent_object = "digitalcollections:student-publications"
    cmodel = "islandora:bookCModel"  # fill
    object_location = ""
    label = ""
    title = ""
    Type = "text"
    year = ""
    language_code = "eng"
    language_text = "English"
    Format = "books"
    format_uri = "http://vocab.getty.edu/page/aat/300028051"
    file_format = "image/jp2"
    digital_origin = "reformatted digital"
    rights = "http://rightsstatements.org/vocab/InC/1.0/"
    # Additional DATA

    for child in root:  # same as for loop up top, except it appends the element instead
        tag = child.tag
        if tag == 'scandate':  # TEST
            scanYear = (int)(child.text[0:4])  # inclusive for the first number, exclusive for the second
            scanMonth = (int)(child.text[4:6])
            scanDate = (int)(child.text[6:8])
            timestamp = datetime.date(scanYear, scanMonth, scanDate)  # date formatting
            CSV_Main.append(timestamp)
        elif tag == 'title':
            label = child.text
            title = child.text
        elif tag in TAGS_WANTED:
            CSV_Main.append(child.text)
            if tag == 'pub_date': # (CHANGE)
                year = child.text

    # Write first row data
    firstRowData = [pid, parent_object, cmodel, object_location, label, title, Type, year, language_code, language_text, Format, format_uri, file_format, digital_origin, rights]
    for addData in range(len(firstRowData)):
        CSV_Main.append(firstRowData[addData])
    CSVWriter.writerow(CSV_Main)
    # Write first row data ------------

    # Write Main DATA(first row) - different for the other rows ----------------

    # Remove certain pictures -------------------
    scanDataDP = 'S:/Digital Projects/Internet Archive Downloads/Burr/scandata'  # (CHANGE) DIRECTORY
    download(lines[i], verbose=True, glob_pattern='*scandata.xml', destdir=scanDataDP, ignore_existing=True,
             no_directory=True)

    SDFileName = lines[i] + '_scandata.xml'  # Adds xml extension for file reading reasons
    fullSDPath = scanDataDP + '/' + SDFileName
    SDFolderPath = 'S:/Digital Projects/Internet Archive Downloads/Burr/' # (CHANGE)
    SDFolderFileName = lines[i] + '_jp2/'
    finalSDPath = SDFolderPath + SDFolderFileName + SDFolderFileName  # 2x folderName cause we have redundate folders

    tree = XET.parse(fullSDPath)
    root = tree.getroot()
    for child in root.findall("./pageData/"):
        storeAttrib = child.get('leafNum')
        for subChild in child:  # in the node leafNum basically
            if subChild.tag == 'addToAccessFormats':
                if subChild.text == "false":
                    keyCode = str(storeAttrib).zfill(4)
                    print(lines[i] + keyCode + " should be removed")
                    deleteFilePath = finalSDPath + lines[i] + "_" + keyCode + ".jp2"
                    if os.path.exists(deleteFilePath):
                        os.remove(deleteFilePath)
                        print(lines[i] + "_" + keyCode + ".jp2" + " has been removed")  # DEBUG
                    else:
                        print(lines[i] + keyCode + ": The file location does not exist")
    # Remove certain pictures -------------------

    # Write Additional -----------------
    allRows = []
    addRowsData = []  # arr for appending the repeated data
    imagesList = []  # for storing the directory of the images
    folderName_add = "Alumni Bulletin" # (CHANGE)
    parent_object_add = "digitalcollections:" + lines[i]
    cmodel_add = "islandora:pageCModel"
    type_add = "text"
    digital_origin_add = "reformatted digital"
    rights_add = "http://rightsstatements.org/vocab/InC/1.0/"
    pid_empty = ""
    year_empty = ""
    language_c_empty = ""
    lanaguage_t_empty = ""
    format_empty = ""
    format_uri_empty = ""
    file_format_empty = ""

    #loop to find all of the image files and append it to a list
    for x in os.listdir(finalSDPath):
        if x.endswith(".jp2"):
            imagesList.append(x)

    for j in range(len(imagesList)):
        object_location_add = "Internet Archive Downloads/" + folderName_add + "/" + SDFolderFileName + SDFolderFileName + imagesList[j] 
        label_add = label + " " + str(j + 1).zfill(3)
        title_add = label + " " + str(j + 1).zfill(3)  # -----------------------
        addRowsData = ["", "", "", "", "", "", "", "", "", "", "", "", pid_empty, parent_object_add,
                       cmodel_add, object_location_add, label_add, title_add, type_add, year_empty, language_c_empty,
                       lanaguage_t_empty, format_empty, format_uri_empty, file_format_empty, digital_origin_add, rights_add]
        allRows.append(addRowsData)
    CSVWriter.writerows(allRows)
    CSV_Data.close()
    # Write Additional -----------------

# Verbose=True    : Makes the program easier to debug with detailed outputs of errors in the terminal
# glob_pattern    : Only return files matching the given glob pattern, glob patterns specify sets of filenames with wildcard characters such as *
# destdir         : Downloads to the desired file path
# ignore_existing : Skip files that already exist locally
# no_directory    : Ignores creating an item directory(folder), downloads the file directly

# Date header tag can be different, same for Rights (FOR AB its 'possible-copyright-status')
# Date published different tga, please change