import pandas as pd
import numpy as np

from PyQt5 import QtCore
from time import time

from scipy.stats import norm

class NumpyDataFrame :
    def __init__(self, pandasDataFrame='none') :
        if type(pandasDataFrame) != str:
            self.content = pandasDataFrame.values
            self.shape = pandasDataFrame.shape
            self.columns = pandasDataFrame.columns.tolist()
            self.index = pandasDataFrame.index.tolist()

    def changeContent(self, newTable, newColumn = None, newIndex = None):
        self.content = np.array(newTable)
        self.shape = self.content.shape
        if newColumn :
            self.columns = newColumn
        if newIndex :
            self.index = newIndex

    def toStrList(self, whichToConvert):
        if whichToConvert == 'index' :
            return [str(x) for x in self.index]
        elif whichToConvert == 'columns' :
            return [str(x) for x in self.columns]
        else :
            raise KeyError('wrong argument input - either index or columns should be given.')


    def to_pdDF(self):
        return pd.DataFrame(self.content, index=self.index, columns=self.columns)


class Engine(QtCore.QThread) :
    sendTableFrameInfo = QtCore.pyqtSignal(dict) # {'row':verticalHeader, 'col':horizontalHeader}
    sendValueForSingleCell = QtCore.pyqtSignal(tuple) #(rowNum, colNum, Value)
    hideRowSignal = QtCore.pyqtSignal(int) #rowNum
    tableShowFinished = QtCore.pyqtSignal()
    changeStatusbarMessageSignal = QtCore.pyqtSignal(str)

    def __init__(self, programStatus):
        super().__init__()

        self.programStatus = programStatus

        self.elecData_pd = pd.DataFrame()
        self.metaData = pd.DataFrame()

        self.listOfCampuses = []
        self.listOfDepts = []
        self.listOfUsages = []

        self.lengthOfInputPeriod = 0

        self.bldgListForCorrection = []
        self.settingsForCorrection = {}

        self.tableSliced = NumpyDataFrame()
        self.tableForShowing = NumpyDataFrame()
        self.internalTableForShowing = NumpyDataFrame()
        self.validSaverForSliced = NumpyDataFrame()

        # year = [' 0', '-1', '-2', '-3', '-4']
        # dh = [' 0', '-1', '+1']

        year = [' 0', '-1', '-2']
        dh = [' 0', '-1', '+1']

        self.previousTimeDict = {}

        for y in year :
            for d in dh :
                for h in dh :
                    self.previousTimeDict["".join([y, 'y', d, 'd', h, 'h'])] = int(y) * 52 * 7 * 24 + int(d) * 24 + int(h)


    def readFile(self, filePath, fileType):
        if fileType == 'bldg':
            try:
                self.elecData_pd = pd.read_csv(filePath, index_col=0, parse_dates=True, engine='python')\
                    .apply(pd.to_numeric, errors='coerce').fillna(0)
            except UnicodeDecodeError:
                self.elecData_pd = pd.read_csv(filePath, encoding='cp949', index_col=0, parse_dates=True, engine='python')\
                    .apply(pd.to_numeric, errors='coerce').fillna(0)
            # self.parseElec()

        else :
            try:
                self.metaData = pd.read_csv(filePath, engine='python')
            except UnicodeDecodeError:
                self.metaData = pd.read_csv(filePath, encoding='cp949', engine='python')


    def parseMeta(self):
        self.metaData.loc[:, 'item'] = self.metaData.loc[:, '동 번호'] + "동" + " (" + self.metaData.loc[:, '건물명'] + ')'

        self.listOfCampuses = self.metaData['캠퍼스'].unique()
        self.listOfDepts = self.metaData['기관'].unique()
        self.listOfUsages = self.metaData['용도'].unique()

    def checkValue(self, value):
        if self.settingsForCorrection['startValue'] <= value <= self.settingsForCorrection['endValue'] :
            return True
        else :
            return False

    def run(self):
        self.availableBldgs = []
        self.changeStatusbarMessageSignal.emit("데이터 불러오는 중...")

        for bld in self.settingsForCorrection['whichBldgs']:
            if bld in self.elecData_pd.columns :
                self.availableBldgs.append(bld)

        # print(self.availableBldgs)

        tableSliced_pd = self.elecData_pd[self.availableBldgs]
        tableSliced_pd = tableSliced_pd.apply(round, args=(1,))

        validSaverForSliced_pd = pd.DataFrame(dtype=bool)
        validSaverForSliced_pd = validSaverForSliced_pd.reindex_like(tableSliced_pd)

        # when pandas dataframe is converted to numpy ndarray, delete the pandas one
        validSaverForSliced_np = NumpyDataFrame(validSaverForSliced_pd)
        del validSaverForSliced_pd

        tableSliced_pd.loc[:, 'count'] = range(tableSliced_pd.shape[0])

        tableForShowing_pd = tableSliced_pd.loc[self.settingsForCorrection['startDate']:self.settingsForCorrection['endDate']]
        self.lengthOfInputPeriod = tableForShowing_pd.shape[0]
        tableSliced_np = NumpyDataFrame(tableSliced_pd)
        del tableSliced_pd

        indexForMelted = tableForShowing_pd.index.tolist()*len(self.availableBldgs)
        tableForShowing_pd = tableForShowing_pd.melt(id_vars=['count'], var_name='동', value_name='계측량')
        tableForShowing_pd.index = indexForMelted

        internalTableForShowing_np = NumpyDataFrame(tableForShowing_pd)

        tableForShowing_pd = tableForShowing_pd.drop('count', axis=1)  # count column is only for calculation - it should not be shown
        tableForShowing_pd.loc[:, '이상'] = ""

        tableForShowing_np = NumpyDataFrame(tableForShowing_pd)
        del tableForShowing_pd

        #internalTableForShowing.columns : 0 for count, 1 for '동', 2 for 계측량
        #tableForShowing.columns : 0 for '동', 1 for 계측량, 2 for 이상label

        sizeOfTable = tableForShowing_np.shape

        self.sendTableFrameInfo.emit({'row': tableForShowing_np.toStrList('index'),
                                      'col': tableForShowing_np.toStrList('columns')})

        numOfData = str(sizeOfTable[0])
        bldColNum = 0 # position of building in the sliced table
        for rowNum in range(sizeOfTable[0]) :
            statusMessageRowNum = rowNum + 1
            self.sendValueForSingleCell.emit((rowNum, 0, tableForShowing_np.content[rowNum][0]))
            value = tableForShowing_np.content[rowNum][1]
            self.sendValueForSingleCell.emit((rowNum, 1, value))
            # check if the value is outside the range
            if self.checkValue(value):
                pass
            else :
                                                # internalTableForShowing.columns : 0 for count, 1 for '동', 2 for 계측량
                validSaverForSliced_np.content[internalTableForShowing_np.content[rowNum][0]][bldColNum] = False
                # tableForShowing.columns : 0 for '동', 1 for 계측량, 2 for 이상label
                tableForShowing_np.content[rowNum][2] = '이상'
                self.sendValueForSingleCell.emit((rowNum, 2, "이상"))
            if statusMessageRowNum % self.lengthOfInputPeriod == 0:
                bldColNum += 1
            if rowNum % 100 == 0:
                self.changeStatusbarMessageSignal.emit(
                    "".join(["데이터를 추가하고 있습니다 ( ", str(statusMessageRowNum), " / ", numOfData, " )"]))

        self.tableShowFinished.emit()

        # for class variables accessible from other functions, the frame should be numpy ndarray
        self.tableSliced = tableSliced_np
        self.validSaverForSliced = validSaverForSliced_np

        self.tableForShowing = tableForShowing_np
        self.internalTableForShowing = internalTableForShowing_np

        self.correctFunc()

    def correctFunc(self):
        previousHeader = list(self.previousTimeDict.keys())
        # tableForShowing = self.tableForShowing.to_pdDF
        internalTableForShowing_pd = self.internalTableForShowing.to_pdDF()

        # setting table for showing checkboxes and correction data
        if self.settingsForCorrection['iqr']:
            internalTableForShowing_pd.loc[:, '상한1'] = np.nan
            internalTableForShowing_pd.loc[:, '하한1'] = np.nan

        if self.settingsForCorrection['ndist']:
            internalTableForShowing_pd.loc[:, '상한2'] = np.nan
            internalTableForShowing_pd.loc[:, '하한2'] = np.nan

        internalTableForShowing_pd.loc[:, '추천'] = np.nan

        # tableForShowing = tableForShowing.reindex(columns = tableForShowing.columns.tolist() + previousHeader)
        internalTableForShowing_pd = internalTableForShowing_pd.reindex(columns = internalTableForShowing_pd.columns.tolist()
                                                                               + previousHeader)

        newHeaderForShowing = self.tableForShowing.columns + internalTableForShowing_pd.columns.tolist()[3:]

        tableForShowing_pd = self.tableForShowing.to_pdDF()
        tableForShowing_pd = tableForShowing_pd.reindex(columns = newHeaderForShowing)

        internalTableForShowing_np = NumpyDataFrame(internalTableForShowing_pd)
        del internalTableForShowing_pd

        startColNum = tableForShowing_pd.columns.get_loc(previousHeader[0])
        sizeOfTable = tableForShowing_pd.shape
        numOfData = str(sizeOfTable[0])

        tableForShowing_np = NumpyDataFrame(tableForShowing_pd)
        del tableForShowing_pd

        self.sendTableFrameInfo.emit({'col': tableForShowing_np.toStrList('columns')})

        lengthOfEntireData = self.elecData_pd.shape[0] # the whole number of period of the elecData file
        bldColNum = 0
        start = time()
        for rowNum in range(sizeOfTable[0]) :
            statusMessageRowNum = rowNum + 1
            if rowNum % 100 == 0 :
                self.changeStatusbarMessageSignal.emit("".join(["주변 데이터를 불러오고 있습니다... ( ", str(statusMessageRowNum), " / ", numOfData, " )"]))
            currentTimeIndex = internalTableForShowing_np.content[rowNum][0]
            colNum = startColNum
            # 0 for count, 1 for 동, 2 for 계측량, 3 for 이상
            for header in self.previousTimeDict:
                targetTimeIndex = int(currentTimeIndex + self.previousTimeDict[header])
                if 0 <= targetTimeIndex < lengthOfEntireData :
                    value = self.tableSliced.content[targetTimeIndex][bldColNum]
                    if self.checkValue(value) :
                        tableForShowing_np.content[rowNum][colNum] = value
                        internalTableForShowing_np.content[rowNum][colNum] = value
                        self.sendValueForSingleCell.emit((rowNum, colNum, value))
                    else :
                        self.validSaverForSliced.content[targetTimeIndex][bldColNum] = False
                        wrongValue = "".join(['(', str(value), ')'])
                        tableForShowing_np.content[rowNum][colNum] = wrongValue
                        self.sendValueForSingleCell.emit((rowNum, colNum, wrongValue))
                colNum += 1
            if statusMessageRowNum % self.lengthOfInputPeriod == 0:
                bldColNum += 1


        self.tableShowFinished.emit()
        self.changeStatusbarMessageSignal.emit("모든 데이터가 로딩되었습니다.")
        print(time() - start)

        self.tableForShowing = tableForShowing_np
        self.internalTableForShowing = internalTableForShowing_np
