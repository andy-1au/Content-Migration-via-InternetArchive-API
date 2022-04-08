import pandas as pd
import glob

concatenateFileName = 'Alumni_Bulletin_Concatenate' + '.csv'
concatenatePath = 'S:\Digital Projects\Internet Archive Downloads\Alumni Bulletin\CSVConcatenate/' + concatenateFileName

all_filenames = [i for i in glob.glob('../Alumni Bulletin/CSV/*.csv')]
df = pd.concat([pd.read_csv(f) for f in all_filenames])
print(df)
df.set_axis(["Index", "Volume-Number", "Subject-Topic", "Description-Abstract", "Creator", "Date-Created", "Language-Code",
             "Rights", "Call-Number", "Identifier",	"PPI", "Capture-Device", "Date-Captured", "pid", "parent_object",
             "cmodel", "object_location", "label", "Title", "Type", "Year", "Language-Code", "Language-Text", "Format",
             "Format-URL", "File-Format", "Digital-Origin"	"Rights"], axis=1) #axis = 1 is for columns
print(df)
df.to_csv(concatenatePath)



