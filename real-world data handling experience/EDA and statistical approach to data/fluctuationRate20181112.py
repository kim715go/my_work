import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc('font', family='HCR Dotum')

# ---------------------------

totalData = pd.read_table("3yearAmendedFinished180523.txt", encoding='cp949')
metaData = pd.read_table("15-17metaData.txt", encoding='cp949')
totalData.index = pd.date_range('20150101', periods = 365*24+366*24+365*24, freq='h')
totalData = totalData.drop(['날짜', '시간'], axis=1)
metaData.index = pd.date_range('20150101', periods = 365*2 + 366)
metaData = metaData.drop(['날짜', '날짜.1'], axis=1)
y17 = pd.read_table("totalAnalysis2017.txt")
bldInfo = y17[['totalArea', 'deptCode', 'bldNum', 'usageCode']]
bldInfo.index = bldInfo['bldNum']
bldInfo = bldInfo.drop('bldNum', axis=1)

# ------------------ 2017data
y17Data = totalData['2017']
daily17 = y17Data.groupby([y17Data.index.month, y17Data.index.day]).sum()
daily17.index = pd.date_range('20170101', periods=365)
daily17['요일'] = metaData['2017']['요일']
daily17['temp'] = metaData['2017']['기온']

bldData = pd.DataFrame()
bldData['perArea'] = daily17.sum()/bldInfo['totalArea']

baseRateDaily = []
for colName in daily17: 
    bldSeries = daily17[colName]
    bldSeries = bldSeries.iloc[bldSeries.nonzero()]
    bldSeries = bldSeries.sort_values()
    smallest = sum(bldSeries[:5])
    largest = sum(bldSeries[-5:])
    if largest : 
        temp = smallest/largest
    else : 
        temp = 0
        
    baseRateDaily.append(temp)

bd = pd.Series(baseRateDaily)
bd.index = daily17.columns
bldData['bRD'] = bd

hourlyRate = []
hourlySum = y17Data.groupby(y17Data.index.hour).sum()

for colNames in hourlySum :
    bldSeries = hourlySum[colNames]
    bldSeries = bldSeries.sort_values()
    if bldSeries.iloc[-1] : 
        hourlyRate.append(bldSeries.iloc[0]/bldSeries.iloc[-1])
    else : 
        hourlyRate.append(0)

hr = pd.Series(hourlyRate)
hr.index = y17Data.columns

bldData['hRD'] = hr

monthlySum = daily17.groupby(daily17.index.month).sum()
monthlySum['season'] = ['w','w','w', 'm','m','s','s','s','s', 'm','m','w']
seasonal = monthlySum.groupby('season').sum().transpose()

bldData['winter'] = seasonal['w']/seasonal['m']
bldData['summer'] = seasonal['s']/seasonal['m']

# ----------------------------------------------------
newInfo = pd.read_excel("bldInfoNew.xlsx")

new = []
for i in newInfo['동 No.'] : 
    i = str(i)
    i = i.replace('_', '-')
    new.append(i)

newInfo['동 No.'] = new
newInfo.index = newInfo['동 No.']
newInfo = newInfo.drop('동 No.', axis=1)

bldInfo[['bldName', 'year', 'heatP']] = newInfo[['건물명', '준공연도', '냉난방시설']]


dif = pd.read_table("diffs.txt")
dif.index = dif['bldNum']
dif = dif.drop('bldNum', axis=1)
bldData['diffR'] = dif['diff']

newValidOnes = pd.read_excel('validones.xlsx')
forNormalize = newValidOnes.drop(['bRD', 'win/sum'], axis=1)
normalized_nO = (forNormalize - forNormalize.mean())/forNormalize.std()

newValidOnes[['bldName', 'year', 'heatP']] = newInfo[['건물명', '준공연도', '냉난방시설']]
newValidOnes[['deptCode', 'usageCode']] = bldInfo[['deptCode', 'usageCode']]
newValidOnes.iloc[:, 1:7] *= 100

#winter-summer rate
newValidOnes['win/sum'] = newValidOnes['winter']/newValidOnes['summer']*100

plots = list(newValidOnes.columns[:7])
plots.remove('bRD')

y17.index = y17.bldNum
y17 = y17.drop('bldNum', 1)

newValidOnes['dailyFluct'] = y17.fluctRate
newValidOnes['hourlyFluct'] = y17Data.std()/y17Data.mean()

columnNames = ['인문사회계', '이공계', '예술계', '행정지원', '연구시설', '강의지원', '편의시설', '학술지원']
# fileNames = ['원단위', '기저율', '난방률', '냉방률', '냉방대비율', '증감률']

# subNames = ['일단위 변동계수(표준편차/평균)', '시간단위 변동계수(표준편차/평균)']
# fileNames = ['일단위 변동계수', '시간단위 변동계수']


subNames = ['EUI(원단위 사용량, (kWh/㎡·year)', '기저부하율(시간단위)(%)', '난방기간 에너지 변동비(%)', '냉방기간 에너지 변동비(%)', '전년대비 사용량 증감율(%)', '일단위 변동계수(표준편차/평균)']

# subNames = ['냉방 대비 난방 에너지 부하율(%)']


plots = ['perArea', 'hRD', 'winter', 'summer', 'diffR', 'dailyFluct']

res = {}

fig = plt.figure(figsize=(15,11))

positionNum = 231

means = []
stds = []

for i in range(8) : 
    temp = newValidOnes.query('usageCode=='+str(i))
    means.append(temp.mean())
    stds.append(temp.std())

for index, item in enumerate(plots) : 

    plt.subplot(positionNum)

    for i in range(8) : 
        plt.title(subNames[index])
        lowerLim = means[i][item]-stds[i][item]
        if lowerLim >= 0 : 
           pass
        else : 
            lowerLim = 0

        plt.plot([lowerLim, means[i][item]+stds[i][item]], [i+1, i+1], '-', color='xkcd:sky blue', linewidth=18)
        plt.plot([means[i][item], ],[i+1,], 'r|', markersize=21, markeredgewidth=4)

    plt.tight_layout()

    positionNum += 1

    plt.yticks([x+1 for x in range(8)], columnNames)
    plt.ylim([0,9])
    plt.grid()

plt.suptitle('용도별 척도 비교', fontsize=16)
fig.tight_layout(rect=[0, 0.03, 1, 0.95])
#plt.show()
#fig.tight_layout()
fig.savefig('범위비교.png')
plt.close(fig)