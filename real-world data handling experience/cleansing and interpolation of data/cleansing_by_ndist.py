import matplotlib.pyplot as plt
import numpy as np
import os
import datetime
from scipy import stats

def readfile(fileName):
    try : 
        f = open(fileName, 'r', encoding="utf-8")
        g = f.readlines()
    except UnicodeDecodeError : 
        f = open(fileName, 'r', encoding='cp949')
        g = f.readlines()

    f.close()
    data = []

    sDate = datetime.datetime(2015,1,1)
    deltaT = datetime.timedelta(hours=1)

    for day in g[1:] :
        temp = day.strip().split()
        temp2 = ' '.join([sDate.date().isoformat(), sDate.time().isoformat()])
        colNum = len(temp)

        for i in range(3, colNum) :
            try:
                temp3 = float(temp[i])
                if temp3 < 0 :
                    temp[i] = 0
                else :
                    temp[i] = temp3
            except ValueError:
                temp[i] = 0.0
        temp = [temp2] + temp[3:]
        data.append(temp)
        sDate += deltaT
    head = g[0].strip().split()
    head = head[2:]
    return [head, data]
    # head : ['시간', building nums in order]
    # data : [date&time, electricity usage of each building]


def transpose (array) :
    return [list(x) for x in zip(*array)]

def indexCheck(x, rawData): # check whether an index is within the range of the given data
    start = 0
    end = len(rawData[1]) #should be changed according to the size of the given dataset
    if start <= x < end : return True
    else : return False

def cleanse(rawData, bldIndex, length=0, startDate= datetime.date(2015,1,1)) :
    #rawData is the result tuple of readfile function (['시간', 1, 2, ...], ['2015-01-01 00:00:00', 30.0, 47.0 ..,])
    #limitType : 1 - quartile type // 2 - normal dist, 95% // 3 - normal dist, 99% // 4 - t dist, 95% // 5 - t dist, 99%
    res = []
    if length==0 :length = len(rawData[1]) #total
    current = (startDate - datetime.date(2015,1,1)).days * 24 #hourly index
    count = 0
    firstTryYearlySet = [-1, 0, 1, -25, -24, -23, 23, 24, 25] # +- 1 day, +- 1 hour
    #firstTryYearlyWeekendSet = [-1, 0, 1, -169, -168,-167, 167, 168, 169]
    secondTryYearlySet = [-169, -168, -167, 167, 168, 169] # += 1 week, +- 1 hour
    #secondTryYearlyWeekendSet = [-25, -24, -23, 23, 24, 25]
    year = 364 * 24 #why not 365*24? because keeping the same "day" in a week is much more important


    while current < length :
        hourlyRes = [rawData[1][current][0], round(rawData[1][current][bldIndex], 1)] # extracting buildingwise elec usage for each hour

        currentYearFirstTry = [current + x for x in firstTryYearlySet]
        previousYearFirstTry = [current - year + x for x in firstTryYearlySet]
        nextYearFirstTry = [current + year + x for x in firstTryYearlySet]
        doublePreviousYearFirstTry = [current - 2*year + x for x in firstTryYearlySet]

        sampleSetList = [x for x in currentYearFirstTry + previousYearFirstTry + nextYearFirstTry + doublePreviousYearFirstTry if indexCheck(x, rawData)] #save valid indices
        sampleSetList.remove(current) #drop the current hourly usage value

        #use only positive usage values
        sampleValue = [rawData[1][x][bldIndex] for x in sampleSetList if rawData[1][x][bldIndex] > 0]


        if len(sampleValue) < 10 : #gathering more samples if the whole number is below 10 to guarantee the minimum confidence
            currentYearSecondTry = [current + y for y in secondTryYearlySet]
            previousYearSecondTry = [current - year + y for y in secondTryYearlySet]
            nextYearSecondTry = [current + year + y for y in secondTryYearlySet]
         #   doublePreviousYearSecondTry = [current - 2*year + y for y in secondTryYearlySet]

            sampleSetList = [x for x in currentYearSecondTry + previousYearSecondTry + nextYearSecondTry if indexCheck(x, rawData)]
            sampleValue += [rawData[1][x][bldIndex] for x in sampleSetList if rawData[1][x][bldIndex] > 0]


        if len(sampleValue) < 2 : #sample set with a single value -> do nothing
            hourlyRes += ["", "", "lack"]

        else :
            sampleMean = np.mean(sampleValue)
            sampleMedian = np.median(sampleValue)

            # limitType : 1 - quartile type // 2 - normal dist, 95% // 3 - normal dist, 99% // 4 - t dist, 95% // 5 - t dist, 99%

            #if limitType == 1 :
            #    thirdQuartile = np.percentile(sampleValue, 75)
            #    firstQuartile = np.percentile(sampleValue, 25)
            #    IQR = thirdQuartile - firstQuartile
            #    upperLim = thirdQuartile + 1.5*IQR
            #    lowerLim = firstQuartile - 1.5*IQR

            #else :

            sampleStd = np.std(sampleValue, ddof=1)
            numOfSample = len(sampleValue)
            sqrtOfNum = np.sqrt(numOfSample)

            #if limitType == 2 :
            #    halfOfInterval = -stats.norm.ppf(0.025) * (1 + 1/sqrtOfNum)*sampleStd
            #    upperLim = sampleMean + halfOfInterval
            #    lowerLim = sampleMean - halfOfInterval

            #if limitType == 3 :
            #    halfOfInterval = -stats.norm.ppf(0.005) * (1 + 1 / sqrtOfNum) * sampleStd
            #    upperLim = sampleMean + halfOfInterval
            #    lowerLim = sampleMean - halfOfInterval

            #if limitType == 4 : #degree of freedom : numOfSample-1
            #halfOfInterval = -stats.t.ppf(0.025, numOfSample-1) * (1 + 1/sqrtOfNum) * sampleStd
            #upperLim = sampleMean + halfOfInterval
            #lowerLim = sampleMean - halfOfInterval

            #if limitType == 5 :
            halfOfInterval = -stats.t.ppf(0.01, numOfSample-1) * (1 + 1/sqrtOfNum) * sampleStd
            upperLim = sampleMean + halfOfInterval
            lowerLim = sampleMean - halfOfInterval

            hourlyRes.append(round(lowerLim,1))
            hourlyRes.append(round(upperLim,1))
            if lowerLim <= hourlyRes[1] <= upperLim and hourlyRes[1]!=0:
                hourlyRes.append("")
                # hourlyRes.append(len(sampleValue))
                hourlyRes.append(round(sampleMean, 1))
                hourlyRes.append(round(sampleMedian, 1))
            else :
                hourlyRes.append("abnormal")
                # hourlyRes.append(len(sampleValue))
                hourlyRes.append(round(sampleMean, 1))
                hourlyRes.append(round(sampleMedian, 1))

        res.append(hourlyRes)
        count += 1
        current += 1
    #    if current%1000==0 : print(current)

        #print(bldIndex)
        #if bldIndex > 1 : break

    return res


rawHourly = readfile("updatedRaw.txt")
print(rawHourly[1][0])
#rawHourly[1] = rawHourly[1][:-4]


numOfBlds = len(rawHourly[0])
# lengthOfHours = len(hourlyData[0])
# cumMonthDates = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334,
#                  365, 396, 425, 456, 486, 517, 547, 578, 609, 639, 670,
#                  700, 731, 762, 790, 821, 851, 882, 912, 943, 974, 1004,
#                  1035, 1065, 1096, 1127, 1155]
# cumMonthHours = [x*24 for x in cumMonthDates]
# cumMonthNames = ['15/1', '15/2', '15/3', '15/4', '15/5', '15/6', '15/7', '15/8', '15/9', '15/10', '15/11', '15/12',
#                  '16/1', '16/2', '16/3', '16/4', '16/5', '16/6', '16/7', '16/8', '16/9', '16/10', '16/11', '16/12',
#                  '17/1', '17/2', '17/3', '17/4', '17/5', '17/6', '17/7', '17/8', '17/9', '17/10', '17/11', '17/12',
#                  '18/1', '18/2', '18/3']
# weekDates = np.linspace(0,1186,7)
# typeName = ['IQR', 'NDist95', 'NDist99', 'TDist95', 'TDist99']


def aggregateCleansing (fullData, bldIndex) :
    #fullData is the whole result of readfile function
    #typeName = ['IQR', 'NDist95', 'NDist99', 'TDist95', 'TDist99']
    head = ['dateTime', 'initialValue', 'lowerLim', 'upperLim', 'check', 'meanSubst', 'medianSubst']
    bldNum = fullData[0][bldIndex]

    cleansed = cleanse(fullData, bldIndex, startDate=datetime.date(2018,7,1))
    cleansed.insert(0, head)
    g = open('ci98_first/'+'bld'+bldNum+'_cleansed'+'.txt', 'w')
    for line in cleansed :
        g.write('\t'.join([str(x) for x in line]))
        g.write('\n')
    g.close()

for i in range(1, numOfBlds):
    aggregateCleansing(rawHourly, i)
    print(rawHourly[0][i])