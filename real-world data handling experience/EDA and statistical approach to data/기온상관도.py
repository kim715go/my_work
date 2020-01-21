import pandas as pd
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

import os
import matplotlib as mpl

mpl.rc('font', family='HCR Dotum')

daily = pd.read_table("totalAmendedDailySumFor3Years.txt", date_parser=True)
daily = daily.rename(columns = {"요일":'bldNum'})
daily.index = daily['bldNum']
daily = daily.drop('bldNum', axis = 1)

daily = daily.transpose()
daily.index = pd.date_range('20150101', periods = 1096)


metaData = pd.read_table("15-17metaData.txt", encoding = 'ansi', date_parser=True)
metaData.index = pd.date_range('1/1/2015', periods = 1096)
metaData = metaData.drop(['날짜', '날짜.1'], axis=1)


x = sp.symbols('x')
dailyForAnal = daily
dailyForAnal['요일'] = metaData['요일']
dailyForAnal['기온'] = metaData['기온']

dailyForAnal = dailyForAnal.query('요일<6')

g = dailyForAnal.columns.tolist()
g = g[-2:] + g[:-2]
dailyForAnal = dailyForAnal[g]

for year in range(2015, 2018):
    os.makedirs('predictions'+str(year), exist_ok=True)
    print('starting ', year)
    yearly= dailyForAnal[str(year)]

    #fDCriticals = []
    #fDChecks = []
    #sDCriticals = []
    #sDChecks = []
    #accuracy = {}
    gradients = {}

    length = len(yearly)
    
    tempMin = int(round(yearly['기온'].min()))
    tempMax = int(round(yearly['기온'].max()))
    xx = np.linspace(tempMin-1, tempMax+1, 300)
    tempRange = range(tempMin, tempMax+1)
    
    for colName in yearly.columns[2:]:
        fig = plt.figure(figsize=(10,6))
        
        mean = np.mean(yearly[colName])
        temp = np.polyfit(yearly['기온'], yearly[colName], 5, full=True)
        summ = np.sum((yearly[colName]-mean)**2)
        
        rsqrd = round(float(1-temp[1]/summ), 3)
        stde= round(float((temp[1]/length)**.5), 2)
        
        regression = sp.Poly(temp[0], x)
        
        #observedMin = yearly[colName].min()
        #observedMax = yearly[colName].max()
        
        plt.plot(yearly['기온'], yearly[colName], 'o', label = '관측값')
        

        yy = [regression(i) for i in xx]
        
        plt.plot(xx, yy, label="추세선")
        plt.plot(xx, [x+2*stde for x in yy], label=r'$+2\sigma$')
        plt.plot(xx, [x-2*stde for x in yy], label=r'$-2\sigma$')

        try : meanSd = round(float(stde/mean)*100, 1)
        except : meanSd = 0
        
        plt.xlabel(r'$r^2$' + "=" + str(rsqrd) +" / "  + r'$\sigma$' + '='+ str(stde) 
        + " (" + str(meanSd) + "% of observed mean " + str(round(mean, 2)) + ")")
        plt.legend(loc=0)
        plt.title(str(year) + " bld " + colName)
        
        fig.savefig(os.path.join('predictions'+str(year)+'/'+colName+'.png'))
        plt.close(fig)
        
        
        diff = sp.diff(regression, x)
        grad = [diff(i) for i in tempRange]
        gradients[colName] = grad
        
        #secondDiff = sp.diff(diff, x)
        #thirdDiff = sp.diff(secondDiff, x)

        #firstCritical = [sp.re(i) for i in sp.solve(diff, x) if abs(sp.im(i))<.0001]
        #secondCritical = [sp.re(i) for i in sp.solve(secondDiff, x) if abs(sp.im(i)) <.0001]

        #fDCriticals.append(firstCritical)
        #fDChecks.append([secondDiff(i) for i in firstCritical])

        #sDCriticals.append(secondCritical)
        #sDChecks.append([thirdDiff(i) for i in secondCritical])

        #accuracy[colName] = {'rsqrd':float(1-temp[1]/summ), 'ste' : float((temp[1]/length)**.5), 'mean':mean}

        print(colName, end= " ")

    #firstD = pd.DataFrame(fDCriticals, yearly.columns[2:])
    #secondD = pd.DataFrame(sDCriticals, yearly.columns[2:])
    #firstC = pd.DataFrame(fDChecks, yearly.columns[2:])
    #secondC = pd.DataFrame(sDChecks, yearly.columns[2:])
    #acc = pd.DataFrame(accuracy).transpose()

    #firsts = firstD.join(firstC, lsuffix = ' criticals', rsuffix = ' checks')
    #seconds = secondD.join(secondC, lsuffix = ' criticals', rsuffix = ' checks')

    #res = firsts.join(seconds, lsuffix = ' 1st', rsuffix = ' 2nd')
    #res = res.join(acc)

    #res.to_csv('tempAnal'+str(year)+'.txt', sep='\t')
    
    gradDF = pd.DataFrame(gradients, tempRange)
    gradDF = gradDF.transpose()
    gradDF.to_csv("gradients"+str(year)+".txt", sep='\t')
    print('\n')