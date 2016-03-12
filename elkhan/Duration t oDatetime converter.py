
# coding: utf-8

# In[ ]:

import calendar
from datetime import date
import datetime
import sys, traceback
sameDayWords=["TODAY", "TONIGHT", "EVENING"," NOON","AFTERNOON ", "MORNING"," NIGHT","OVERNIGHT", "MIDNIGHT"]#
dayOfWeeks= {"MONDAY":1, "TUESDAY":2, "WEDNESDAY":3, "THURSDAY":4, "FRIDAY":5, "SATURDAY":6, "SUNDAY":7}
expiredWords=["EXPIRED", "EXPIRE", "CANCELED", "CANCELLED"]
# UNTIL 9 PM EDT /8 PM CDT/ SATURDAY
# UNTIL NOON PDT TODAY

# FROM 6 PM (5 PM CDT) THIS EVENING TO 4 PM EDT (3 PM CDT) FRIDAY
# FROM 10 AM TO 4 PM CDT THURSDAY

# FROM 9 AM MDT TUESDAY THROUGH TUESDAY EVENING
# FROM SATURDAY EVENING THROUGH SUNDAY EVENING

# FOR TULSA COUNTY THROUGH TONIGHT
# FOR THIS EVENING THROUGH WEDNESDAY
# FOR MONDAY AND TUESDAY
# FOR TONIGHT HAS BEEN CANCELED

# LATE FRIDAY NIGHT THROUGH SATURDAY EVENING
# THROUGH FRIDAY EVENING

# POSSIBLE TONIGHT AND SATURDAY NIGHT
# IS CANCELLED FOR SUNDAY NIGHT

def containsDayOfWeek(line):
    weekdays=[]
    for dayOfWeek in dayOfWeeks:
        if dayOfWeek in line:
            weekdays.append(dayOfWeek)
    
    if len(weekdays) ==2:
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
    return days

def getRangeDates(dt,weekdaysList):
    dateWeekDay = calendar.day_name[dt.weekday()].upper()
    result = []
    print "Date Range: ", dt, weekdaysList, dateWeekDay
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
        print "\n\n====================== ", weekdaysList , " ===========================\n\n"
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
            return durationDates
        elif len(sameDay) >=1:
            durationDates.append(dt)
            return durationDates
    
    if len(containsExpiredCancelled(line)) > 0 :
        durationDates.append(str(dt) +"\t"+str(containsExpiredCancelled(line)))
        return durationDates
    
    if len(sameDay) > 0 and len(weekdays) == 0:
        durationDates.append(dt)
        return durationDates
    
    if len(weekdays) == 0 and len(sameDay) == 0:
        durationDates.append(dt)
        return durationDates
    
    if untilIndex > -1 :
        if len(weekdays) == 1:
            # add all dates between warning announced date and in effect dates
            # UNTIL 9 PM EDT /8 PM CDT/ SATURDAY
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
        elif len(weekdays) == 0 and len(sameDay) >=1 :
            # UNTIL NOON PDT TODAY
            durationDates.append(dt)
            return durationDates
            
    if fromIndex > -1 and toIndex >-1:
        # FROM 10 AM TO 4 PM CDT THURSDAY
        # FROM 6 PM (5 PM CDT) THIS EVENING TO 4 PM EDT (3 PM CDT) FRIDAY
        if len(sameDay) <= 1 and len(weekdays) == 1:
            # Add all days from today until that weekday
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates        
        # FROM MIDNIGHT TONIGHT TO NOON ON SUNDAY
        elif len(sameDay) >= 1 and len(weekdays) == 1:
            # Add all days from today until that weekday
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates    
        # FROM 1 PM SUNDAY TO 8 PM CDT MONDAY
        elif len(weekdays) == 2:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates    
        
        
    if fromIndex > -1 and throughIndex >-1:   
        # FROM 9 AM MDT TUESDAY THROUGH TUESDAY EVENING
        #print weekdays
        if len(weekdays) == 2 and weekdays[0] == weekdays[1]:
            # Add that day into duration days
            #durationDates.append("Date "+weekdays[0])
            #durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays)
            return durationDates
        elif len(weekdays) == 2:
            # Add all days in the range into duration days
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
        # FROM MIDNIGHT THROUGH 9 AM TUESDAY
        elif  throughIndex > -1 and len(sameDay) > 0 and len(weekdays) > 0 :
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates
        # FROM 1000 AM MST THROUGH 800 PM MST TUESDAY
        elif len(weekdays) == 1 and len(sameDay) ==0:
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return durationDates
      
    
    if fromIndex > -1 and untilIndex >-1: 
        # IN EFFECT FROM 1 PM EST SATURDAY UNTIL 5 AM EDT SUNDAY
        if len(weekdays) == 2:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates

        
        
    if fromIndex >-1:
        #print sameDay,weekdays
        # FROM THIS AFTERNOON AND ON THURSDAY
        if len(sameDay) == 1 and len(weekdays) == 1:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates
        # FROM SATURDAY
        elif len(weekdays) == 1 :
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return durationDates

    if forIndex > -1:
        # FOR THIS EVENING THROUGH WEDNESDAY
        # FOR THIS EVENING THROUGH SUNDAY MORNING
        if len(sameDay) >=1  and throughIndex > -1 and len(weekdays) == 1:
            # Add all days in the range into duration days
            #durationDates.append("Date Range "+str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates
        # FOR TULSA COUNTY THROUGH TONIGHT
        elif len(sameDay) == 0 and throughIndex > -1 and len(weekdays) == 0:
            durationDates.append(dt)
            return durationDates
        # FOR MONDAY AND TUESDAY
        elif andIndex > -1 and len(weekdays) == 2:
            # Add these 2 weekdays into duration days
            #durationDates.append("Date Range "+weekdays[0]+"\t"+weekdays[1])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates2 = getDateOfOneSpecificDay(dt,weekdays[1])
            result = durationDates + durationDates2
            return result
        # FOR FRIDAY MORNING
        elif len(weekdays) == 1:
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return durationDates
        # FOR MONDAY WITH AN EXCESSIVE HEAT WATCH FOR CINCINNATI FOR TUESDAY
        elif len(weekdays) ==2:
            #durationDates.append("Date Range "+weekdays[0]+"\t"+weekdays[1])
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
        # FOR SATURDAY THROUGH MONDAY
        if throughIndex > -1 and len(weekdays) > 1:
            #durationDates.append("Date Range "+weekdays[0]+"\t"+weekdays[1])
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
            
    if throughIndex > -1 and fromIndex == -1 and forIndex== -1 :
        # THROUGH FRIDAY EVENING
        if len(weekdays) == 1:
            # Add that week day into duration days
            #durationDates.append("Date "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return durationDates
        # LATE FRIDAY NIGHT THROUGH SATURDAY EVENING
        elif len(weekdays) == 2:
            # Add all days in the range into duration days
            #durationDates.append("Date Range "+ str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
        
    if andIndex > -1 and (fromIndex == -1 and forIndex== -1 and throughIndex == -1):
        # POSSIBLE TONIGHT AND SATURDAY NIGHT
        # TONIGHT AND TUESDAY MORNING
        if len(sameDay) >= 1 and len(weekdays) ==1:
            # Add that week day also into duration days
            #durationDates.append("Date Range "+weekdays[0])
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            #durationDates.append(dt)
            return durationDates
        elif len(weekdays) == 2:
            # Add all days in the range into duration days
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
    
    # FOR SATURDAY SUNDAY  AND MONDAY
    if andIndex > -1 and fromIndex==untilIndex==toIndex==toIndex==throughIndex:
        if len(weekdays)==3:
            #durationDates.append("Date 3 days:  " + str(weekdays))
            durationDates0 = getDateOfOneSpecificDay(dt,weekdays[0])
            durationDates1 = getDateOfOneSpecificDay(dt,weekdays[1])
            durationDates2 = getDateOfOneSpecificDay(dt,weekdays[2])
            durationDates = durationDates0 + durationDates1 + durationDates2
            return durationDates 
    
    if intoIndex > -1:
        # TONIGHT INTO SATURDAY MORNING
         if len(sameDay) >= 1 and len(weekdays) ==1:
                #durationDates.append("Date " + str(weekdays[0]))
                durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
                #durationDates.append(dt)
                return durationDates
        # INTO EARLY FRIDAY
         elif len(sameDay) == 0 and len(weekdays) == 1:
                #durationDates.append("Date " + str(weekdays[0]))
                durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
                return durationDates
        # THURSDAY AFTERNOON INTO FRIDAY MORNING
         elif len(weekdays) == 2 :
                #durationDates.append("Date Range " + str(weekdays))
                durationDates = getRangeDates(dt,weekdays)
                return durationDates
        
    if toIndex > -1:
        #TONIGHT TO EARLY MONDAY MORNING
        if len(sameDay) >= 1 and len(weekdays) == 1:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates
        # TO 7 AM EDT FRIDAY
        elif len(sameDay) ==0 and len(weekdays) == 1:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            #durationDates.append(dt)
            return durationDates
        # WEDNESDAY NIGHT TO EARLY THURSDAY MORNING FOR
        elif len(weekdays) == 2:
            #durationDates.append("Date Range " + str(weekdays))
            durationDates = getRangeDates(dt,weekdays)
            return durationDates
    
    # WEDNESDAY FROM 10 AM MST THROUGH 7 PM MST
    if len(weekdays) == 1 and line.find(weekdays[0]) < line.find("FROM"):
        #durationDates.append("Date " + str(weekdays[0]))
        durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
        return durationDates
    
    # EARLY MONDAY ACROSS NORTHEAST AND PORTIONS OF EAST CENTRAL NEW MEXICO
    if len(weekdays) == 1 :
        #durationDates.append("Date " + str(weekdays[0]))
        durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
        return durationDates

    if betweenIndex > -1 :
        # THURSDAY BETWEEN 10 AM AND 7 PM MST
        if len(weekdays) == 1:
            #durationDates.append("Date " + str(weekdays[0]))
            durationDates = getDateOfOneSpecificDay(dt,weekdays[0])
            return durationDates
        
    # FROM LATE MONDAY NIGHT INTO TUESDAY MORNING AND TUESDAY NIGHT INTO WEDNESDAY MORNING FOR ALL
    if fromIndex > -1 and intoIndex > -1 and andIndex > -1 and forIndex > -1:
        untilAnd = getwarningDates(dt,line.split("AND")[0])
        afterAnd = getwarningDates(dt,line.split("AND")[1])
        result = untilAnd +  afterAnd
        return result
    
# lineCount = 0
# with open("duration.xml", "r") as myfile:
#     dt = ""
#     line = ""
#     for l in myfile:        
#         lineCount += 1
#         if lineCount % 2 == 1:
#             dt = l
#         else:
#             line=l
#             #print "DATE : ", dt
#             try:
#                 dt = parser.parse(dt.strip())
#             except:
#                 print "Exception: ", l
#                 continue
#             #print "DATE2 : ", dt
#             #print line.strip()
#             result = getwarningDates(dt,line)
#             if result is None:
#                     print lineCount," Could not parse date: ", line
#                     sys.exit(0)
                    
#             #print "\n"


# CHECK FOR CORRECTNESS: FOR EARLY TUESDAY MORNING THROUGH TUESDAY MORNING REMAINS IN EFFECT
lineCount = 0
with open("duration.xml", "r") as myfile:
    dt = datetime.datetime.now()
    line = ""
    for l in myfile:        
        lineCount += 1
        line=l
        #print lineCount, line
        result = getwarningDates(dt,line)
        print line, "\t===\t",result,"\n"
        if result is None or len(result)==0:
            print lineCount," Could not parse date: ", line
            sys.exit(0)
             

