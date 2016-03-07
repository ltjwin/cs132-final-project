
# coding: utf-8

# # Parser for National Weather Service Warning Text
# 
# - Each entity ends with empty line 
# - 1st line 2nd word is unique station identifier "WWUS72 <b>KGSP</b> 260750"
# - Date comes after line containing "National Weather Service"
# - Locations:
# - - Line before contains both '-' and '>' characters
# - - Next line "Including the cities of" , also separated by "..." and the last one by AND
# - Duration : line starts and ends with "..."

# In[ ]:

import os
from datetime import datetime
from dateutil import parser

inputDir = "C:/Users/Ede/Google Drive/2016 Spring/CS132/final/inputdata/"
inputDir = "C:/Users/Ede/Google Drive/CS132 Heat Warning Project/Warnings 2001 to 2011/"
initialLineSkipCount=5;

states =["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS"
         ,"MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA"
         ,"WV","WI","WY","DC"]

# http://www.nws.noaa.gov/mdl/forecast/graphics/common/time.html
timeZones=["EST","CST","MST","PST"]

def containsNum(line):                
    for ch in line:
        if ch.isdigit():
            return True
    return False

def containsLetters(line):                
    for ch in line:
        if ch.isalpha():
            return True
    return False

def containsMoreNumThanChars(line):                
    numCnt=0
    charCnt=0
    for ch in line:
        if ch.isdigit():
            numCnt+=1
        else:
            charCnt+=1
    return numCnt>charCnt

def containsState(line):
    for state in states:
        if state in line:#.split("-"):
            return True
    return False

def allDigits(line):
    for ch in line:
        if not ch.isdigit():
            return False
    return True

for fileName in os.listdir(inputDir):
    if fileName.endswith(".txt"):
        skipCnt=0
        print "----------------------------------- File: ",fileName, "---------------------------------------------------"
        with open(os.path.join(inputDir,fileName)) as f:
            warning={}
            content = f.readlines()[5:]
            print "Total lines: ",len(content)
            warningStartLine=0
            warningEndLine=0
            warningCount = 1
            firstLine = True
            lineNum = -1
            result=[]
            result.append("<file>")
            result.append("\t<file-name>"+fileName+"</file-name>")
            #for lineNum in range(len(content)-1):               
            while lineNum < len(content)-1:               
                lineNum+=1
                line = content[lineNum].strip()
                #print lineNum, " Processing : ",line
                
                if firstLine:
                    stationName = line.split()[1]
                    result.append("\t<entity>")
                    result.append("\t<id>"+str(warningCount)+"</id>")
                    result.append("\t<station>"+stationName+"</station>")
                    print warningCount," Station: ",stationName
                    firstLine= False
                    continue
                
                if "NATIONAL WEATHER SERVICE" == line[0:len("NATIONAL WEATHER SERVICE")]:
                    nws = line
                    result.append("\t<nws>"+nws+"</nws>")
                    print "NWS: ", nws
                    continue
                
                
                if ("EDT" in line or "PDT" in line or "CDT" in line or "MDT" in line) and ("AM" in line or "PM" in line) and "..." not in line and "." not in line:
                    dateOfWarning = line
#                     hourMinute = dateOfWarning.split()[0]
#                     hour=""
#                     minutes=""
#                     if(len(hourMinute)==3):
#                         hour = hourMinute[0]
#                         minutes = hourMinute[1:]
#                     else:
#                         hour = hourMinute[:2]
#                         minutes = hourMinute[2:]
                    dateOfWarning = dateOfWarning.split()[-3:]
                    #print "Last : ",dateOfWarning[-1],allDigits(dateOfWarning[-1])
                    if((not allDigits(dateOfWarning[-1])) or (not allDigits(dateOfWarning[1]))):
                        continue
                    if(len(dateOfWarning[1])>2):
                        dateOfWarning[1]=dateOfWarning[1][0:2]
                    
                    if dateOfWarning[0]=="CDT":
                        continue
                    
                    dateOfWarning = ' '.join(dateOfWarning)
                    print "DT: ",dateOfWarning
                    dt = parser.parse(dateOfWarning)
                    print "Date of Warning: ", dt
                    result.append("\t<date>"+str(dt)+"</date>")
                    #342 AM EDT THU APR 26 2001
                    continue
                    
                
                if "-" in line and containsMoreNumThanChars(line) and ("." not in line and "/" not in line) and containsLetters(line):                  
                    shortCode=line
                    shortCode=shortCode.replace(">","-")
                    shortCode = shortCode.split("-")[0]
                    #print "Short code: ", shortCode
                    result.append("\t<short-code>"+shortCode+"</short-code>")
                    continue
                    
                if containsState(line) and line.count("-")>2 and "..." not in line:
                    locations=""
                    while((containsState(content[lineNum]) or content[lineNum].count("-")>2) and ("INCLUDING THE CITIES OF" not in content[lineNum] and "..." not in content[lineNum])):
                        locations+=content[lineNum].strip()
                        lineNum+=1
                    locs=locations.split("-")
                    locs=locs[:-1]
                    #print "Locations: ",locs 
                    result.append("\t<locations>")
                    for loc in locs:
                        result.append("\t\t<location>"+loc+"</location>")
                    result.append("\t</locations>")
#                     print "Locations LONG: ",locations, 
#                     print "Current : ", content[lineNum]
#                     print "Previous: ",content[lineNum-1]
#                     print "Next : ",content[lineNum+1]
                    lineNum-=1
                    continue
                
                if ("ADVISORY" in line or "WARNING" in line) and "..." in line and " " in line:
                    #print " ------------ ",line.split()[1], line.split()
                    if not ("ADVISORY" == line.split()[1] or "WARNING" == line.split()[1]) :
                        if len(line.split()) >2 and not ("ADVISORY" == line.split()[2] or "WARNING" == line.split()[2]):
                            continue
                        else:
                            continue
                    warningType = line.split(" ")[0] +" "
                    warningType += line.split(" ")[1]
                    duration = line[len(warningType):]
                    duration = duration.replace("...","")
                    warningType = warningType.replace("...","")
                    #print "Warning Type: ", warningType
                    #print "Duration: ", duration
                    result.append("\t<type>"+warningType+"</type>")
                    result.append("\t<duration>"+duration+"</duration>")
                    continue
                
                warningEndLine+=1
                if len(line.strip()) == 0:
                    text = "".join(content[warningStartLine:lineNum])
                    result.append("\t<text>"+text+"\t</text>")
                    result.append("\t</entity>")
                    
                    #lineNum = 0
                    #print "Text: ",text
                    warningStartLine = lineNum+1
                    warningCount+=1
                    firstLine=True
                    print "\n"
                    with open("result.xml", "a") as myfile:
                        for l in result:
                            myfile.write(l+"\n")
                    result=[]
        result.append("</file>")
        with open("result.xml", "a") as myfile:
            for l in result:
                myfile.write(l+"\n")
        result=[]
        #print result
        print "Total Warnings: ",warningCount
        #warningCount=0
        #break


            

