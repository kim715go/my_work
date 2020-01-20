import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rc('font', family='HCR Dotum')


def gather(folderName) : 
    
    folder = os.listdir('./'+folderName + '/')
    
    medianDic= {}
    meanDic= {}
    
    for fileN in folder : 
        fileTable = pd.read_table(folderName+"/"+fileN, index_col = 0, parse_dates = True)
        fileN = fileN.split('_')
        bldNum = fileN[0][3:]

        meanSub = []
        medianSub = []
        for row in fileTable.itertuples() : 
            if row[4] == 'abnormal' : 
                meanSub.append(row[5])
                medianSub.append(row[6])
            else : 
                meanSub.append(row[1])
                medianSub.append(row[1])

        medianDic[bldNum] = medianSub
        meanDic[bldNum] = meanSub
        
    return medianDic, meanDic


def to_num(dataframe):
    for col in dataframe : 
        dataframe[col] = pd.to_numeric(dataframe[col], errors='coerce').fillna(0)

bldMeta = pd.read_table('bldMetaData.txt', encoding='cp949',  index_col=0)

original = pd.read_table("updatedRaw.txt", encoding='cp949')
original.index = pd.date_range('20150101', freq='h', periods = 1339*24)
original = original.drop(['날짜', '시간', '요일'], axis =1)
to_num(original)

# ttest = pd.read_table("hourly_result_variance no change_2.txt")
# ttest = ttest.iloc[:1277*24,:]
# ttest.index = pd.date_range('20150101', freq= 'h', periods = 1277*24)
# ttest = ttest.drop(['날짜', '시간', '요일'], axis =1)
# to_num(ttest)

traditionalModified = pd.read_table("hourly_result_variance no change_all.txt")
traditionalModified = traditionalModified.iloc[:1339*24,:]
traditionalModified.index = pd.date_range('20150101', freq= 'h', periods = 1339*24)
traditionalModified = traditionalModified.drop(['날짜', '시간', '요일'], axis =1)
to_num(traditionalModified)

changed_raw = gather('ci98_first')
changed=[changed_raw[0]]

# differentlyModified = pd.read_table("hourlyResWithRevisedAlgorithm.txt")
# differentlyModified = differentlyModified.iloc[:30648,:]
# differentlyModified.index = pd.date_range('20150101', freq= 'h', periods = 30648)
# differentlyModified = differentlyModified.drop(['날짜', '시간', '요일'], axis =1)
# to_num(differentlyModified)

# differentlyModified2 = pd.read_table("hourlyResWithRevisedAlgorithm_2.txt")
# differentlyModified2 = differentlyModified2.iloc[:30648,:]
# differentlyModified2.index = pd.date_range('20150101', freq= 'h', periods = 30648)
# differentlyModified2 = differentlyModified2.drop(['날짜', '시간', '요일'], axis =1)
# to_num(differentlyModified2)

# final = pd.read_table("final.txt", encoding = 'cp949', parse_dates=True, index_col=0)
# to_num(final)


changedTable = []
for dic in changed : 
    tableTable = pd.DataFrame(dic)
    tableTable.index = pd.date_range('20180701', freq='h', periods = 62*24)
    changedTable.append(tableTable)
for i in changedTable : 
    to_num(i)

lengthOfHours = 62*24
dateRange = pd.date_range('20180701', freq='h', periods = lengthOfHours)


revised = pd.read_excel("D:/python projects/201810projects/finalVersion1807~08.xlsx", parse_dates=True, index_col=0)



for bldName in original : 
    #totalHourlyMeanBefore = original['2018'][bldName].mean()
    totalHourlyMeanBefore = original.loc[dateRange, bldName].mean()
    #firstChanged = ttest['2018'][bldName].mean()
    #finalMean = changedTable[0].loc[dateRange, bldName].mean()
    different_changed_double_mean = changedTable[0].loc[dateRange,bldName].mean()
    #ciChangedMedian = changedTable[0][bldName].mean()
    #differentlyModifiedMean = differentlyModified.loc[dateRange, bldName].mean()
    #ci99_exceptMean = changedTable[1].loc[dateRange, bldName].mean()
    #finalMean = final['2018'][bldName].mean()
    #ci98_doubleMean = changedTable[1].loc[dateRange, bldName].mean()
    #differentlyModifiedMean2 = differentlyModified2.loc[dateRange, bldName].mean()
    traditionalModifiedMean = traditionalModified.loc[dateRange,bldName].mean()
    #ttestMean = ttest.loc[dateRange,bldName].mean()
    revised_mean = revised.loc[dateRange, bldName].mean()



    fig = plt.figure(figsize=(18,12))

    plt.subplot(221)
    plt.plot(original.loc[dateRange, bldName])
    plt.plot(dateRange, [totalHourlyMeanBefore]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')
    plt.margins(x=0)
    plt.grid()
    plt.title("보정 전", fontsize= 15)
    
    plt.subplot(224)
    plt.plot(revised.loc[dateRange, bldName])
    plt.plot(dateRange, [revised_mean]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')    
    plt.margins(x=0)
    plt.grid()
    plt.title("최종 보정 결과", fontsize=15)
    
    plt.subplot(222)
    plt.plot(changedTable[0].loc[dateRange, bldName])
    plt.plot(dateRange, [different_changed_double_mean]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')    
    plt.margins(x=0)
    plt.grid()
    plt.title('보정 후(정규화)', fontsize=15)
    
    plt.subplot(223)
    plt.plot(traditionalModified.loc[dateRange, bldName])
    plt.plot(dateRange, [traditionalModifiedMean]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')
    plt.margins(x=0)
    plt.grid()
    plt.title("기존 방식 보정", fontsize= 15)

    # plt.subplot(223)
    # plt.plot(differentlyModified.loc[dateRange, bldName])
    # plt.plot(dateRange, [differentlyModifiedMean]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')
    # plt.margins(x=0)
    # plt.grid()
    # plt.title("알고리즘 변경 후 보정", fontsize= 15)

    # plt.subplot(224)
    # plt.plot(changedTable[1].loc[dateRange, bldName])
    # plt.plot(dateRange, [different_changed_double_mean]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')    
    # plt.margins(x=0)
    # plt.grid()
    # plt.title('변경 알고리즘 + ci98 이중 보정 '+bldName + ' hourly', fontsize=15)


    # plt.subplot(222)
    # plt.plot(differentlyModified2.loc[dateRange, bldName])
    # plt.plot(dateRange, [differentlyModifiedMean2]*lengthOfHours, linestyle = '-', linewidth=2, color = 'red')
    # plt.margins(x=0)
    # plt.grid()
    # plt.title("알고리즘 또 변경(기존방식) 보정", fontsize= 15)

    plt.suptitle("".join(["2018/7~2018/8 보정 전후 비교 - ", bldName, "동 (", str(bldMeta.loc[bldName]['건물명']) , ")"]), fontsize=18)
    #fig.tight_layout()
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig( bldName+".png")
    plt.close(fig)

    print(bldName)

