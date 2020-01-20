# -*- coding: utf-8 -*-
# ver 2.1.3 (19/3/28)

from PyQt5 import QtCore, QtGui, QtWidgets

from datetime import timedelta, datetime, date

from os import rename, mkdir, listdir
from os.path import isdir
from random import sample as randomSample
from string import ascii_letters

import pandas as pd

import requests
from bs4 import BeautifulSoup

from itertools import chain

import re

import sys


def createFolder(folderName) :
    if not isdir(folderName) :
        mkdir(folderName)

class Calculator(QtCore.QThread) :
    updateStatusSignal = QtCore.pyqtSignal(tuple)
    finishedSignal = QtCore.pyqtSignal(str)

    def __init__(self, status, tagFiles, formula, whetherRounded, splitRegex, encoding):
        super().__init__()
        self.status = status
        self.tagFiles = tagFiles
        self.formula = formula
        self.whetherRounded = whetherRounded
        self.splitRegex = splitRegex
        self.encoding = encoding
        self.wholeFolderName = datetime.now().strftime("%Y%m%d_%H%M%S")+'_calc'
        createFolder(self.wholeFolderName)

    # def splitFunc(self, indices, strings):
    #     totalLen = len(strings)
    #     numOfIndices = len(indices)
    #     res = []
    #     if indices:
    #         indices.append(totalLen)
    #         for i in range(numOfIndices):
    #             # print(i)
    #             res.append(strings[indices[i] + 1: indices[i + 1]].strip())
    #     return res
    #
    # def allIndices(self, mainString, sub):
    #     res = []
    #     i = mainString.find(sub)
    #     while i >= 0:
    #         res.append(i)
    #         i = mainString.find(sub, i + 1)
    #     return res

    def run(self):
        self.updateStatusSignal.emit(("계산을 시작합니다...", 'calc'))
        length = self.formula.shape[0]
        count = 0
        while self.status['isRunning']  and count < length:
            if self.status['isPaused'] :
                pass
            else :
                bldg = self.formula.iloc[count]
                formulaText = bldg[1]
                signPos = [x.strip() for x in re.findall(self.splitRegex, formulaText)]
                tags = [x.strip() for x in re.split(self.splitRegex, formulaText)]
                resTable = self.tagFiles[tags[0]].copy()

                if signPos :
                    signLength = len(signPos)
                    order = 0
                    while order < signLength :
                        if signPos[order] == "+" :
                            resTable += self.tagFiles[tags[order + 1]]
                        else :
                            resTable -= self.tagFiles[tags[order + 1]]
                        order += 1

                if self.whetherRounded :
                    resTable = resTable.apply(pd.to_numeric, errors='coerce').fillna(0).round().astype(int)
                resTable.to_csv(self.wholeFolderName + "/" + bldg[0]+'.csv', encoding = self.encoding)
                self.updateStatusSignal.emit((bldg[0] + " 계산 완료", 'calc'))
                count += 1

        self.updateStatusSignal.emit(("모든 계산이 끝났습니다.", 'calc'))
        self.finishedSignal.emit('calc')


class Crawler(QtCore.QThread) :
    updateStatusSignal = QtCore.pyqtSignal(tuple)
    finishedSignal = QtCore.pyqtSignal(str)
    invalidTagsSignal = QtCore.pyqtSignal(tuple)
    updateProgressValue = QtCore.pyqtSignal(tuple)

    def __init__(self, status, tagList, startDate, period, whetherRounded, sessionList, encoding):
        super().__init__()
        self.status = status
        self.tagList = tagList
        self.startDate = startDate
        self.period = period
        self.whetherRounded = whetherRounded
        self.session = sessionList[0]
        self.encoding = encoding
        self.wholeFolderName = datetime.now().strftime("%Y%m%d_%H%M%S") + '_retrieve'
        createFolder(self.wholeFolderName)

        self.dataHeader = {'Content-Type': 'text/xml; charset=utf-8', 'SOAPAction': 'http://tempuri.org/GetDataAi',
                      'Host': '147.46.160.12', 'Expect': '100-continue'}

        self.resColNames =['0시', '1시', '2시', '3시', '4시', '5시', '6시', '7시', '8시', '9시', '10시', '11시', '12시',
                           '13시', '14시', '15시', '16시', '17시', '18시', '19시', '20시', '21시', '22시', '23시']
        self.resIndex = pd.date_range(self.startDate, periods=self.period).strftime("%Y%m%d")


    def eachTag(self, tagNameList, startPoint, order, length):
        #requestSession should be a list containing a session of the requests module : we need its reference, not the object
        tagNameForRequest = ".".join(tagNameList)
        if re.findall(r'(?!GIMAC(_i|V))(^GIPAM|^GIMAC)', tagNameList[1]) :
            tagNameForRequest += ".KW"
        else :
            tagNameForRequest += ".W"
        tagNameForSave = " ".join(tagNameList) + ".csv"
        signalList = ["( ", str(order), " / ",  str(length), " )", " " , tagNameForRequest, " 수집 중..."]

        self.updateStatusSignal.emit(("".join(signalList), 'crawler'))
        # self.updateProgressValue.emit((0, 'crawler'))

        res = []
        validCheck = []

        count = 0
        while self.status['isRunning'] and count < self.period :
            if self.status['isPaused'] :
                pass
            else :
                dataXML = "".join(["""<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><GetDataAi xmlns="http://tempuri.org/"><tag>""",
                                   tagNameForRequest, "</tag><value_type>15</value_type><data_time>1</data_time><year>", str(startPoint.year), "</year><mon>",
                                   str(startPoint.month), "</mon><day>", str(startPoint.day), "</day><hour>0</hour><min>0</min><data_count>24</data_count><data_gab>1</data_gab></GetDataAi></s:Body></s:Envelope>"]).encode('utf-8')
                rd = self.session.post("http://147.46.160.12/AutoWeb/Service/ServiceDataTag.asmx", data=dataXML, headers=self.dataHeader)
                eachDay = [x.get_text() for x in BeautifulSoup(rd.text, 'xml').find_all('SUM')]
                validCheck += eachDay
                res.append(eachDay)
                startPoint += timedelta(days=1)
                count += 1
                # self.updateProgressValue.emit((round((count+1)/self.period), 'crawler'))

        while self.status['isRunning'] : 
            if self.status['isPaused'] : 
                pass
            else : 
                resTable = pd.DataFrame(res, index = self.resIndex, columns = self.resColNames)
                resTable.index.name = "날짜"

                if self.whetherRounded :
                    resTable = resTable.apply(pd.to_numeric, errors='coerce').fillna(0).round().astype(int)
                resTable.to_csv(self.wholeFolderName + "/" + tagNameForSave, encoding=self.encoding)

                self.updateStatusSignal.emit(("".join(signalList[:-1])+" 수집 완료", 'crawler'))

                if len(set(validCheck)) == 1:
                    return [tagNameForRequest]
                else :
                    return []
                break

    def run(self):
        self.updateStatusSignal.emit(("정보 수집을 시작합니다...", 'crawler'))
        length = self.tagList.shape[0]
        runCount = 0
        invalidTags = []

        while self.status['isRunning'] and runCount < length :
            if self.status['isPaused'] :
                pass
            else :
                tagNameList = [str(x) for x in [self.tagList.iloc[runCount, 0], self.tagList.iloc[runCount, 1]]]
                invalidTag = self.eachTag(tagNameList, self.startDate, runCount+1, length)
                runCount += 1
                if invalidTag : 
                    invalidTags += invalidTag

        self.updateStatusSignal.emit(("수집 완료", 'crawler'))
        self.finishedSignal.emit('crawler')

        if invalidTags :
            self.invalidTagsSignal.emit(("\n".join(invalidTags), 'crawler'))


class Ui_MainWindow(QtWidgets.QMainWindow):

    def __init__(self) :
        super().__init__()

        self.calcStatus = {'isRunning':False, 'isPaused':False}
        self.retrieveStatus = {'isRunning' : False, 'isPaused' : False}
        self.roundBoxEnabled = {'calc' : False, 'crawler' : False}
        self.saveAsRounded = {'calc' : False, 'crawler' : False}
        self.clearButtonEnabled = {'calc' : True , 'crawler': True}
        self.progressVisible = {'calc' : False, 'crawler' : False}
        self.progressValue = {'calc' : 0, 'crawler' : 0}
        self.retrieveConnected = False
        # self.isCp949 = False

        today = date.today()

        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)

        self.resize(512, 456)
        self.centralwidget = QtWidgets.QWidget()
        self.wholeVerticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setFont(font)
        self.calcTab = QtWidgets.QWidget()
        self.calcTab.setAutoFillBackground(True)

        self.calcTabLayout = QtWidgets.QVBoxLayout(self.calcTab)
        self.calcTabOpenRow = QtWidgets.QHBoxLayout()
        self.calcTabCalcRow = QtWidgets.QHBoxLayout()

        self.openFormula = QtWidgets.QPushButton(self.calcTab)
        self.openFormula.setFont(font)
        self.export = QtWidgets.QPushButton(self.calcTab)
        self.export.setFont(font)
        self.startCalc = QtWidgets.QPushButton(self.calcTab)
        self.startCalc.setFont(font)
        self.pauseCalc = QtWidgets.QPushButton(self.calcTab)
        self.pauseCalc.setFont(font)
        self.abortCalc = QtWidgets.QPushButton(self.calcTab)
        self.abortCalc.setFont(font)

        self.calcTabOpenRow.addWidget(self.openFormula)
        calcSpacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.calcTabOpenRow.addItem(calcSpacerItem)
        self.calcTabOpenRow.addWidget(self.export)

        self.calcTabCalcRow.addWidget(self.startCalc)
        self.calcTabCalcRow.addWidget(self.pauseCalc)
        self.calcTabCalcRow.addWidget(self.abortCalc)

        self.calcTabLayout.addLayout(self.calcTabOpenRow)
        self.calcTabLayout.addLayout(self.calcTabCalcRow)

        self.calcStatusLabel = QtWidgets.QLabel(self.calcTab)
        self.calcStatusLabel.setFont(font)

        self.calcTabLayout.addWidget(self.calcStatusLabel)

        self.tabWidget.addTab(self.calcTab, "계산")
        self.tabWidget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.retrieveTab = QtWidgets.QWidget()
        self.retrieveTab.setAutoFillBackground(True)
        self.retrieveTabLayout = QtWidgets.QVBoxLayout(self.retrieveTab)

        self.retrieveTabDateRow = QtWidgets.QHBoxLayout()
        self.startDateVertical = QtWidgets.QVBoxLayout()
        self.startLabel = QtWidgets.QLabel(self.centralwidget)
        self.startLabel.setFont(font)
        self.startLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startDateVertical.addWidget(self.startLabel)
        self.startDate = QtWidgets.QDateEdit(self.centralwidget)
        self.startDate.setFont(font)
        self.startDate.setAlignment(QtCore.Qt.AlignCenter)
        self.startDate.setDate(QtCore.QDate(today.year, today.month, 1))
        self.startDate.setCalendarPopup(True)
        self.startDate.setMaximumDate(QtCore.QDate(today))
        self.startDateVertical.addWidget(self.startDate)
        self.retrieveTabDateRow.addLayout(self.startDateVertical)
        self.endDateVertical = QtWidgets.QVBoxLayout()
        self.endLabel = QtWidgets.QLabel(self.centralwidget)
        self.endLabel.setFont(font)
        self.endLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endDateVertical.addWidget(self.endLabel)
        self.endDate = QtWidgets.QDateEdit(self.centralwidget)
        self.endDate.setFont(font)
        self.endDate.setAlignment(QtCore.Qt.AlignCenter)
        self.endDate.setDate(QtCore.QDate(today))
        self.endDate.setMaximumDate(QtCore.QDate(today))
        self.endDate.setCalendarPopup(True)
        self.endDateVertical.addWidget(self.endDate)
        self.retrieveTabDateRow.addLayout(self.endDateVertical)
        self.retrieveTabLayout.addLayout(self.retrieveTabDateRow)

        self.retrieveTabUpperButtonsRow = QtWidgets.QHBoxLayout()
        self.startRetrieve = QtWidgets.QPushButton(self.centralwidget)
        self.startRetrieve.setFont(font)
        self.retrieveTabUpperButtonsRow.addWidget(self.startRetrieve)
        self.pauseRetrieve = QtWidgets.QPushButton(self.centralwidget)
        self.pauseRetrieve.setFont(font)
        self.retrieveTabUpperButtonsRow.addWidget(self.pauseRetrieve)
        self.abortRetrieve = QtWidgets.QPushButton(self.centralwidget)
        self.abortRetrieve.setFont(font)
        self.retrieveTabUpperButtonsRow.addWidget(self.abortRetrieve)
        self.retrieveTabLayout.addLayout(self.retrieveTabUpperButtonsRow)

        self.tabWidget.addTab(self.retrieveTab, "수집")

        self.wholeVerticalLayout.addWidget(self.tabWidget)

        self.roundAndProgressRow = QtWidgets.QHBoxLayout()

        self.whetherRounded = QtWidgets.QCheckBox(self.centralwidget)
        self.whetherRounded.setFont(font)
        self.roundAndProgressRow.addWidget(self.whetherRounded)

        self.changeEncoding = QtWidgets.QCheckBox(self.centralwidget)
        self.changeEncoding.setFont(font)
        self.roundAndProgressRow.addWidget(self.changeEncoding)


        self.progressShow = QtWidgets.QProgressBar(self.centralwidget)
        self.progressShow.setFont(font)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.roundAndProgressRow.addItem(spacerItem)
        self.roundAndProgressRow.addWidget(self.progressShow)

        self.wholeVerticalLayout.addLayout(self.roundAndProgressRow)

        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.wholeVerticalLayout.addWidget(self.tableWidget)
        self.lowerButtonsRow = QtWidgets.QHBoxLayout()
        self.saveLogButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveLogButton.setFont(font)
        self.lowerButtonsRow.addWidget(self.saveLogButton)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        self.clearButton.setFont(font)
        self.lowerButtonsRow.addWidget(self.clearButton)

        self.lowerButtonsRow.addItem(spacerItem)
        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setFont(font)
        self.lowerButtonsRow.addWidget(self.exitButton)
        self.wholeVerticalLayout.addLayout(self.lowerButtonsRow)
        self.setCentralWidget(self.centralwidget)

        self.statusBar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusBar)
        font.setPointSize(9)
        self.statusBar.setFont(font)
        self.crawlerStatusBarMessage = "준비"
        self.calcStatusBarMessage = '준비'

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("오토베이스 데이터 추출기 v 2.1.3 (2019/3/28)")
        self.openFormula.setText("수식 파일 열기")
        self.export.setText("태그 목록 내보내기")
        self.startCalc.setText("동별 계산 시작")
        self.pauseCalc.setText("일시중지")
        self.abortCalc.setText("중단")
        self.export.setDisabled(True)
        self.startCalc.setDisabled(True)
        self.pauseCalc.setDisabled(True)
        self.abortCalc.setDisabled(True)
        self.calcStatusText = {'initial':'동별 산출식 파일을 불러오세요', 'fileOpened':"산출식 파일이 열렸습니다. 태그 목록표를 다운로드할 수 있습니다."}
        self.calcStatusLabel.setText(self.calcStatusText['initial'])
        self.startLabel.setText("시작일자")
        self.endLabel.setText("종료일자")
        self.startRetrieve.setText("목록 불러오기")
        self.pauseRetrieve.setText("일시중지")
        self.pauseRetrieve.setDisabled(True)
        self.abortRetrieve.setText("중단")
        self.abortRetrieve.setDisabled(True)
        self.whetherRounded.setText("결과값 반올림하여 저장")
        self.whetherRounded.setDisabled(True)
        self.changeEncoding.setText("cp949로 저장(기본 utf-8)")
        self.saveLogButton.setText("로그 저장")
        self.saveLogButton.setDisabled(True)
        self.clearButton.setText("초기화")
        self.exitButton.setText("종료")

        self.progressShow.setValue(0)
        self.progressShow.setVisible(False)

        self.statusBar.showMessage('준비')

        self.tabWidget.currentChanged.connect(self.tabChangedFunc)

        self.openFormula.clicked.connect(self.openFormulaFunc)
        self.export.clicked.connect(self.exportFunc)
        self.startCalc.clicked.connect(self.startCalcFunc)
        self.pauseCalc.clicked.connect(self.pauseCalcFunc)
        self.abortCalc.clicked.connect(self.abortCalcFunc)

        self.startRetrieve.clicked.connect(self.startRetrieveFunc)
        self.pauseRetrieve.clicked.connect(self.pauseRetrieveFunc)
        self.abortRetrieve.clicked.connect(self.abortRetrieveFunc)

        self.saveLogButton.clicked.connect(self.saveLogFunc)
        self.clearButton.clicked.connect(self.clearFunc)
        self.exitButton.clicked.connect(self.exitFunc)

        self.whetherRounded.stateChanged.connect(self.checkRounding)

        self.retrieveTagList = ""
        self.formulaTable = ""
        self.sessionList = []

        self.splitRegex = re.compile(r' - | \+ ')

    def checkRounding(self):
        if self.tabWidget.currentIndex() == 0 :
            self.saveAsRounded['calc'] = self.whetherRounded.isChecked()
        else :
            self.saveAsRounded['crawler'] = self.whetherRounded.isChecked()

    def returnEncoding(self):
        if self.changeEncoding :
            return 'cp949'
        else :
            return 'utf-8'


    @QtCore.pyqtSlot(str)
    def finishedWell(self, origin):
        if origin == 'calc' :
            self.calcStatus['isRunning'] = False
            self.openFormula.setEnabled(True)
            self.startCalc.setEnabled(True)
            self.pauseCalc.setEnabled(False)
            self.abortCalc.setEnabled(False)
            self.clearButtonEnabled['calc'] = True
            self.clearButton.setEnabled(self.clearButtonEnabled['calc'])
            self.roundBoxEnabled['calc'] = True
            self.whetherRounded.setEnabled(self.roundBoxEnabled['calc'])
        else :
            self.retrieveStatus['isRunning'] = False
            self.startRetrieve.setEnabled(True)
            self.pauseRetrieve.setEnabled(False)
            self.abortRetrieve.setEnabled(False)
            self.clearButtonEnabled['crawler'] = True
            self.clearButton.setEnabled(self.clearButtonEnabled['crawler'])
            self.roundBoxEnabled['crawler'] = True
            self.whetherRounded.setEnabled(self.roundBoxEnabled['crawler'])
            self.sessionList[0].close()

    @QtCore.pyqtSlot(tuple)
    def updateStatusBar(self, statusTuple):
        self.changeStatusMessage(statusTuple)

    def changeStatusMessage(self, statusTuple):
        text = statusTuple[0]
        origin = statusTuple[1]
        if origin == 'calc' :
            self.calcStatusBarMessage = text
        else :
            self.crawlerStatusBarMessage = text
        if self.tabWidget.currentIndex() == 0 :
            self.statusBar.showMessage(self.calcStatusBarMessage)
        else :
            self.statusBar.showMessage(self.crawlerStatusBarMessage)

    def showTable(self, tableData):
        if type(tableData) == str :
            self.tableWidget.setRowCount(0)
            self.tableWidget.setColumnCount(0)
        else :
            size = tableData.shape
            self.tableWidget.setRowCount(size[0])
            self.tableWidget.setColumnCount(size[1])
            self.tableWidget.setVerticalHeaderLabels(tableData.index.astype(str))
            self.tableWidget.setHorizontalHeaderLabels(tableData.columns.astype(str))

            for rowNum in range(size[0]):
                for colNum in range(size[1]):
                    self.tableWidget.setItem(rowNum, colNum,
                                              QtWidgets.QTableWidgetItem(str(tableData.iloc[rowNum, colNum])))

            self.tableWidget.resizeRowsToContents()
            self.tableWidget.resizeColumnsToContents()

    def readTable(self, fileName):
        try:
            res = pd.read_csv(fileName, index_col=0, engine='python').apply(pd.to_numeric, errors='coerce').fillna(
                0)
        except UnicodeDecodeError:
            res = pd.read_csv(fileName, encoding='cp949', index_col=0, engine='python').apply(pd.to_numeric,
                                                                                              errors='coerce').fillna(
                0)
        return res

    def openFormulaFunc(self):
        name, _ = QtWidgets.QFileDialog.getOpenFileName(self, '산출식 파일 열기', filter="Excel file (*.xlsx *.xls)")
        if name:
            # try:
            #     name.encode("ascii")
            # except UnicodeEncodeError:
            #     QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류",
            #                                   "파일 경로 또는 파일 이름에 한글이 포함되어 있으면 파일을 열 수 없습니다.",
            #                                   QtWidgets.QMessageBox.Ok)
            #     return

            formula = pd.read_excel(name, encoding = sys.getfilesystemencoding())

            if formula.shape[1] != 2:
                QtWidgets.QMessageBox.warning(self.centralwidget, "파일 형식 오류", "지원하지 않는 형식의 파일입니다.",
                                              QtWidgets.QMessageBox.Ok)
                return
        else:
            QtWidgets.QMessageBox.warning(self.centralwidget, "파일 오류", "잘못된 파일이거나 파일이 선택되지 않았습니다.",
                                          QtWidgets.QMessageBox.Ok)
            return

        self.changeStatusMessage(("총 " + str(formula.shape[0]) + "개 동", 'calc'))
        self.formulaTable = formula
        self.showTable(self.formulaTable)

        tagsForCalc = []

        for row in formula.iterrows() :
            tempString = row[1][1]
            # print(row[1][0])
            tempList = [x.strip() for x in re.split(self.splitRegex, tempString)]
            for tag in tempList :
                t = tag.split()
                t.append(tag)
                # print(len(t))
                tagsForCalc.append(t)

        tagsForCalcTable = pd.DataFrame(tagsForCalc).drop_duplicates()

        tagsForCalcTable.columns = ['건물동', '태그명', '전체 태그명']

        self.tagsForCalcTable = tagsForCalcTable

        self.export.setEnabled(True)
        self.startCalc.setEnabled(True)
        self.roundBoxEnabled['calc'] = True
        self.whetherRounded.setEnabled(self.roundBoxEnabled['calc'])
        self.calcStatusLabel.setText(self.calcStatusText['fileOpened'])

    def exportFunc(self):
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self, '태그 목록 저장', filter="Excel file (*.xlsx *.xls)")
        if name:
            # try:
            #     name.encode("ascii")
            # except UnicodeEncodeError:
            #     QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류",
            #                                   "파일 경로 또는 파일 이름에 한글이 포함되어 있으면 파일을 저장할 수 없습니다.",
            #                                   QtWidgets.QMessageBox.Ok)
            #     return

            self.tagsForCalcTable.iloc[:, :2].to_excel(name, index=False)

        else:
            return

    @QtCore.pyqtSlot(tuple)
    def updateProgressValue(self, valueTuple):
        if valueTuple[1] == 'calc' :
            self.progressValue['calc'] = valueTuple[0]
            self.progressShow.setValue(self.progressValue['calc'])
        else :
            self.progressValue['crawler'] = valueTuple[0]
            self.progressShow.setValue(self.progressValue['crawler'])

    def startCalcFunc(self):
        folderName = QtWidgets.QFileDialog.getExistingDirectory(self, "태그 정보 저장 폴더 열기")

        if folderName == "":
            return
        else :
            tagFolderContent = listdir(folderName)
            notExist = []
            allTagFiles = {}
            fileShape = []
            for tagName in self.tagsForCalcTable['전체 태그명']:
                if tagName + '.csv' in tagFolderContent :
                    read = self.readTable(folderName + '/' + tagName + '.csv')
                    read.apply(pd.to_numeric, errors='coerce').fillna(0)
                    allTagFiles[tagName] = read
                    readShape = (read.index.tolist(), read.columns.tolist())
                    if readShape not in fileShape :
                        fileShape.append(readShape)
                else :
                    notExist.append(tagName)

            if notExist :
                QtWidgets.QMessageBox.warning(self.centralwidget, "태그 파일 없음", '다음 태그 파일이 없습니다.\n'+ "\n".join(notExist),
                                              QtWidgets.QMessageBox.Ok)
                return

            if len(fileShape) != 1 :
                QtWidgets.QMessageBox.warning(self.centralwidget, "태그 파일 형식 다름", '태그 파일 간의 열과 행이 다릅니다.\n'+ "\n".join(notExist),
                                              QtWidgets.QMessageBox.Ok)
                return

            go = QtWidgets.QMessageBox.question(self.centralwidget, "계산 실행", \
                                                '입력한 조건대로 계산을 시작할까요?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes)
            if go == QtWidgets.QMessageBox.Yes:
                self.calcStatusLabel.setText(folderName)
            else:
                self.calcStatusLabel.setText(self.calcStatusText['fileOpened'])
                return

            self.openFormula.setDisabled(True)
            self.startCalc.setDisabled(True)
            self.pauseCalc.setEnabled(True)
            self.abortCalc.setEnabled(True)

            self.clearButtonEnabled['calc'] = False
            self.clearButton.setEnabled(self.clearButtonEnabled['calc'])
            self.roundBoxEnabled['calc'] = False
            self.whetherRounded.setEnabled(self.roundBoxEnabled['calc'])

            self.allTagFiles = allTagFiles

            self.calcEngine = Calculator(self.calcStatus, self.allTagFiles, self.formulaTable, self.saveAsRounded['calc'], self.splitRegex, self.returnEncoding())
            self.calcEngine.updateStatusSignal.connect(self.updateStatusBar)
            self.calcEngine.finishedSignal.connect(self.finishedWell)

            self.calcStatus['isRunning'] = True

            self.calcEngine.start()
            

    def pauseCalcFunc(self):
        if self.calcStatus['isPaused'] :
            self.calcStatus['isPaused'] = False
            self.pauseCalc.setText("일시중지")
        else :
            self.calcStatus['isPaused'] = True
            self.pauseCalc.setText("다시 시작")

    def abortCalcFunc(self):
        self.calcStatus['isRunning'] = False
        self.calcStatus['isPaused'] = False
        self.openFormula.setEnabled(True)
        self.startCalc.setEnabled(True)
        self.pauseCalc.setEnabled(False)
        self.pauseCalc.setText("일시중지")
        self.abortCalc.setEnabled(False)
        self.clearButtonEnabled['calc'] = True
        self.clearButton.setEnabled(self.clearButtonEnabled['calc'])
        self.changeStatusMessage(("준비", 'calc'))
        self.roundBoxEnabled['calc'] = True
        self.whetherRounded.setEnabled(self.roundBoxEnabled['calc'])

    def tabChangedFunc(self):
        if self.tabWidget.currentIndex() == 0 :
            self.whetherRounded.setEnabled(self.roundBoxEnabled['calc'])
            self.whetherRounded.setChecked(self.saveAsRounded['calc'])
            self.clearButton.setEnabled(self.clearButtonEnabled['calc'])
            self.statusBar.showMessage(self.calcStatusBarMessage)
            self.progressShow.setVisible(self.progressVisible['calc'])
            self.progressShow.setValue(self.progressValue['calc'])
            self.showTable(self.formulaTable)
        else :
            self.whetherRounded.setEnabled(self.roundBoxEnabled['crawler'])
            self.whetherRounded.setChecked(self.saveAsRounded['crawler'])
            self.clearButton.setEnabled(self.clearButtonEnabled['crawler'])
            self.statusBar.showMessage(self.crawlerStatusBarMessage)
            self.progressShow.setVisible(self.progressVisible['crawler'])
            self.progressShow.setValue(self.progressValue['crawler'])
            self.showTable(self.retrieveTagList)

    def makeConnection(self, address, data, header, sessionList, whatToFind = 'result', expectedRes = 'matched') :
        session = sessionList[0]
        while True : 
            temp = session.post(address, data=data, headers = header)
            if BeautifulSoup(temp.text, 'xml').find(whatToFind).get_text() == expectedRes :
                temp.close()
                break

    def startRetrieveFunc(self):
        if self.startRetrieve.text() == "시작" :
            self.startDate_dateModule = date(self.startDate.date().year(), self.startDate.date().month(),
                                             self.startDate.date().day())
            self.endDate_dateModule = date(self.endDate.date().year(), self.endDate.date().month(),
                                           self.endDate.date().day())

            period = (self.endDate_dateModule - self.startDate_dateModule).days + 1

            if period < 1 :
                QtWidgets.QMessageBox.warning(self.centralwidget, "기간 설정 오류", "기간 설정이 잘못되어 있습니다.",
                                              QtWidgets.QMessageBox.Ok)
                return


            go = QtWidgets.QMessageBox.question(self.centralwidget, "수집 실행", \
                                                '입력한 조건대로 수집을 시작할까요?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.Yes)

            if go == QtWidgets.QMessageBox.Yes:
                pass
            else:
                return

            self.startRetrieve.setDisabled(True)
            self.pauseRetrieve.setEnabled(True)
            self.abortRetrieve.setEnabled(True)

            self.clearButtonEnabled['crawler'] = False
            self.clearButton.setEnabled(self.clearButtonEnabled['crawler'])
            self.roundBoxEnabled['crawler'] = False
            self.whetherRounded.setEnabled(self.roundBoxEnabled['crawler'])

            self.sessionList = [requests.Session()]

            self.retrieveEngine = Crawler(self.retrieveStatus, self.retrieveTagList, self.startDate_dateModule, period, self.saveAsRounded['crawler'],
                                          self.sessionList, self.returnEncoding())
            self.retrieveEngine.updateStatusSignal.connect(self.updateStatusBar)
            self.retrieveEngine.finishedSignal.connect(self.finishedWell)
            self.retrieveEngine.invalidTagsSignal.connect(self.popMessageBox)
            self.retrieveEngine.updateProgressValue.connect(self.updateProgressValue)

            self.retrieveStatus['isRunning'] = True
            # self.progressVisible['crawler'] = True
            # self.progressShow.setVisible(self.progressVisible['crawler'])

            if self.retrieveConnected :
                pass
            else :
                """실제 프로그램 구동부에는 값이 존재하지만 게시에 적절하지 않은 내용이 있어 모두 주석처리하고 내용은 삭제했습니다"""
                # userLoginAddress = 
                # userLoginHeader = 
                # userLoginData = 

                # self.makeConnection(userLoginAddress, userLoginData, userLoginHeader, self.sessionList, 'CheckUserNameResult', 'true')

                self.retrieveConnected = True

            self.retrieveEngine.start()

        else :
            name, _ = QtWidgets.QFileDialog.getOpenFileName(self, '태그 목록 열기', filter = "Excel file (*.xlsx *.xls)")
            if name:
                # try:
                #     name.encode("ascii")
                # except UnicodeEncodeError:
                #     QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류",
                #                                   "파일 경로 또는 파일 이름에 한글이 포함되어 있으면 파일을 열 수 없습니다.",
                #                                   QtWidgets.QMessageBox.Ok)
                #     return

                tagList = pd.read_excel(name, encoding=sys.getfilesystemencoding())

                if tagList.shape[1] != 2:
                    QtWidgets.QMessageBox.warning(self.centralwidget, "파일 형식 오류", "지원하지 않는 형식의 파일입니다.",
                                                  QtWidgets.QMessageBox.Ok)
                    return
            else:
                QtWidgets.QMessageBox.warning(self.centralwidget, "파일 오류", "잘못된 파일이거나 파일이 선택되지 않았습니다.",
                                              QtWidgets.QMessageBox.Ok)
                return

            self.changeStatusMessage(("총 " + str(tagList.shape[0]) + "개 태그", 'crawler'))
            self.retrieveTagList = tagList
            self.showTable(self.retrieveTagList)
            self.startRetrieve.setText("시작")
            self.roundBoxEnabled['crawler'] = True
            self.whetherRounded.setEnabled(True)

    def pauseRetrieveFunc(self):
        if self.retrieveStatus['isPaused'] :
            self.retrieveStatus['isPaused'] = False
            self.pauseRetrieve.setText("일시중지")
        else :
            self.retrieveStatus['isPaused'] = True
            self.pauseRetrieve.setText("다시 시작")

    def abortRetrieveFunc(self):
        self.retrieveStatus['isRunning'] = False
        self.retrieveStatus['isPaused'] = False
        self.sessionList[0].close()
        self.startRetrieve.setEnabled(True)
        self.pauseRetrieve.setEnabled(False)
        self.pauseRetrieve.setText("일시중지")
        self.abortRetrieve.setEnabled(False)
        self.clearButtonEnabled['crawler'] = True
        self.clearButton.setEnabled(self.clearButtonEnabled['crawler'])
        self.changeStatusMessage(("준비", 'crawler'))
        self.roundBoxEnabled['crawler'] = True
        self.whetherRounded.setEnabled(self.roundBoxEnabled['crawler'])

    def clearFunc(self):
        if self.tabWidget.currentIndex() == 0 :
            self.formulaTable = ""
            self.showTable(self.formulaTable)
            self.startCalc.setDisabled(True)
            self.pauseCalc.setDisabled(True)
            self.abortCalc.setDisabled(True)
            self.export.setDisabled(True)
            self.changeStatusMessage(("준비", 'calc'))
            self.roundBoxEnabled['calc'] = False
            self.whetherRounded.setEnabled(self.roundBoxEnabled['calc'])
            self.calcStatusLabel.setText(self.calcStatusText['initial'])
        else :
            self.retrieveTagList = ""
            self.showTable(self.retrieveTagList)
            self.startRetrieve.setText("목록 불러오기")
            self.pauseRetrieve.setDisabled(True)
            self.abortRetrieve.setDisabled(True)
            self.sessionList = []
            self.changeStatusMessage(("준비", 'crawler'))
            self.roundBoxEnabled['crawler'] = False
            self.whetherRounded.setEnabled(self.roundBoxEnabled['crawler'])
            self.retrieveConnected = False
            self.progressValue['crawler'] = 0
            self.progressVisible['crawler'] = False
            self.progressShow.setValue(self.progressValue['crawler'])
            self.progressShow.setVisible(self.progressVisible['crawler'])
        self.changeEncoding.setChecked(False)

    def saveLogFunc(self):
        pass

    def exitFunc(self):
        sys.exit()

    @QtCore.pyqtSlot(tuple)
    def popMessageBox(self, messageTuple):
        if messageTuple[1] == 'crawler' :
            resMessage = QtWidgets.QMessageBox(self.centralwidget)
            resMessage.setIcon(QtWidgets.QMessageBox.Warning)
            resMessage.setWindowTitle("정보가 없는 태그")
            resMessage.setText("주어진 기간 내에서 다음 태그의 시간대별 수치는 모두 같습니다.\n추가적인 확인이 필요할 수 있습니다.\n")
            resMessage.setStandardButtons(QtWidgets.QMessageBox.Ok)
            resMessage.setDetailedText(messageTuple[0])
            resMessage.open()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    ui.show()
    sys.exit(app.exec_())

