import startCapsule as strtCpsl
import correctionProgram_190425 as crcPrgm
import controller as ctrlr

from PyQt5 import QtCore, QtGui, QtWidgets

import pandas as pd
import sys
import os

import pickle

# from datetime import datetime


class GetDataDialog(strtCpsl.Ui_Dialog) :
    successfullyLoaded = QtCore.pyqtSignal(str)
    connectionLost = QtCore.pyqtSignal(str)

    def __init__(self, engine):
        super().__init__()
        self.engine = engine[0]
        self.newPaths = {'bldg': "", 'meta': "", 'reseted':False}
        self.beforePaths = {'bldg': "", 'meta': "", 'saved': False}
        self.pathChanged = {'bldg':False, 'meta':False}


    def getFilePath(self, whereToShow):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(self, "파일 불러오기", filter="csv 파일 (*.csv)")
        if fileName :
            if whereToShow == 'bldg' :
                self.bldgPath.setText(fileName)
                self.newPaths['bldg'] = fileName
                self.pathChanged['bldg'] = True
            else :
                self.metaPath.setText(fileName)
                self.newPaths['meta'] = fileName
                self.pathChanged['meta'] = True

    def reset(self):
        super().reset()
        self.newPaths['bldg'] = ""
        self.pathChanged['bldg'] = True

        self.newPaths['meta'] = ""
        self.pathChanged['meta'] = True

        self.newPaths['reseted'] = True



    def accept(self):
        if self.pathChanged['bldg'] :
            self.beforePaths['bldg'] = self.newPaths['bldg']
            if self.newPaths['bldg'] :
                self.engine.readFile(self.newPaths['bldg'], 'bldg')
                self.successfullyLoaded.emit('bldg')
            else :
                self.engine.elecData = ""
                self.connectionLost.emit('bldg')

        if self.pathChanged['meta'] :
            self.beforePaths['meta'] = self.newPaths['meta']
            if self.newPaths['meta'] :
                self.engine.readFile(self.newPaths['meta'], 'meta')
                self.successfullyLoaded.emit('meta')
            else :
                self.engine.metaData = ""
                self.connectionLost.emit('meta')

        if self.checkBox.isChecked() :
            self.beforePaths['saved'] = True
            if self.pathChanged['bldg'] or self.pathChanged['meta'] :
                with open("_filepath.pkl", 'wb') as f:
                    pickle.dump(self.beforePaths, f)

        if self.newPaths['reseted'] :
            self.beforePaths['saved'] = False
            with open("_filepath.pkl", 'wb') as f:
                pickle.dump(self.beforePaths, f)

        self.pathChanged['bldg'] = False
        self.pathChanged['meta'] = False
        self.newPaths['reseted'] = False

        super().accept()


    def reject(self):
        self.bldgPath.setText(self.beforePaths['bldg'])
        self.newPaths['bldg'] = ""
        self.metaPath.setText(self.beforePaths['meta'])
        self.newPaths['meta'] = ""

        self.newPaths['reseted'] = False
        self.checkBox.setChecked(self.beforePaths['saved'])
        self.pathChanged['bldg'] = False
        self.pathChanged['meta'] = False

        super().reject()


class MainProgram(crcPrgm.Ui_MainWindow) :
    def __init__(self):
        super().__init__()
        self.dataConnected = {'bldg':False, 'meta':False}
        self.programStatus = {'isRunning':False, 'isPaused':False}
        self.statusMessages = {'default': '데이터 연결됨', 'notBldg': '전력 데이터가 연결되어 있지 않습니다',
                               'notMeta': '건물 데이터가 연결되어 있지 않습니다', 'notConnected': '데이터가 연결되어 있지 않습니다'}

        self.engine = ctrlr.Engine(self.programStatus)

        self.engine.sendTableFrameInfo.connect(self.updateTableFrame)
        self.engine.sendValueForSingleCell.connect(self.updateTableCellValue)
        self.engine.tableShowFinished.connect(self.makeTableFitted)
        self.engine.hideRowSignal.connect(self.hideRowInTable)
        self.engine.changeStatusbarMessageSignal.connect(self.updateStatusbarMessage)

        self.dataGetter = GetDataDialog([self.engine])

        self.chooseCategoryComboBox.addItem("전체")
        self.chooseCategoryComboBox.addItem("기관별")
        self.chooseCategoryComboBox.addItem("용도별")

        # self.currentlyShownBldgs = []
        self.buildingForCorrection = []
        self.inputForCorrectionEngine = {}

        self.dataGetter.successfullyLoaded.connect(self.connectionSuccessful)
        self.dataGetter.connectionLost.connect(self.connectionFailed)

        self.chooseCategoryComboBox.currentTextChanged.connect(self.changeAccordingToCategory)
        self.chooseDetailComboBox.currentTextChanged.connect(self.changeAccordingToDetail)

        self.initialize()

    def initialize(self):
        if os.path.isfile('_filepath.pkl'):
            with open('_filepath.pkl', 'rb') as f :
                self.dataGetter.beforePaths = pickle.load(f)
                if self.dataGetter.beforePaths['saved'] :
                    self.dataGetter.checkBox.setChecked(True)
                    if self.dataGetter.beforePaths['bldg'] :
                        if os.path.isfile(self.dataGetter.beforePaths['bldg']) :
                            self.dataGetter.bldgPath.setText(self.dataGetter.beforePaths['bldg'])
                            self.engine.readFile(self.dataGetter.beforePaths['bldg'], 'bldg')
                            self.dataConnected['bldg'] = True
                    if self.dataGetter.beforePaths['meta'] :
                        if os.path.isfile(self.dataGetter.beforePaths['meta']) :
                            self.dataGetter.metaPath.setText(self.dataGetter.beforePaths['meta'])
                            self.engine.readFile(self.dataGetter.beforePaths['meta'], 'meta')
                            self.dataConnected['meta'] = True

        else :
            print('file Not Found')

        self.statusControl()
        self.makeSettings()

    def statusControl(self):
        if self.dataConnected['bldg'] :
            if self.dataConnected['meta'] :
                self.statusbar.showMessage(self.statusMessages['default'])
            else :
                self.statusbar.showMessage(self.statusMessages['notMeta'])
        else :
            if self.dataConnected['meta'] :
                self.statusbar.showMessage(self.statusMessages['notBldg'])
            else :
                self.statusbar.showMessage(self.statusMessages['notConnected'])


    @QtCore.pyqtSlot(str)
    def connectionSuccessful(self, fileType):
        if fileType == 'bldg' :
            self.dataConnected['bldg'] = True
        else :
            self.dataConnected['meta'] = True

        self.statusControl()

    @QtCore.pyqtSlot(str)
    def connectionFailed(self, fileType):
        if fileType == 'bldg' :
            self.dataConnected['bldg'] = False
        else :
            self.dataConnected['meta'] = False

        self.statusControl()


    def dataConnectCheck(self):
        print('button pressed')
        t = self.dataGetter.exec_()
        if t :
            self.makeSettings()

    def makeSettings(self):
        if self.dataConnected['bldg'] and self.dataConnected['meta']:
            self.engine.parseMeta()

            self.chooseCampusComboBox.clear()
            self.chooseDetailComboBox.clear()

            for item in self.engine.listOfCampuses :
                self.chooseCampusComboBox.addItem(item)


    def changeAccordingToCategory(self, text):
        self.chooseDetailComboBox.clear()

        if text == '기관별' :
            for item in self.engine.listOfDepts :
                self.chooseDetailComboBox.addItem(item)
        else :
            for item in self.engine.listOfUsages :
                self.chooseDetailComboBox.addItem(item)


    def changeAccordingToDetail(self, text):
        self.showBuildingList.clear()
        # self.currentlyShownBldgs = []

        if self.chooseCategoryComboBox.currentText() == "기관별" :
            temp = self.engine.metaData.loc[self.engine.metaData.loc[:,'기관'] == text]
            for itemRow in temp.iterrows() :
                self.showBuildingList.addItem(itemRow[1]['item'])
                # self.currentlyShownBldgs.append(itemRow[1]['동 번호'])

        elif self.chooseCategoryComboBox.currentText() == "용도별" :
            temp = self.engine.metaData.loc[self.engine.metaData.loc[:,'용도'] == text]
            for itemRow in temp.iterrows() :
                self.showBuildingList.addItem(itemRow[1]['item'])
                # self.currentlyShownBldgs.append(itemRow[1]['동 번호'])

        else : 
            self.chooseDetailComboBox.clear()
            for itemRow in self.engine.metaData.iterrows():
                self.showBuildingList.addItem(itemRow[1]['item'])
                # self.currentlyShownBldgs.append(itemRow[1]['동 번호'])

    def addToCorrectionList(self, selected):
        for bldg in selected:
            if bldg in self.buildingForCorrection:
                pass
            else:
                self.buildingForCorrection.append(bldg)
                self.buildingForCorrectionList.addItem(bldg)

    def addSelected(self):
        selectedItems = [x.text() for x in self.showBuildingList.selectedItems()]
        self.addToCorrectionList(selectedItems)

    def addEntire(self):
        self.showBuildingList.selectAll()
        self.addSelected()

    def deleteFromCorrectionList(self, selected):
        for name in selected:
            self.buildingForCorrection.remove(name)

        self.buildingForCorrectionList.clear()
        if self.buildingForCorrection :
            self.buildingForCorrectionList.addItems(self.buildingForCorrection)

    def deleteSelected(self):
        selectedItems = [x.text() for x in self.buildingForCorrectionList.selectedItems()]
        self.deleteFromCorrectionList(selectedItems)

    def deleteEntire(self):
        self.buildingForCorrectionList.selectAll()
        self.deleteSelected()

    def startPauseToggle(self):
        if not self.programStatus['isRunning'] :
            self.programStatus['isRunning'] = True
            self.clearAbortButton.setText('중단')
            self.startPauseCorrectionButton.setText("일시중지")

            self.startCorrection()

        else :
            if self.programStatus['isPaused']:
                self.programStatus['isPaused'] = False
                self.startPauseCorrectionButton.setText("일시중지")

            else :
                self.programStatus['isPaused'] = True
                self.startPauseCorrectionButton.setText("다시 시작")

    def startCorrection(self):
    #     self.inputForCorrectionEngine['startDate'] = datetime(self.startDateEdit.date().year(), self.startDateEdit.date().month(), self.startDateEdit.date().day())
    #     self.inputForCorrectionEngine['endDate'] = datetime(self.endDateEdit.date().year(), self.endDateEdit.date().month(), self.endDateEdit.date().day())

        self.inputForCorrectionEngine['startDate'] = self.startDateEdit.date().toString('yyyy-MM-dd')
        self.inputForCorrectionEngine['endDate'] = self.endDateEdit.date().toString('yyyy-MM-dd')


        if self.abnormal_IQR_checkbox.isChecked() :
            if self.yesInterpolationRadioButton.isChecked() :
                self.inputForCorrectionEngine['iqr'] = 'yesInterpolate'
            else :
                self.inputForCorrectionEngine['iqr'] = 'noInterpolate'
        else :
            self.inputForCorrectionEngine['iqr'] = ""

        if self.abnormal_ND_checkbox.isChecked():
            self.inputForCorrectionEngine['ndist'] = self.reliabilitySpinBox.value()/100.0
        else :
            self.inputForCorrectionEngine['ndist'] = ""

        self.inputForCorrectionEngine['valueType'] = self.replacementOptionComboBox.currentText()
        self.inputForCorrectionEngine['whichBldgs'] = [x.split("동")[0] for x in self.buildingForCorrection]

        self.inputForCorrectionEngine['startValue'] = self.startRangeSpinBox.value()
        self.inputForCorrectionEngine['endValue'] = self.endRangeSpinBox.value()
        self.inputForCorrectionEngine['dynamicalError'] = self.dynamicalErrorCheckbox.isChecked()

        self.engine.settingsForCorrection = self.inputForCorrectionEngine

        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)

        self.engine.start()


    @QtCore.pyqtSlot(dict)
    def updateTableFrame(self, frameInfo):
        if 'row' in frameInfo :
            self.dataTable.setRowCount(len(frameInfo['row']))
            self.dataTable.setVerticalHeaderLabels(frameInfo['row'])
        if 'col' in frameInfo :
            self.dataTable.setColumnCount(len(frameInfo['col']))
            self.dataTable.setHorizontalHeaderLabels(frameInfo['col'])

    @QtCore.pyqtSlot(tuple)
    def updateTableCellValue(self, cellInfo):
        self.dataTable.setItem(cellInfo[0], cellInfo[1], QtWidgets.QTableWidgetItem(str(cellInfo[2])))

    @QtCore.pyqtSlot()
    def makeTableFitted(self) : 
        self.dataTable.resizeRowsToContents()
        self.dataTable.resizeColumnsToContents()

    @QtCore.pyqtSlot(int)
    def hideRowInTable(self, rowNum):
        self.dataTable.setRowHidden(rowNum, True)

    @QtCore.pyqtSlot(str)
    def updateStatusbarMessage(self, message):
        self.statusbar.showMessage(message)

    def clearAbortToggle(self):
        if self.programStatus['isRunning']:
            self.programStatus['isRunning'] = False
            self.programStatus['isPaused'] = False
            self.startPauseCorrectionButton.setText("보정 시작")
            self.clearAbortButton.setText('초기화')

    # def showTable(self, tableData):
    #     if type(tableData) == str :
    #         self.tableWidget.setRowCount(0)
    #         self.tableWidget.setColumnCount(0)
    #     else :
    #         size = tableData.shape
    #         self.tableWidget.setRowCount(size[0])
    #         self.tableWidget.setColumnCount(size[1])
    #         self.tableWidget.setVerticalHeaderLabels(tableData.index.astype(str))
    #         self.tableWidget.setHorizontalHeaderLabels(tableData.columns.astype(str))

    #         for rowNum in range(size[0]):
    #             for colNum in range(size[1]):
    #                 self.tableWidget.setItem(rowNum, colNum,
    #                                           QtWidgets.QTableWidgetItem(str(tableData.iloc[rowNum, colNum])))

    #         self.tableWidget.resizeRowsToContents()
    #         self.tableWidget.resizeColumnsToContents()



if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    ui = MainProgram()
    ui.show()

    sys.exit(app.exec_())