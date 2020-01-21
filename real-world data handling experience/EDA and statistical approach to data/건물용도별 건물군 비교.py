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

plots = list(newValidOnes.columns[:7])
plots.remove('bRD')

columnNames = ['인문사회계', '이공계', '예술계', '행정지원', '연구시설', '강의지원', '편의시설', '학술지원']
subNames = ['연면적당(kWh/㎡·year)', '시간단위기저율(%)', '동계비(%)', '하계비(%)', '동계/하계비(%)', '증감비(%)']

for usage in range(8) : 

    test = newValidOnes.query('usageCode == '+ str(usage))
    fig = plt.figure(figsize=(15,11))

    for i in range(6) : 

        positionNum = 231
        positionNum += i

        temporar = test[plots[i]]
        temporar = temporar.sort_values()
        y = list(temporar)

        plt.subplot(positionNum)
        plt.plot(y, range(len(y)), 'o')
        plt.yticks(range(len(y)), temporar.index)
        plt.xticks(temporar.quantile([0, .25, .5, .75, 1]))
        plt.title(subNames[i])
        plt.grid()

    plt.suptitle(columnNames[usage], fontsize=16)
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    #plt.show()
    #fig.tight_layout()
    fig.savefig(columnNames[usage]+".png")
    plt.close(fig)