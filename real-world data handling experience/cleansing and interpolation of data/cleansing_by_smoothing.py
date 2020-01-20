
# coding: utf-8
import copy
import statistics as stat

def readfileVer1(fileName):
    try :
        f = open(fileName, 'r', encoding='cp949')
    except UnicodeDecodeError :
        f= open(fileName, 'r', encoding='utf-8')
    g = f.readlines()
    f.close()
    data = []


    for hour in g[1:] :
        temp = hour.strip().split('\t')
        colNum = len(temp)
        temp[0] = int(temp[0])
        temp[1] = int(temp[1])
        temp[2] = int(temp[2])

        for i in range(3, colNum) :
            try:
                temp2 = float(temp[i])
                if temp2 < 0 :
                    temp[i] = 0
                else :
                    temp[i] = temp2
            except ValueError:
                temp[i] = 0.0

        data.append(temp)

    head = g[0].strip().split('\t')

    return head, data
    # head : ['날짜', '시간','요일', building nums in order]
    # data : [dateNum,hourNum, dayNum, electricity usage of each building]

#index1 : the index of each row
#index2 : the column index of each building
#var : average of absolute variance of a building
#times : the norm of range by variance that is used for determining error values.

#오류 데이터 수집
def collect_wrong(array, index2, var, times, startDate=1, endDate=0):
    wrong = []
    if endDate == 0 :
        endDate = len(array)
    else :
        endDate = endDate * 24 - 24
    count = startDate * 24 - 24

    while count < endDate :
        if value_check(count, index2, array, var, times) : pass
        else:
            temp = copy.deepcopy(array[count][0:3])
            temp.append(array[count][index2])
            temp.insert(0, count)
            wrong.append(temp)
        count += 1
    return wrong
    #[hourIndex, date&time, dayNum, wrongValueOfIndex2]


def value_check(index1, index2, array, var, times):
    num = len(array)
    varTimes = var*times
    checkValue = array[index1][index2]
    if checkValue == 0 : return False
    elif index1 > 0 and index1 < num : 
        backIndex = index1-1 # forthIndex = index1+1
        backValue = array[backIndex][index2]  #forthValue = array[forthIndex][index2]
        if abs(backValue-checkValue) > varTimes : return False
        else : return True
    else : return True


def variance(array, index2):
    count = 0
    sumData = 0
    for hour in array[1:]:
        sumData += abs(array[count][index2]-hour[index2])


        count += 1
    return sumData/(len(array)-1)


def error_count(array, index2, var, times, startDate=1, endDate=0) :
    err = 0
    if endDate == 0 : endDate = len(array)
    else : endDate = endDate * 24 - 24
    count = startDate * 24 - 24
    length = endDate - count
	
    while count < endDate :
        if value_check(count, index2, array, var, times) : pass
        else : err += 1
        count += 1
    
    return err, err/length

def interpolate_linear(originalArray, wrongArray, index2) :
    wrongIndex = [hour[0] for hour in wrongArray]
    startIndex = 0 + 1
    endIndex = len(originalArray) -1

    for index in wrongIndex :
        if index in range(startIndex, endIndex) :
            backIndex = index - 1
            forthIndex = index + 1
            if backIndex in wrongIndex or forthIndex in wrongIndex : pass
            else :
                originalArray[index][index2] = 0.5*(originalArray[backIndex][index2]+originalArray[forthIndex][index2])


def interpolate_linear_yearLeap(originalArray, wrongArray, index2) :
    wrongIndex = [hour[0] for hour in wrongArray]
    startIndex = 0 + 1
    endIndex = len(originalArray) -1

    for index in wrongIndex :
        if index in range(startIndex, endIndex) :
            backIndex = index - 364*24 -1
            forthIndex = index - 364*24 +1
            if backIndex in wrongIndex or forthIndex in wrongIndex : pass
            else :
                originalArray[index][index2] = 0.5*(originalArray[backIndex][index2]+originalArray[forthIndex][index2])


def _week_based_yearLeap(array, index1, index2, weekN, var, times):
    changedValue = array[index1][index2]  # 원데이터에서 날짜 & 시간
    maxN = len(array)  # 끝날짜 인덱스
    minN = 0  # 첫째날짜 인덱스
    plusPairs = []
    minusPairs = []  # plus는 뒷날, minus는 앞날
    for i in range(1, weekN + 1):  # weekN은 앞뒤 몇 주간의 데이터를 활용할 것인가 하는 것!
        temp = i * 168  # 실제 인덱스에 더하거나 뺄 값
        plusTemp = index1 + temp -8736
        minusTemp = index1 - temp -8736
        # 2의 제곱으로 가중치를 부여:가까운 건 높게, 먼 건 낮게
        if plusTemp < maxN and value_check(plusTemp, index2, array, var, times):
            plusPairs.append((array[plusTemp][index2], 2 ** (weekN - i)))
        if minusTemp > minN and value_check(minusTemp, index2, array, var, times):
            minusPairs.append((array[minusTemp][index2], 2 ** (weekN - i)))
    if len(plusPairs) * len(minusPairs) == 0:
        return changedValue  # 플러스와 마이너스가 최소 1개씩은 있어야 함
    else:
        # print(array[index1][index2])
        # print(plusPairs, minusPairs)
        sumN = sum([j for i, j in plusPairs]) + sum([j for i, j in minusPairs])
        total = sum([i * j for i, j in plusPairs]) + sum([i * j for i, j in minusPairs])
        changedValue = total / sumN  # 가중평균 구해서 토해냄
        return changedValue


def interpolate_week_yearLeap(originalArray, wrongArray, index2, weekN, var, times):

    wrongIndex = [hour[0] for hour in wrongArray]
    
    for index in wrongIndex : 
        originalArray[index][index2] = _week_based_yearLeap(originalArray, index, index2, weekN, var, times)



#only for interpolate_weeks function
def _week_based(array, index1, index2, weekN, var, times):
    changedValue = array[index1][index2]  # 원데이터에서 날짜 & 시간
    maxN = len(array)  # 끝날짜 인덱스
    minN = 0  # 첫째날짜 인덱스
    plusPairs = []
    minusPairs = []  # plus는 뒷날, minus는 앞날
    for i in range(1, weekN + 1):  # weekN은 앞뒤 몇 주간의 데이터를 활용할 것인가 하는 것!
        temp = i * 168  # 실제 인덱스에 더하거나 뺄 값
        plusTemp = index1 + temp
        minusTemp = index1 - temp
        # 2의 제곱으로 가중치를 부여:가까운 건 높게, 먼 건 낮게
        if plusTemp < maxN and value_check(plusTemp, index2, array, var, times):
            plusPairs.append((array[plusTemp][index2], 2 ** (weekN - i)))
        if minusTemp > minN and value_check(minusTemp, index2, array, var, times):
            minusPairs.append((array[minusTemp][index2], 2 ** (weekN - i)))
    if len(plusPairs) * len(minusPairs) == 0:
        return changedValue  # 플러스와 마이너스가 최소 1개씩은 있어야 함
    else:
        # print(array[index1][index2])
        # print(plusPairs, minusPairs)
        sumN = sum([j for i, j in plusPairs]) + sum([j for i, j in minusPairs])
        total = sum([i * j for i, j in plusPairs]) + sum([i * j for i, j in minusPairs])
        changedValue = total / sumN  # 가중평균 구해서 토해냄
        return changedValue


def interpolate_week(originalArray, wrongArray, index2, weekN, var, times):

    wrongIndex = [hour[0] for hour in wrongArray]
    
    for index in wrongIndex : 
        originalArray[index][index2] = _week_based(originalArray, index, index2, weekN, var, times)


##functions only for interpolate_avg
    # minimum : index of the starting day, maximum : index of the last day
def _dayCheck(dateSet, minimum, maximum, wrongSet):
    temp = []
    for date in dateSet:
        if date < minimum or date > maximum:
            pass
        elif date in wrongSet:
            pass
        else:
            temp.append(date)
    return temp


def _get_average(originalArray, peripheralArray, index2):
    dataSum = [.0] * 24  # initialization of a list with 24 zeros
    for day in peripheralArray:
        startNum = day * 24 - 24
        for i in range(24):
            dataSum[i] += originalArray[startNum + i][index2]

    return [x / len(peripheralArray) for x in dataSum]
###


#앞뒤 x주만으로 해결되지 않는 애들을 보정할 때
#이 함수는 None을 리턴함 : 보정한 후 originalArray를 직접 수정함(별도의 수정 데이터 반환 없음)
def interpolate_avg (originalArray, wrongArray, index2):


    #collecting all wrong day data set
    wrongDateAndDay = {x[1]:x[3] for x in wrongArray} #dateNumber:dayNum
    wrongDateNum = set(wrongDateAndDay.keys())
    averages = {}
    #temp={}

    start = 0
    end = len(originalArray)/24
    
    for dateNum in wrongDateNum :
        dayNum = wrongDateAndDay[dateNum]
        if dayNum<6: # for weekdays : the main week and the previous and the next, 52 weeks before, and after : 5 weeks
            count = 0
            weekNum = 5-dayNum
            oneWeekNums = []

            while count < 5 : 
                oneWeekNums.append(weekNum)
                weekNum -= 1
                count += 1

            mainWeekNums = [x+dateNum for x in oneWeekNums]
            nextWeekNums = [x+7 for x in mainWeekNums]
            lastWeekNums = [x-7 for x in mainWeekNums]
            oneYearBefore = [x+364 for x in mainWeekNums]
            oneYearAfter = [x-364 for x in mainWeekNums]
            peripherals = mainWeekNums + nextWeekNums + lastWeekNums + oneYearBefore + oneYearAfter
            correctPeripherals = _dayCheck(peripherals, start, end, wrongDateNum)

            if len(correctPeripherals) <3 : pass
            else : 
     #           temp[dateNum] = correctPeripherals
                avgForInterpolation = _get_average(originalArray, correctPeripherals, index2)
                averages[dateNum] = avgForInterpolation

        else :
            if dayNum <8 : # Saturday and Sunday
                normNum = 6-dayNum
            else : #holidays except for Sat & Sun
                normNum = 6-(dayNum-7)
                
            aroundNums = [7,14,21,28,-7,-14,-21,-28]
            saturdays = [x+normNum+dateNum for x in aroundNums]
            sundays = [x+normNum+dateNum+1 for x in aroundNums]
            peripherals = saturdays + sundays
            peripherals = set(peripherals)
            correctPeripherals = _dayCheck(peripherals, start, end, wrongDateNum)

            if len(correctPeripherals) <3 : pass
            else : 
      #          temp[dateNum] = correctPeripherals
                avgForInterpolation = _get_average(originalArray, correctPeripherals, index2)
                averages[dateNum] = avgForInterpolation

    for hourList in wrongArray : #index, dateNum, hour, dayNum, elec
        if hourList[1] in averages :
            originalArray[hourList[0]][index2] = averages[hourList[1]][hourList[2]] #dateNum:a list of interpolated elec for 24 hours

    #return temp


def dailySumSingle (array, index2, startDateIndex=1, endDateIndex=0, stats = True) :
    daily = []
    if endDateIndex == 0 : endDateIndex = len(array)/24
    for i in range(int(startDateIndex-1), int(endDateIndex)) :
        dailySum = 0.0
        for j in range(24) :
            dailySum += array[i*24+j][index2]
        daily.append(dailySum)

    if stats :
        forStatValue = copy.deepcopy(daily)
        forStatValue.sort()
        avg = stat.mean(forStatValue)

        stdev = stat.stdev(forStatValue)
        try : stdevRatio = stdev/avg
        except : stdevRatio = 0

        avgForHighestFive = stat.mean(forStatValue[-5:])

        if avgForHighestFive == 0 :
            avgForLowestFive = 0
            baseRatio = 0

        else :
            count = 0
            length = len(forStatValue)
            while count < length-5  :
                if forStatValue[count] == 0 : count += 1
                else : break

            avgForLowestFive = stat.mean(forStatValue[count:count+5])
            baseRatio = avgForLowestFive/avgForHighestFive

        daily.append(avg)
        daily.append(avgForLowestFive)
        daily.append(avgForHighestFive)
        daily.append(baseRatio)
        daily.append(stdev)
        daily.append(stdevRatio)

    else :
        i = 0
        while i < 6 :
            daily.append("NaN")
            i += 1

    return daily

def dateAndDay(array) :
    res = {}
    for hour in array :
        if hour[0] in res : pass
        else :
            res[hour[0]]=hour[2]
    return res

def dailySumAll(dailySumSingles, dateAndDayDict, headerFromInput, startDay=1, endDay=0):
    res = []
    headerFromInput.pop(1)
    statRows = ['avg', 'lowest', 'highest', 'baseR', 'stdev', 'stdevR']
    res.append(headerFromInput)

    if endDay == 0: endDay = len(dateAndDayDict)+1


    count = 0
    for i in range(int(startDay), int(endDay)) :
        temp = []
        temp.append(i)
        temp.append(dateAndDayDict[i])
        for building in dailySumSingles:
            temp.append(building[count])
        res.append(temp)
        count += 1

    for j in range(6) :
        temp2 = [statRows[j], '']
        for building in dailySumSingles :
            temp2.append(building[count+j])

        res.append(temp2)


    return res



if __name__ == "__main__" :

    startDate = 1
    fileName = 'updatedRaw.txt'

    rawData = readfileVer1(fileName)
    data = rawData[1]
    amended = copy.deepcopy(data)
    length = len(data)

    h = rawData[0]
    NumOfBlds = len(h) - 3
    varTimes = 5

    dailySums = []
    dayForDates = dateAndDay(data)

    initialErrorRow = ['Num of errors', "", ""]
    initialErrorRateRow = ['Error rate', "", ""]
    fixedErrorRow = ['fixed errors', "", ""]
    fixRateRow = ['fix rate', "", ""]

    _iER = []
    _iERR =[]
    _fER = []
    _fRR =[]

    modifyingStartDate = 1278
    modifyingEndDate = 0

    for i in range(NumOfBlds) :
        initialErrors = error_count(data, 3+i, variance(data, 3+i), varTimes, modifyingStartDate, modifyingEndDate)
        _iER.append(initialErrors[0]) #the number of all errors within the modifying range
        _iERR.append(initialErrors[1]) #the percentage of errors within the modifying range

        check = 0
        var = variance(data, 3 + i)
        #wrongData = collect_wrong(data, 3 + i, var, varTimes, modifyingStartDate, modifyingEndDate)
        wrongData = collect_wrong(data, 3 + i, var, varTimes)

        while check < 3:

            interpolate_linear(amended, wrongData, 3+i)
            wrongData = collect_wrong(amended, 3+i, var, varTimes, modifyingStartDate, modifyingEndDate)

            interpolate_week(amended, wrongData, 3+i, 3, var, varTimes)
            wrongData = collect_wrong(amended, 3+i, var, varTimes, modifyingStartDate, modifyingEndDate)

            interpolate_linear_yearLeap(amended, wrongData, 3+i)
            wrongData = collect_wrong(amended, 3+i, var, varTimes, modifyingStartDate, modifyingEndDate)

            interpolate_week_yearLeap(amended, wrongData, 3+i, 3, var, varTimes)
            wrongData = collect_wrong(amended, 3+i, var, varTimes, modifyingStartDate, modifyingEndDate)

            interpolate_avg(amended, wrongData, 3+i)
            wrongData = collect_wrong(amended, 3+i, var, varTimes, modifyingStartDate, modifyingEndDate)

            check += 1
        





        finalErrors = error_count(amended, 3+i, variance(amended, 3+i), varTimes, modifyingStartDate, modifyingEndDate)
#        except :
#            print(i+3)
        #finalErrorRate = finalErrors/ length
        numOfFixed = initialErrors[0] - finalErrors[0]
        fixRate = numOfFixed/initialErrors[0]

        _fER.append(numOfFixed)
        _fRR.append(fixRate)

        temp = dailySumSingle(amended, 3+i, startDateIndex=modifyingStartDate, stats=False)
        dailySums.append(temp)

        print(4+i)

    amended.append(initialErrorRow+_iER)
    amended.append(initialErrorRateRow+_iERR)
    amended.append(fixedErrorRow+_fER)
    amended.append(fixRateRow+_fRR)



    res_hourly = open('hourly_result_variance no change_all.txt', 'w', encoding = 'utf-8')
    res_hourly.write('\t'.join([str(x) for x in h]))
    res_hourly.write('\n')

    for hour in amended :
        res_hourly.write('\t'.join([str(x) for x in hour]))
        res_hourly.write('\n')

    res_hourly.close()

    # dailyResult = dailySumAll(dailySums, dayForDates, h, startDay=modifyingStartDate)

    # dailyResult.append(initialErrorRow[:-1]+_iER)
    # dailyResult.append(initialErrorRateRow[:-1]+_iERR)
    # dailyResult.append(fixedErrorRow[:-1]+_fER)
    # dailyResult.append(fixRateRow[:-1]+_fRR)

    # res_daily = open('daily_result_variance no change_2.txt', 'w', encoding = 'utf-8')

    # for row in dailyResult :
    #     res_daily.write('\t'.join([str(x) for x in row]))
    #     res_daily.write('\n')

    # res_daily.close()


"""
data = readfile('bld302.txt', 182)
h = header('bld302.txt')
amended = copy.deepcopy(data)

var = variance(data, 4)
#amended[994][3]=83.


wrongData = collect_wrong(amended, 4, var, 5)


interpolate_week(amended, wrongData,4,3,var,5)

#whichDay = interpolate_avg(amended, wrongData)
interpolate_avg(amended, wrongData, 4)



res2 = open('res_bld302.txt','w')
res2.write('\t'.join([str(x) for x in h]))
res2.write('\n')
for day in amended:
    res2.write('\t'.join([str(x) for x in day]))
    res2.write('\n')
res2.close()


res3 = open('wrong.txt','w')
for day in wrongData:
    res3.write('\t'.join([str(x) for x in day]))
    res3.write('\n')
res3.close()




res4 = open('amendedDaily_bld302.txt','w')
amendedDaily = daySum(amended, 4,1,550)
for day in amendedDaily:
    res4.write(str(day))
    res4.write('\n')
res4.close()

c = error_count(amended, 4, var, 5)
print (c)

print(h)

"""