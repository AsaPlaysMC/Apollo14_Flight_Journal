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
    if callsign == "MCC":
        callsign = "CC"
    return callsign

pageCounter = 8
curRow = 0

output_file_name_and_path = "../MISSION_DATA/A14_CM_cleaned.csv"
outputFile = open(output_file_name_and_path, "w")

callsignList = []
lastTimestamp = 0

for curFile in ["as14_CM.csv"]:
    inputFilePath = "../MISSION_DATA/" + curFile
    reader = csv.reader(open(inputFilePath, "rU"), delimiter='|')
    for row in reader:
        curRow += 1
        # if row[1].__len__() > 7:
        # 	print curRow
        # 	print "------------- Page: " + str(pageCounter) + " ::" + row[1]
        time_stamp = row[0] + " " + row[1] + " " + row[2] + " " + row[3]
        # print(row)

        scrubbedCallsign = scrub_callsign(row[4])
        # if not scrubbedCallsign in callsignList:
        #    callsignList.append(scrubbedCallsign)
        #    print "Page: " + str(pageCounter) + " : " + scrubbedCallsign

        curTimestamp = scrub_timestamp(time_stamp).replace(' ', '')
        if not curTimestamp >= lastTimestamp:
            print 'Timestamp out of order: Row: {0} Timestamp: {1}'.format(curRow, time_stamp.replace(" ", "|"))
        lastTimestamp = curTimestamp

        outputLine = '{0}|{1}|{2}\n'.format(scrub_timestamp(time_stamp), scrubbedCallsign, row[5])
            
        outputFile.write(outputLine)
        # print outputLine
outputFile.close()