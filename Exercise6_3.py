#
# File: Exercise6_3.py
# Name: Christopher M. Anderson
# Date: 01/16/2020
# Course: DSC540 Data Preparation
# Week: 6
# Assignment Exercise: 6.3 Mid-Term Project
#

# ----------| MID-TERM PROJECT |----------

# Objective:

# 1) Replace headers (Data Wrangling with Python pg. 154 – 163)
# 2) Format Data to a Readable Format (Data Wrangling with Python pg. 164 – 168)
# 3) Identify outliers and bad data (Data Wrangling with Python pg. 169 – 174)
# 4) Find Duplicates (Data Wrangling with Python pg. 175 – 178)
# 5) Conduct Fuzzy Matching (if you don’t have an obvious example to do this with in your
#    data, create categories and use Fuzzy Matching to lump data together) (Data Wrangling
#    with Python pg. 179 – 188)

# ------------------------------------------------------------------------------------------
#
#    NOTES:
#
#    The conversion of data from SPSS format to CSV is done in R
#    using the GSSData.R script.
#
#    The result of this conversion is the GSS2018_Original.csv file.
#    Since this is a massive file with over 1,000 columns (headers) and is over
#    20MB in size, this file was then manually edited and saved as GSS2018.csv
#    to get it down to 25 variables (headers) and a smidgen over 1,000 records
#    so that it is much more manageable.
#
#    The SPSS human-readable header value data was achieved by importing the data
#    from the GSS_Codebook_index.pdf into a CSV file file using techniques learned
#    in previous weeks of this course. That file was subsequently cleaned manually
#    (removed empty rows and ones that showed page number information, and then by
#    splitting the contents from the single column of information into two so that
#    the SPSS mnemonic information was in the first column, and its corresponding
#    human-readable value was in the second coulumm. The result of this PDF to CSV
#    conversion and cleaning is the GSSHeaders.csv file.
#
# ------------------------------------------------------------------------------------------

# ----------| 1) REPLACE HEADERS |----------

# Instructions:

# Replace headers (Data Wrangling with Python pg. 154 – 163)

# Objective:

# Import the 2018 General Social Survey data (GSS2018.sav) and our human-readable headers
# data files and match up the SPSS mnemonic header data with the corresponding
# human-readable values.

# from csv import DictReader
#
# data = DictReader(open('GSS2018.csv', 'rt', encoding='utf-8'))
# header = DictReader(open('GSSHeaders.csv', 'rt', encoding='utf-8'))
#
# dataRows = [d for d in data]
# headerRows = [h for h in header]
#
# print(dataRows[:5])
# print(headerRows[:5])
#
# newRows = []
#
# for data_dict in dataRows:
#     new_row = {}
#     for dkey, dval in data_dict.items():
#         for header_dict in headerRows:
#             if dkey in header_dict.values():
#                 new_row[header_dict.get('Description')] = dval
#     newRows.append(new_row)

from csv import reader
import pprint
from fuzzywuzzy import fuzz

data = reader(open('GSS2018.csv', 'rt', encoding='utf-8'))
header = reader(open('GSSHeaders.csv', 'rt', encoding='utf-8'))

dataRows = [d for d in data]
headerRows = [h for h in header if h[0] in dataRows[0]]

print(len(dataRows[0]))
print(len(headerRows))

allShortHeaders = [h[0] for h in headerRows]

skipIndex = []

for header in dataRows[0]:
    if header not in allShortHeaders:
        index = dataRows[0].index(header)
        skipIndex.append(index)

newData = []

for row in dataRows[1:]:
    newRow = []
    for i, d in enumerate(row):
        if i not in skipIndex:
            newRow.append(d)
    newData.append(newRow)

zippedData = []

for dRow in newData:
    zippedData.append(list(zip(headerRows, dRow)))

dataHeaders = []

for i, header in enumerate(dataRows[0]):
    if i not in skipIndex:
        dataHeaders.append(header)

headerMatch = zip(dataHeaders, allShortHeaders)

print(headerMatch)


# ----------| 2) FORMAT DATA TO A READABLE FORMAT |----------

# Instructions:

# Format Data to a Readable Format (Data Wrangling with Python pg. 164 – 168)

# Objective:

# Let's take a look at the first 20 records of our data now showing the rather
# ugly SPSS mnemonic, and the corresponding human readable text value that
# it matches up with

for x in enumerate(zippedData[0][:20]):
    print(x)


# ----------| 3) IDENTIFY OUTLIERS AND BAD DATA |----------

# Instructions:

# Identify outliers and bad data (Data Wrangling with Python pg. 169 – 174)

# Objective:

# We want to ensure that the data we have so carefully cleaned is accurate and
# relevant. Let's do that by checking to see how many 'NA' responses are in the
# data and also verify that the responses are applicable (for example, we don't
# have a 'Yes' or 'No' answer when we are expecting tha type of response, or we
# show content like 'missing' or other anomalies in our data.

# Look for 'NA' responses and get a count of how many there are for each header/category

naCount = {}

for row in zippedData:
    for resp in row:
        question = resp[0][1]
        answer = resp[1]
        if answer == 'NA':
            if question in naCount.keys():
                naCount[question] += 1
            else:
                naCount[question] = 1

pprint.pprint(naCount)

# Create a categorization for each of the type of responses to make
# sure they are legitimate and we can check for potential errors

datatypes = {}

start_dict = {'Digit': 0, 'Yes': 0, 'No': 0,
              'NA': 0, 'Empty': 0, 'Time Related': 0,
              'Text': 0, 'Unknown': 0
              }

for row in zippedData:
    for resp in row:
        question = resp[0][1]
        answer = resp[1]
        key = 'Unknown'
        if answer.isdigit():
            key = 'Digit'
        elif answer == 'NA':
            key = 'NA'
        elif answer == 'YES':
            key = 'Yes'
        elif answer == 'NO':
            key = 'No'
        elif answer.isspace():
            key = 'Empty'
        elif answer.find('/') > 0 or answer.find(':') > 0:
            key = 'Time Related'
        elif answer.isalpha():
            key = 'Text'
        if question not in datatypes.keys():
            datatypes[question] = start_dict.copy()
        datatypes[question][key] += 1

pprint.pprint(datatypes)


# ----------| 4) FIND DUPLICATES |----------

# Instructions:

# Find Duplicates (Data Wrangling with Python pg. 175 – 178)

# Objective:

# Ensure data is accurate by looking for and removing duplicate
# information. Based upon the output of this code, we don't appear
# to have any duplicate information.

for x in enumerate(zippedData[0]):
    print(x)


# ----------| 5) CONDUCT FUZZY MATCHING |----------

# Instructions:

# Conduct Fuzzy Matching (Data Wrangling with Python pg. 179 – 188)
# (If you don’t have an obvious example to do this with in your data,
# create categories and use fuzzy matching to lump data together)

# Objective:

# Fuzzy matching allows you to determine if two items
# (usually strings) are “the same.” I am opting to create categories
# and use fuzzy matching since my data does not appear to have any.

myRecords = [{'favoriteFood': 'street tacos',
              'favoriteDrink': 'coffee and creamer',
              'favoriteDessert': 'peanut butter balls dipped in chocolate',
              },

             {'favoriteFood': 'taco truck tacos',
              'favoriteDrink': 'coffee with creamer',
              'favoriteDessert': 'chocolate covered peanut butter balls',
              }]

print('The fuzzy match for your favorite food is:',
      fuzz.token_sort_ratio(myRecords[0].get('favoriteFood'),
                            myRecords[1].get('favoriteFood')), '%'),

print('The fuzzy match for your favorite drink is:',
      fuzz.token_sort_ratio(myRecords[0].get('favoriteDrink'),
                            myRecords[1].get('favoriteDrink')), '%'),

print('The fuzzy match for your favorite dessert is:',
      fuzz.token_sort_ratio(myRecords[0].get('favoriteDessert'),
                            myRecords[1].get('favoriteDessert')), '%'),
