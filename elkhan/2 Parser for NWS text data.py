
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

# In[41]:

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

def getLetterCount(line):
    cnt = 0
    for ch in line:
        if ch.isalpha():
            cnt += 1
    return cnt

def getDigitCount(line):
    cnt = 0
    for ch in line:
        if ch.isdigit():
            cnt += 1
    return cnt

def removeNonAlphaFromStartWarningType(st):
    for i in range(len(st)) :
        if not st[i].isalpha():
            continue
        else:
            break
    return st[i:]

def putCorrectSpacinginWarning(st):
    if st == "MORNINGREACHING ADVISORY":
        return "MORNING REACHING ADVISORY"
    elif st == "MPHBELOW ADVISORY":
        return "MPH BELOW ADVISORY"
    elif st == "CORRECTIONHEAT ADVISORY":
        return "CORRECTION HEAT ADVISORY"
    elif st == "HEADLINEWIND ADVISORY":
        return "HEADLINE WIND ADVISORY"
    else:
        return st
        
def cleanWarningType(st):
    newSt = removeNonAlphaFromStartWarningType(st)
    st = putCorrectSpacinginWarning(newSt)
    return st

def getLocationsFromShortCode(st):
    #NCZ048-051>053-058-059-062>065-262000-
    #print st
    result=[]
    words = st.split("-")
    threeLetters = words[0][:3]
    #OHZ066-067-075-076-WVZ009>011-017>020-028>032-039-040-261200-
    #['OHZ066', 'OHZ067', 'OHZ075', 'OHZ076', 'WVZ009', 'WVZ09', 'WVZ010', 'WVZ011', 'WVZ017', 'WVZ018', 'WVZ019', 'WVZ020', 'WVZ028', 'WVZ029', 'WVZ030', 'WVZ031', 'WVZ032', 'WVZ039', 'WVZ040']
    for i in range(len(words)):
        word = words[i]
        if i==0:
            if ">" not in word:
                result.append(word)
            else:
                #print "WORD: ",word
                word = word[3:]
                rangeWords= word.split(">")
                fromNum = int(rangeWords[0])
                toNum = int(rangeWords[1])
                while fromNum <= toNum:
                    if fromNum < 10:
                        result.append(threeLetters+"00"+str(fromNum))
                    elif fromNum < 100:
                        result.append(threeLetters+"0"+str(fromNum))
                    else:
                        result.append(threeLetters+str(fromNum))
                    fromNum+=1
        elif len(word)==6 and allDigits(word) or len(word.strip())==0:
            break
        elif containsLetters(word):
            threeLetters = word[:3]
            if ">" in word:
                rangeWords= word.split(">")
                fromNum = int(rangeWords[0][3:])
                toNum = int(rangeWords[1])
                while fromNum <= toNum:
                    if fromNum < 10:
                        result.append(threeLetters+"00"+str(fromNum))
                    elif fromNum < 100:
                        result.append(threeLetters+"0"+str(fromNum))
                    else:
                        result.append(threeLetters+str(fromNum))
                    fromNum+=1
            else:
                result.append(word)
        elif ">" in word:
            rangeWords= word.split(">")
            fromNum = int(rangeWords[0])
            toNum = int(rangeWords[1])
            while fromNum <= toNum:
                if fromNum < 10:
                        result.append(threeLetters+"00"+str(fromNum))
                elif fromNum < 100:
                    result.append(threeLetters+"0"+str(fromNum))
                else:
                    result.append(threeLetters+str(fromNum))
                fromNum+=1
        else:
            if len(word) >1:
                result.append(threeLetters+word)
    #print st
    #print result
    return result     
            

uniqueTypes={}
uniqueDurations={}

for fileName in os.listdir(inputDir):
    if fileName.endswith(".txt"):
        skipCnt=0
        #print "----------------------------------- File: ",fileName, "---------------------------------------------------"
        with open(os.path.join(inputDir,fileName)) as f:
            warning={}
            content = f.readlines()[5:]
            #print "Total lines: ",len(content)
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
                    #print warningCount," Station: ",stationName
                    firstLine= False
                    continue
                
                if "NATIONAL WEATHER SERVICE" == line[0:len("NATIONAL WEATHER SERVICE")]:
                    nws = line
                    result.append("\t<nws>"+nws+"</nws>")
                    #print "NWS: ", nws
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
                    #print "DT: ",dateOfWarning
                    dt = parser.parse(dateOfWarning)
                    #print "Date of Warning: ", dt
                    result.append("\t<date>"+str(dt)+"</date>")
                    #342 AM EDT THU APR 26 2001
                    continue
                    
                
                if "-" in line and containsMoreNumThanChars(line) and ("." not in line and "/" not in line) and containsLetters(line):                  
                    shortCode=line.strip()
                    #MDZ001-OHZ039>041-048>050-057>059-068-069-PAZ007>009-013>016-020>023-
                    #029>032-WVZ001>004-012-021>023-041-091242-
                    if getDigitCount(content[lineNum+1]) > getLetterCount(content[lineNum+1]) and "." not in line and "/" not in line:                       
                        while(getDigitCount(content[lineNum+1]) > getLetterCount(content[lineNum+1]) and "." not in content[lineNum+1] and "/" not in content[lineNum+1]):
                            lineNum+=1
                            line = content[lineNum].strip()
                            shortCode += line                           
                        shortCode += line
                        #lineNum -= 1
                    #print "S:",shortCode, "\t===\t",line
                    result.append("\t<short-code>"+shortCode+"</short-code>")
                    locations = getLocationsFromShortCode(shortCode)
                    #shortCode=shortCode.replace(">","-")
                    #shortCode = shortCode.split("-")[0]
                    #print "Short code: ", shortCode
                    #NCZ048-051>053-058-059-062>065-262000-
                    result.append("\t<locations>")
                    for location in locations:
                        result.append("\t\t<location>"+location+"</location>")
                    result.append("\t</locations>")
                    continue
                    
#                 if containsState(line) and line.count("-")>2 and "..." not in line:
#                     locations=""
#                     while((containsState(content[lineNum]) or content[lineNum].count("-")>2) and ("INCLUDING THE CITIES OF" not in content[lineNum] and "..." not in content[lineNum])):
#                         locations+=content[lineNum].strip()
#                         lineNum+=1
#                     locs=locations.split("-")
#                     locs=locs[:-1]
#                     #print "Locations: ",locs 
#                     result.append("\t<locations>")
#                     for loc in locs:
#                         result.append("\t\t<location>"+loc+"</location>")
#                     result.append("\t</locations>")
# #                     print "Locations LONG: ",locations, 
# #                     print "Current : ", content[lineNum]
# #                     print "Previous: ",content[lineNum-1]
# #                     print "Next : ",content[lineNum+1]
#                     lineNum-=1
#                     continue
                
                if ("ADVISORY" in line or "WARNING" in line or "WATCH" in line) and "..." in line[:3] and " " in line and line[-1]!=".":
                    #print " ------------ ",line.split()[1], line.split()
                    if not ("ADVISORY" == line.split()[1] or "WARNING" == line.split()[1] or "WATCH" == line.split()[1]) :
                        if len(line.split()) >2 and not ("ADVISORY" == line.split()[2] or "WARNING" == line.split()[2] or "WATCH" == line.split()[2]):
                            continue
                        #else:
                        #    continue
                    if line[-3:] != "...":
                        lineNum += 1
                        line += " "+content[lineNum].strip()
                        while (line[-3:] != "..." and "..." not in content[lineNum].strip()):
                            lineNum += 1
                            line += " "+content[lineNum].strip()
                    warningType = line.split(" ")[0] +" "
                    warningType += line.split(" ")[1]
                    if "ADVISORY" not in warningType and "WARNING" not in warningType and "WATCH" not in warningType:
                        warningType += " "+line.split(" ")[2]
                    duration = line[len(warningType):]
                    duration = duration.replace("...","")
                    warningType = warningType.replace("...","")
                    #print "Warning Type: ", warningType
                    #print "Duration: ", duration
                    warningType = cleanWarningType(warningType)
                    if warningType not in uniqueTypes:
                        uniqueTypes[warningType]=1
                    
                    result.append("\t<type>"+warningType+"</type>")
                    duration = duration.strip()
                    if len(duration) > 0 :
                        result.append("\t<duration>"+duration+"</duration>")
                        if duration not in uniqueDurations:
                            uniqueDurations[duration]=1
                    
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
                    #print "\n"
                    with open("result.xml", "a") as myfile:
                        for l in result:
                            myfile.write(l+"\n")
                    result=[]
        result.append("</file>")
        with open("result.xml", "a") as myfile:
            for l in result:
                myfile.write(l+"\n")
        result=[]
        #break



print "\n\n--------------------------------------\n\n"        
# for key in uniqueTypes.keys():
#     print key

# for key in uniqueDurations.keys():
#     print key
    
with open("duration.xml", "a") as myfile:
    for l in uniqueDurations:
        myfile.write(l+"\n")    

