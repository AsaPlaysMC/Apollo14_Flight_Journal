import csv
import sys 
import re
import datetime


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


def append_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    
    newLine = lines[line_num].replace('\n', '')
    newLine += " " + text + "\n"
    lines[line_num] = newLine
    
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()  

pageCounter = 8
curReadRow = 0
curWriteRow = 0
lastLineIsTapeTitle = 0

output_file_name_and_path = "../MISSION_DATA/A14_CM_cleaned_phase2.csv"
outputFile = open(output_file_name_and_path, "w")
outputFile.write('')
outputFile.close()

callsignList = []
lastTimestamp = 0
lastTimestampStr = "00 00 00 00"
outputLine = ""

inputFilePath = "../MISSION_DATA/A14_CM_cleaned.csv"
reader = csv.reader(open(inputFilePath, "rU"), delimiter='|')
for row in reader:
    outputFile = open(output_file_name_and_path, "a")
    curReadRow += 1
    curTimestamp = row[0].replace(' ', '')
    if not curTimestamp >= lastTimestamp:
        print 'Timestamp out of order: Page{0} Timestamp:{1}'.format(pageCounter, row[0])
    lastTimestamp = curTimestamp
    # print GETFromTimestamp(row[0])
    outputLine = '{0}|{1}|{2}\n'.format(GETFromTimestamp(row[0]), row[1], row[2])
    outputFile.write(outputLine)
    curWriteRow += 1
    # print outputLine
outputFile.close()
