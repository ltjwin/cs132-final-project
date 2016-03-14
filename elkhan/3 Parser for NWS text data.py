
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

# In[8]:

import os
from datetime import datetime
from dateutil import parser
import calendar
from datetime import date
import datetime
import sys, traceback


inputDir = "C:/Users/Ede/Google Drive/2016 Spring/CS132/final/inputdata/"
inputDir = "C:/Users/Ede/Google Drive/CS132 Heat Warning Project/Warnings 2001 to 2011/"
initialLineSkipCount=5;

states =["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS"
         ,"MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA"
         ,"WV","WI","WY","DC"]

# http://www.nws.noaa.gov/mdl/forecast/graphics/common/time.html
timeZones=["EST","CST","MST","PST"]



sameDayWords=["TODAY", "TONIGHT", "EVENING"," NOON","AFTERNOON ", "MORNING"," NIGHT","OVERNIGHT", "MIDNIGHT"]#
dayOfWeeks= {"MONDAY":1, "TUESDAY":2, "WEDNESDAY":3, "THURSDAY":4, "FRIDAY":5, "SATURDAY":6, "SUNDAY":7}
expiredWords=["EXPIRED", "EXPIRE", "CANCELED", "CANCELLED"]

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
            

    
# ------------------------------------------------------------------------------------------------------------------
### Converting duration to date code

def containsDayOfWeek(line):
    weekdays=[]
    for dayOfWeek in dayOfWeeks:
        if dayOfWeek in line:
            weekdays.append(dayOfWeek)
#             if line.count(dayOfWeek) ==1:
#                 weekdays.append(dayOfWeek)
#             else:
#                 cnt = line.count(dayOfWeek)
#                 i=0
#                 while i < cnt:
#                     weekdays.append(dayOfWeek)
#                     i+=1
    
    if len(weekdays) == 2:
        if line.find(weekdays[0]) > line.find(weekdays[1]):
            weekdays[0],weekdays[1] = weekdays[1], weekdays[0]
    
    return weekdays

def containsExpiredCancelled(line):
    days=[]
    for day in expiredWords:
        if day in line:
            days.append(day)
    return days

def containsSameDayWord(line):
    days=[]
    for day in sameDayWords:
        if day in line:
            days.append(day)
#             if line.count(day) ==1:
#                 days.append(day)
#             else:
#                 cnt = line.count(day)
#                 i=0
#                 while i < cnt:
#                     days.append(day)
#                     i+=1
    return days

def getRangeDates(dt,weekdaysList):
    dateWeekDay = calendar.day_name[dt.weekday()].upper()
    result = []
    #print "Date Range: ", dt, weekdaysList, dateWeekDay
    if len(weekdaysList) == 1:
        if dateWeekDay != weekdaysList[0]:
            # create dates [dateWeekDay,weekdaysList[0]]
            start = dayOfWeeks[dateWeekDay]
            end = dayOfWeeks[weekdaysList[0]]
            if start > end :
                diff = end + 7 - start
            else:
                diff = end - start
            start = 0
            while(start <= diff ):
                newDt = dt + datetime.timedelta(days=start) 
                result.append(newDt)
                start+=1
            return result
        else:
            result=[]
            result.append(dt)
            return result
    #elif len(weekdaysList) == 2 and weekdaysList[0]==weekdaysList[1]:   
    elif len(weekdaysList) == 2 :
        fromRangeDay =  weekdaysList[0]
        toRangeDay =  weekdaysList[1]
        start = dayOfWeeks[fromRangeDay]
        end = dayOfWeeks[toRangeDay]
        if start > end :
            diff = end + 7 - start
        else:
            diff = end - start
        start = 0
        while(start <= diff ):
            newDt = dt + datetime.timedelta(days=start) 
            result.append(newDt)
            start+=1
        return result
    # FROM MONDAY AFTERNOON THROUGH WEDNESDAY EVENING  ALTHOUGH IT WILL BE HOT THIS AFTERNOON AND AGAIN ON SUNDAY
    elif len(weekdaysList) ==3:
        #print "\n\n====================== ", weekdaysList , " ===========================\n\n"
        fromRangeDay =  weekdaysList[0]
        toRangeDay =  weekdaysList[1]
        start = dayOfWeeks[fromRangeDay]
        end = dayOfWeeks[toRangeDay]
        if start > end :
            diff = end + 7 - start
        else:
            diff = end - start
        start = 0
        while(start <= diff ):
            newDt = dt + datetime.timedelta(days=start) 
            result.append(newDt)
            start+=1
        newDt = getDateOfOneSpecificDay(dt,weekdaysList[2])
        result.append(newDt)
        return result

def getDateOfOneSpecificDay(dt,weekDay):
    result = []
    dateWeekDay = calendar.day_name[dt.weekday()].upper()
    dateWeekDayInt = dayOfWeeks[dateWeekDay] 
    weekDayInt = dayOfWeeks[weekDay]
    if dateWeekDayInt > weekDayInt :
        diff = weekDayInt + 7 - dateWeekDayInt
    else:
        diff = dateWeekDayInt - weekDayInt
    newDt = dt + datetime.timedelta(days=diff) 
    result.append(newDt)
    return result
    
def getwarningDates(dt,line):
    durationDates=[]
    warningDtWeekDay = calendar.day_name[dt.weekday()].upper()
    
    fromIndex = line.find("FROM")
    untilIndex = line.find("UNTIL")
    toIndex = line.find("TO")
    throughIndex = line.find("THROUGH")
    forIndex =  line.find("FOR")
    andIndex = line.find("AND")
    intoIndex = line.find("INTO")
    betweenIndex = line.find("BETWEEN")
    
    weekdays = containsDayOfWeek(line)
    expiredwords = containsExpiredCancelled(line)
    sameDay = containsSameDayWord(line)
#     print "\tWeekdays: ", weekdays
#     print "\tSameDay: ", sameDay
#     print "\tExpiredwords: ", expiredwords
    
    if "SATURDAYSUNDAY" in line:
        durationDates.append("SATURDAYSUNDAY")
        return durationDates
    
    # MONDAY MORNING
    if fromIndex==untilIndex==toIndex==toIndex==throughIndex==forIndex==andIndex:
        if len(weekdays)==1:
            #durationDates.append(weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return [durationDates,""]
        elif len(sameDay) >=1:
            durationDates.append(dt)
            return [durationDates,""]
    
    if len(containsExpiredCancelled(line)) > 0 :
        #durationDates.append(str(dt) +"\t"+str(containsExpiredCancelled(line)))
        durationDates.append(dt)
        return [durationDates,containsExpiredCancelled(line)]
    
    if len(sameDay) > 0 and len(weekdays) == 0:
        durationDates.append(dt)
        return [durationDates,""]
    
    if len(weekdays) == 0 and len(sameDay) == 0:
        durationDates.append(dt)
        return [durationDates,""]
    
    if untilIndex > -1 :
        if len(weekdays) == 1:
            # add all dates between warning announced date and in effect dates
            # UNTIL 9 PM EDT /8 PM CDT/ SATURDAY
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
        elif len(weekdays) == 0 and len(sameDay) >=1 :
            # UNTIL NOON PDT TODAY
            durationDates.append(dt)
            return [durationDates,""]
            
    if fromIndex > -1 and toIndex >-1:
        # FROM 10 AM TO 4 PM CDT THURSDAY
        # FROM 6 PM (5 PM CDT) THIS EVENING TO 4 PM EDT (3 PM CDT) FRIDAY
        if len(sameDay) <= 1 and len(weekdays) == 1:
            # Add all days from today until that weekday
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # FROM MIDNIGHT TONIGHT TO NOON ON SUNDAY
        elif len(sameDay) >= 1 and len(weekdays) == 1:
            # Add all days from today until that weekday
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # FROM 1 PM SUNDAY TO 8 PM CDT MONDAY
        elif len(weekdays) == 2:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]   
        
        
    if fromIndex > -1 and throughIndex >-1:   
        # FROM 9 AM MDT TUESDAY THROUGH TUESDAY EVENING
        #print weekdays
        if len(weekdays) == 2 and weekdays[0] == weekdays[1]:
            # Add that day into duration days
            #durationDates.append("Date "+weekdays[0])
            #durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays)
            return [durationDates,""]
        elif len(weekdays) == 2:
            # Add all days in the range into duration days
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
        # FROM MIDNIGHT THROUGH 9 AM TUESDAY
        elif  throughIndex > -1 and len(sameDay) > 0 and len(weekdays) > 0 :
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # FROM 1000 AM MST THROUGH 800 PM MST TUESDAY
        elif len(weekdays) == 1 and len(sameDay) ==0:
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return [durationDates,""]
      
    
    if fromIndex > -1 and untilIndex >-1: 
        # IN EFFECT FROM 1 PM EST SATURDAY UNTIL 5 AM EDT SUNDAY
        if len(weekdays) == 2:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]

        
        
    if fromIndex >-1:
        #print sameDay,weekdays
        # FROM THIS AFTERNOON AND ON THURSDAY
        if len(sameDay) == 1 and len(weekdays) == 1:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # FROM SATURDAY
        elif len(weekdays) == 1 :
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return [durationDates,""]

    if forIndex > -1:
        #print "-- entred forIndex"
        # FOR THIS EVENING THROUGH WEDNESDAY
        # FOR THIS EVENING THROUGH SUNDAY MORNING
        # FOR EARLY TUESDAY MORNING THROUGH TUESDAY MORNING REMAINS IN EFFECT
        if len(sameDay) >=1  and throughIndex > -1 and len(weekdays) == 1:
            #print "len(sameDay) >=1  and throughIndex > -1 and len(weekdays) == 1"
            # Add all days in the range into duration days
            #durationDates.append("Date Range "+str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # FOR TULSA COUNTY THROUGH TONIGHT
        elif len(sameDay) == 0 and throughIndex > -1 and len(weekdays) == 0:
            #print "len(sameDay) == 0 and throughIndex > -1 and len(weekdays) == "
            durationDates.append(dt)
            return [durationDates,""]
        # FOR MONDAY AND TUESDAY
        elif andIndex > -1 and len(weekdays) == 2:
            #print "andIndex > -1 and len(weekdays) == 2"
            # Add these 2 weekdays into duration days
            #durationDates.append("Date Range "+weekdays[0]+"\t"+weekdays[1])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates2 = getDateOfOneSpecificDay(dt,weekdays[1])
            result = durationDates + durationDates2
            return [result,""]
        # TONIGHT AND THURSDAY MORNING FOR
        elif len(weekdays) == 1 and andIndex > -1 and len(sameDay) >=1 :
            #print "len(weekdays) == 1 and andIndex > -1 and len(sameDay) ==1 and len(weekdays) ==1"
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates.append(dt)
            return [durationDates,""]
        # FOR FRIDAY MORNING
        elif len(weekdays) == 1:
            #print "len(weekdays) == 1"
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return [durationDates,""]
        # FOR MONDAY WITH AN EXCESSIVE HEAT WATCH FOR CINCINNATI FOR TUESDAY
        elif len(weekdays) ==2:
            #print "len(weekdays) ==2"
            #durationDates.append("Date Range "+weekdays[0]+"\t"+weekdays[1])
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
        # FOR SATURDAY THROUGH MONDAY
        if throughIndex > -1 and len(weekdays) > 1:
            #durationDates.append("Date Range "+weekdays[0]+"\t"+weekdays[1])
            #print "throughIndex > -1 and len(weekdays) > 1"
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
        # FOR MOST OF CENTRAL AND SOUTHERN ARKANSAS THURSDAY AND FRIDAY   AFTERNOON HEAT INDEX 105 TO 110 THURSDAY AND FRIDAY
        if andIndex > -1 and len(weekdays) ==2:
            durationDates0 = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates1 = getDateOfOneSpecificDay(dt,weekdays[1])
            durationDates = durationDates0 + durationDates1
            return [durationDates,""] 
            
    if throughIndex > -1 and fromIndex == -1 and forIndex== -1 :
        # THROUGH FRIDAY EVENING
        if len(weekdays) == 1:
            # Add that week day into duration days
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return [durationDates,""]
        # LATE FRIDAY NIGHT THROUGH SATURDAY EVENING
        elif len(weekdays) == 2:
            # Add all days in the range into duration days
            #durationDates.append("Date Range "+ str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
        
    if andIndex > -1 and (fromIndex == -1 and forIndex== -1 and throughIndex == -1):
        # POSSIBLE TONIGHT AND SATURDAY NIGHT
        # TONIGHT AND TUESDAY MORNING
        if len(sameDay) >= 1 and len(weekdays) ==1:
            # Add that week day also into duration days
            #durationDates.append("Date Range "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            #durationDates.append(dt)
            return [durationDates,""]
        elif len(weekdays) == 2:
            # Add all days in the range into duration days
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
    
    # FOR SATURDAY SUNDAY  AND MONDAY
    if andIndex > -1 and fromIndex==untilIndex==toIndex==toIndex==throughIndex:
        if len(weekdays)==3:
            #durationDates.append("Date 3 days:  " + str(weekdays))
            durationDates0 = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates1 = getDateOfOneSpecificDay(dt,weekdays[1])
            durationDates2 = getDateOfOneSpecificDay(dt,weekdays[2])
            durationDates = durationDates0 + durationDates1 + durationDates2
            return [durationDates,""]
    
    if intoIndex > -1:
        # TONIGHT INTO SATURDAY MORNING
         if len(sameDay) >= 1 and len(weekdays) ==1:
                #durationDates.append("Date " + str(weekdays[0]))
                durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
                #durationDates.append(dt)
                return [durationDates,""]
        # INTO EARLY FRIDAY
         elif len(sameDay) == 0 and len(weekdays) == 1:
                #durationDates.append("Date " + str(weekdays[0]))
                durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
                return [durationDates,""]
        # THURSDAY AFTERNOON INTO FRIDAY MORNING
         elif len(weekdays) == 2 :
                #durationDates.append("Date Range " + str(weekdays))
                durationDates = getRangeDates(dt,weekdays)
                return [durationDates,""]
        
    if toIndex > -1:
        #TONIGHT TO EARLY MONDAY MORNING
        if len(sameDay) >= 1 and len(weekdays) == 1:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # TO 7 AM EDT FRIDAY
        elif len(sameDay) ==0 and len(weekdays) == 1:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return [durationDates,""]
        # WEDNESDAY NIGHT TO EARLY THURSDAY MORNING FOR
        elif len(weekdays) == 2:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return [durationDates,""]
    
    # WEDNESDAY FROM 10 AM MST THROUGH 7 PM MST
    if len(weekdays) == 1 and line.find(weekdays[0]) < line.find("FROM"):
        #durationDates.append("Date " + str(weekdays[0]))
        durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
        return [durationDates,""]
    
    # EARLY MONDAY ACROSS NORTHEAST AND PORTIONS OF EAST CENTRAL NEW MEXICO
    if len(weekdays) == 1 :
        #durationDates.append("Date " + str(weekdays[0]))
        durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
        return [durationDates,""]

    if betweenIndex > -1 :
        # THURSDAY BETWEEN 10 AM AND 7 PM MST
        if len(weekdays) == 1:
            #durationDates.append("Date " + str(weekdays[0]))
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return [durationDates,""]
        
    # FROM LATE MONDAY NIGHT INTO TUESDAY MORNING AND TUESDAY NIGHT INTO WEDNESDAY MORNING FOR ALL
    if fromIndex > -1 and intoIndex > -1 and andIndex > -1 and forIndex > -1:
        untilAnd = getwarningDates(dt,line.split("AND")[0])
        afterAnd = getwarningDates(dt,line.split("AND")[1])
        result = untilAnd +  afterAnd
        return [result,""]

# ------------------------------------------------------------------------------------------------------------------------------------------------------
    
uniqueTypes={}
uniqueDurations={}
uniqueDurationsList=[]
dateOfWarning=""
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
                    hourMinute = dateOfWarning.split()[0]
                    hour=""
                    minutes=""
                    if(len(hourMinute)==3):
                        hour = hourMinute[0]
                        minutes = hourMinute[1:]
                    else:
                        hour = hourMinute[:2]
                        minutes = hourMinute[2:]
                    
                    if len(minutes) ==0:
                        minutes ="0"
                    dateOfWarning = dateOfWarning.split()[-3:]
                    #print "Last : ",dateOfWarning[-1],allDigits(dateOfWarning[-1])
                    if((not allDigits(dateOfWarning[-1])) or (not allDigits(dateOfWarning[1]))):
                        dateOfWarning = ""
                        continue
                    if(len(dateOfWarning[1])>2):
                        dateOfWarning[1]=dateOfWarning[1][0:2]
                    
                    if dateOfWarning[0]=="CDT":
                        dateOfWarning = ""
                        continue
                    
                    dateOfWarning = ' '.join(dateOfWarning)
                    #print "DT: ",dateOfWarning
                    if allDigits(hour) and allDigits(minutes):
                        dateOfWarning = hour + ":" + minutes + " "+dateOfWarning
                    #print dateOfWarning, "\tLine: ",line
                    dt = parser.parse(dateOfWarning)
                    #print "Date of Warning: ", dt
                    dateOfWarning = dt
                    #print lineNum, line, dateOfWarning
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
                
                if ("ADVISORY" in line or "WARNING" in line or "WATCH" in line or "FREEZING TEMPERATURES" in line) and "..." in line[:3] and " " in line and (line[-1]!="." or line[-3:]=="..."):
                    #print " ------------ ",line
                    if "FREEZING TEMPERATURES" not in line:
                        if not ("ADVISORY" == line.split()[1] or "WARNING" == line.split()[1] or "WATCH" == line.split()[1]) :
                            if len(line.split()) >2 and not ("ADVISORY" == line.split()[2] or "WARNING" == line.split()[2] or "WATCH" == line.split()[2]):
                                if len(line.split()) >3 and not ("ADVISORY" == line.split()[3] or "WARNING" == line.split()[3] or "WATCH" == line.split()[3]):
                                    if len(line.split()) >4 and not ("ADVISORY" == line.split()[4] or "WARNING" == line.split()[4] or "WATCH" == line.split()[4]):
                                        continue
                        #else:
                        #    continue
                    
                    if line == "...WATCHES AND WARNINGS...":
                        continue
                    if line[-3:] != "..." :#: or ("AND" in content[lineNum+1] and "..." in content[lineNum+1] and content[lineNum+1].find("AND") < content[lineNum+1].find("...")):
                        lineNum += 1
                        line += " "+content[lineNum].strip()
                        while (line[-3:] != "..." and "..." not in content[lineNum].strip() and "." not in line) :#or ("AND" in content[lineNum+1] and "..." in content[lineNum+1]):
                            lineNum += 1
                            line += " "+content[lineNum].strip()
                    warningType = line.split(" ")[0] +" "
                    warningType += line.split(" ")[1]
                    i=2
                    while "ADVISORY" not in warningType and "WARNING" not in warningType and "WATCH" not in warningType and "FREEZING TEMPERATURES" not in warningType:
                        warningType += " "+line.split(" ")[i]
                        i+=1
                    duration = line[len(warningType):]
                    duration = duration.replace("..."," ")
                    warningType = warningType.replace("..."," ")
                    #print "Warning Type: ", warningType
                    #print "Duration: ", duration
                    warningType = cleanWarningType(warningType)
                    if warningType not in uniqueTypes:
                        uniqueTypes[warningType]=1
                    
                    result.append("\t<type>"+warningType+"</type>")
                    duration = duration.strip()
                    if len(duration) > 0 :
                        if len(str(dateOfWarning)) == 0:
                            continue
                        result.append("\t<duration>"+duration+"</duration>")
                        #print lineNum, " DatOfWarning: ",dateOfWarning,"Duration: ", duration, "Line: ", line
                        dateResult = getwarningDates(dateOfWarning,duration)
                        dates = sorted(dateResult[0])
                        cancelled = dateResult[1]
                        result.append("\t<duration-dates>")
                        if len(cancelled) > 0:
                            result.append("\t\t<duration-date>"+ str(dates) +"</duration-date>")
                            result.append("\t</duration-dates>")
                            result.append("\t<cancelled>"+ str(1) +"</cancelled>")
                        else:
                            for t in dates:
                                result.append("\t\t<duration-date>"+ str(t) +"</duration-date>")
                            result.append("\t</duration-dates>")
                            result.append("\t<cancelled>"+ str(0) +"</cancelled>")
                        if duration not in uniqueDurations:
                            uniqueDurations[duration]=1
                            #uniqueDurationsList.append(dateOfWarning);
                            uniqueDurationsList.append(duration);
                    
                    #print "Warning Type: ",warningType
                    #print "Duration: ",duration
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
    for l in uniqueDurationsList:
        myfile.write(str(l)+"\n")    


# In[17]:

print "\n\n--------------------------------------\n\n"        
print "Total different warning Types: ", len(uniqueTypes.keys())
for key in uniqueTypes.keys():
    print key


# In[27]:

for l in uniqueDurationsList:
    if "THROUGH" in str(l):
        print l

