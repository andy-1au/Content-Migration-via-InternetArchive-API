import pandas as pd
import glob

concatenateFileName = 'Alumni_Bulletin_Concatenate' + '.csv'
concatenatePath = 'S:\Digital Projects\Internet Archive Downloads\Alumni Bulletin\CSVConcatenate/' + concatenateFileName

all_filenames = [i for i in glob.glob('../Alumni Bulletin/CSV/*.csv')]
df = pd.concat([pd.read_csv(f) for f in all_filenames])
#---------TEMP SECTION TO CHANGE HEADERS----------
print(df) #DEBUG
df.set_axis(["Index", "Volume-Number", "Subject-Topic", "Description-Abstract", "Creator", "Date-Created", "Language-Code",
             "Rights", "Call-Number", "Identifier",	"PPI", "Capture-Device", "Date-Captured", "pid", "parent_object",
             "cmodel", "object_location", "label", "Title", "Type", "Year", "Language-Code", "Language-Text", "Format",
             "Format-URL", "File-Format", "Digital-Origin"	"Rights"], axis=1) #axis = 1 is for columns
print(df) #DEBUG
#---------TEMP SECTION TO CHANGE HEADERS---------- (can remove)
#.1 occurs when we have the same headers
# try using. df.rename(index: ' ', string: ' ') 
df.to_csv(concatenatePath, index=False)



