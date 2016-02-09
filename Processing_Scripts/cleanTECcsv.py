import csv
import sys 
import re


def sterilize_token(token):
    bs0 = BadNumberSub(0, ["o","Q","O","C","X"])
    bs1 = BadNumberSub(1, ["i","J", "I","!","L","l"])
    bs4 = BadNumberSub(4, ["h", "^"])
    bs6 = BadNumberSub(6, ["b"])
    bs7 = BadNumberSub(7, ["?", "T"])
    bs8 = BadNumberSub(8, ["B"])
    bs9 = BadNumberSub(9, ["g"])
    
    temp_token = token
    
    for badSub in [bs0, bs1, bs4, bs6, bs7, bs8, bs9]:
        for sub in badSub.badSubList:
            temp_token = temp_token.replace(sub, str(badSub.number))

    return temp_token


def scrub_timestamp(timestamp):
    values = re.split(" ", timestamp)
    i = 0
    days = 0    
    days = sterilize_token(values[i])
    i += 1
    hours = sterilize_token(values[i])
    i += 1
    minutes = sterilize_token(values[i])
    i += 1
    seconds = sterilize_token(values[i])
    
    cleanTimestamp = days + " " + hours + " " + minutes + " " + seconds
    
    testCleanTimestamp = cleanTimestamp.replace(' ', '')    
    if not testCleanTimestamp.isdigit():
        print "Uncleanable timestamp: " + cleanTimestamp + " - " + timestamp.replace(" ", "|")

    return cleanTimestamp


class BadNumberSub:
    def __init__(self, number, bad_sub_list):
        self.number = number
        self.badSubList = bad_sub_list


def scrub_callsign(callsign):
    # callsign = callsign.upper()
    callsign = callsign.strip()
    callsign = callsign.upper()
    if callsign == "MCC":
        callsign = "CC"
    return callsign


SECONDS_OFFSET = 0
TIMESTAMP_PARTS = 4


def GETFromTimestamp(timestamp):
    values = re.split(" ", timestamp);
    i = 0
    days = 0
    if TIMESTAMP_PARTS > 3:
        days = int(values[i])
        i += 1
    hours = int(values[i])
    i += 1
    minutes = int(values[i])
    i += 1
    seconds = int(values[i])

    return str((days * 24) + hours).zfill(3) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    # return (seconds + (minutes * 60) + (hours * 60 * 60) + (days * 24 * 60 * 60)) - SECONDS_OFFSET

pageCounter = 8
curRow = 0

output_file_name_and_path = "../MISSION_DATA/AS14_TECa_cleaned.csv"
outputFile = open(output_file_name_and_path, "w")

callsignList = []
lastTimestamp = 0

for curFile in ["AS14_TECa.csv"]:
    inputFilePath = "../MISSION_DATA/" + curFile
    reader = csv.reader(open(inputFilePath, "rU"), delimiter='|')
    for row in reader:
        curRow += 1
        # if row[1].__len__() > 7:
        # 	print curRow
        # 	print "------------- Page: " + str(pageCounter) + " ::" + row[1]
        time_stamp = row[0].replace(' ', '') + " " + row[1].replace(' ', '') + " " + row[2].replace(' ', '') + " " + row[3].replace(' ', '')
        # print(row)

        scrubbedCallsign = scrub_callsign(row[4])
        # if not scrubbedCallsign in callsignList:
        #    callsignList.append(scrubbedCallsign)
        #    print "Page: " + str(pageCounter) + " : " + scrubbedCallsign

        curTimestamp = scrub_timestamp(time_stamp).replace(' ', '')
        if not curTimestamp >= lastTimestamp:
            print 'Timestamp out of order: Row: {0} Timestamp: {1}'.format(curRow, time_stamp.replace(" ", "|"))
        lastTimestamp = curTimestamp

        outputLine = '{0}|{1}|{2}\n'.format(GETFromTimestamp(scrub_timestamp(time_stamp)), scrubbedCallsign, row[5])
            
        outputFile.write(outputLine)
        print outputLine
outputFile.close()