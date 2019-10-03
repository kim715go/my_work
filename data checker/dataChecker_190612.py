# "전력량 초기 보정 및 그래프 확인 프로그램 v.1.0.3 (2019/6/11)"
# v 1.0.1 수정사항 : 현재 활성화된 파일이 목록에서 제거되었을 때 다른 기능이 작동하지 않도록 함 (2019/5/15)
# v 1.0.2 수정사항 : 목록에만 있고 열리지 않은 파일을 목록에서 제거하려고 할 때 발생하는 에러 제거 (2019/6/5)
# v 1.0.3 수정사항 : 파일을 목록에서 제거한 후 그래프를 이동시키려고 표를 더블클릭할 때 발생하는 에러 제거 (2019/6/11)
# v 1.0.4 수정사항 : 파일 목록 중 존재하지 않는 파일을 열려고 할 때 발생하는 에러 제거 (2019/6/12)
# v 1.0.5 수정사항 : 데이터 stack 과정에서 인덱싱 관련 오류 수정(연속된 데이터만 인풋으로 들어올 것이라는 가정 삭제) (2019/8/21)

import matplotlib as mpl
mpl.rc('font', family = 'HCR Dotum')

import pandas as pd

import userInterface as uI
from PyQt5 import QtCore, QtGui, QtWidgets

from statsmodels.tsa.seasonal import seasonal_decompose
import numpy as np

from scipy.stats import norm
from matplotlib.pyplot import figure, close

def zero_runs(a):
    # Create an array that is 1 where a is 0, and pad each end with an extra 0.
    iszero = np.concatenate(([0], np.equal(a, 0).view(np.int8), [0]))
    absdiff = np.abs(np.diff(iszero))
    # Runs start and end where absdiff is 1.
    ranges = np.where(absdiff == 1)[0].reshape(-1, 2)
    return ranges # return format example : [[1, 3], [5, 8], [9, 10]]

class SettingDialog(QtWidgets.QDialog):
    def __init__(self, variables):
        super().__init__()

        self.variables = variables
        self.resize(280, 100)
        self.setMinimumSize(QtCore.QSize(280, 100))
        self.setMaximumSize(QtCore.QSize(280, 100))
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.sameConsecLabel = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.sameConsecLabel, 0, 0, 1, 1)
        self.credibLabel = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.credibLabel, 1, 0, 1, 1)
        self.sameConsecSpinBox = QtWidgets.QSpinBox(self)
        self.gridLayout.addWidget(self.sameConsecSpinBox, 0, 1, 1, 1)
        self.credibSpinBox = QtWidgets.QDoubleSpinBox(self)
        self.gridLayout.addWidget(self.credibSpinBox, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslateUi(self):
        self.setWindowTitle("세부 설정")
        self.sameConsecLabel.setText("동일 측정값 이상 기준 횟수")
        self.credibLabel.setText("오류 검출 신뢰도")
        self.credibSpinBox.setSuffix("%")

        self.sameConsecSpinBox.setValue(self.variables['sameConsec'])
        self.credibSpinBox.setValue(self.variables['credibility']*100)

    def accept(self):
        self.variables['sameConsec'] = self.sameConsecSpinBox.value()
        self.variables['credibility'] = self.credibSpinBox.value()/100
        super().accept()


class Kernel(uI.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("전력량 초기 보정 및 그래프 확인 프로그램 v.1.0.4 (2019/6/12)")

        self.filePathList = []
        self.statusMessage = "준비"

        self.initialFileTables = {}
        self.parsedFileTables = {}

        self.currentPath = ""
        self.currentGraphSaveFolderPath = ""
        self.currentDataSaveFolderPath = ""

        self.settingVars = {'sameConsec':6, 'credibility':.99}
        self.showOutlierCheckBox.setChecked(True)
        self.onlyCurrentRadioButton.setChecked(True)

        self.buildingForCorrectionList.itemDoubleClicked.connect(self.fileNameDoubleClicked)
        self.buildingForCorrectionList.itemClicked.connect(self.fileNameClicked)

        self.statusbar.showMessage(self.statusMessage)

        self.dataTableIndex = self.dataTable.verticalHeader()
        self.dataTableIndex.sectionDoubleClicked.connect(self.moveGraphTo)

        self.dataTableColumns = self.dataTable.horizontalHeader()
        self.dataTableColumns.sectionDoubleClicked.connect(self.filterTo)

        self.dataTableScrollBar = self.dataTable.verticalScrollBar()
        # self.dataTableScrollBar.valueChanged.connect(self.recordCurrentScrollPosition)

        self.rowFiltered = False
        self.partialCorrectionEnabled = False
        self.correctionStartDateEdit.setEnabled(False)
        self.correctionEndDateEdit.setEnabled(False)

        self.dataTable.cellDoubleClicked.connect(self.toggleCondition)

        self.correctPartialCheckBox.stateChanged.connect(self.enablePartialCorrection)

        self.statusbar.showMessage(self.statusMessage)

    def openFiles(self):
        pathList, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "파일 불러오기", filter="csv 파일 (*.csv)")
        if pathList :
            for path in pathList :
                if path not in self.filePathList :
                    self.buildingForCorrectionList.addItem(path)
                    self.filePathList.append(path)

    def fileNameDoubleClicked(self, item): #always open the designated file... even if it has already been opened
        if self.currentPath in self.parsedFileTables :
            self.parsedFileTables[self.currentPath]['scrollPos'] = self.dataTableScrollBar.value()
        self.currentPath = item.text()
        table = self.openFile(self.currentPath)
        if type(table) is pd.DataFrame :
            self.parseInitialTable(self.currentPath, table)

    def fileNameClicked(self, item):
        path = item.text()
        if self.currentPath in self.parsedFileTables :
            self.parsedFileTables[self.currentPath]['scrollPos'] = self.dataTableScrollBar.value()

        if path in self.parsedFileTables and path != self.currentPath:
            self.currentPath = path
            self.reloadParsedTable(self.currentPath)

    def openFile(self, path):
        try :
            table = pd.read_csv(path, engine='python', index_col=0, parse_dates=True)
        except UnicodeDecodeError :
            table = pd.read_csv(path, engine='python', index_col=0, parse_dates=True, encoding='euc-kr')
        except FileNotFoundError :
            QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류", "주어진 경로의 파일이 존재하지 않습니다.\n" + path, QtWidgets.QMessageBox.Ok)
            return
        if table.shape[1] != 24 :
            QtWidgets.QMessageBox.warning(self.centralwidget, "올바르지 않은 파일 형식", "테이블의 형태가 활용 가능하지 않습니다", QtWidgets.QMessageBox.Ok)
            return
        else :
            return table

    def deleteFromCorrectionList(self, selected):
        for path in selected:
            if path in self.filePathList:
                self.filePathList.remove(path)
                if path in self.parsedFileTables :
                    del self.parsedFileTables[path]

        self.buildingForCorrectionList.clear()
        if self.filePathList :
            self.buildingForCorrectionList.addItems(self.filePathList)

    def deleteSelected(self):
        selectedItems = [x.text() for x in self.buildingForCorrectionList.selectedItems()]
        self.deleteFromCorrectionList(selectedItems)

    def deleteEntire(self):
        self.buildingForCorrectionList.selectAll()
        self.deleteSelected()

    def parseInitialTable(self, path, table, resNotShowing = False):
        table.columns = [str(x).zfill(2) for x in range(24)]
        temp = table.stack()
        temp.name="전력량"
        temp.index = pd.core.tools.datetimes.to_datetime([" ".join(x) for x in temp.index.to_native_types()])

        parsedTable = pd.DataFrame(temp)
        parsedTable['계차'] = temp.diff()
        parsedTable['이상'] = ""
        parsedTable['대체'] = temp.values

        res = {'table':parsedTable, 'decomposed':"", 'numOfErrorsInitial':0,
               'plotStart':"", 'plotEnd':"", 'redPoint':True, 'scrollPos':0}
            # table, seasonal decomposition, error num, graph start, graph end, whether red point, current scroll pos of table

        self.parsedFileTables[path] = res

        self.analyseTable(path, resNotShowing)

    def setDateRange(self, path, key):
        startDate_datetimeDate = self.parsedFileTables[path]['table'].index[0].date()
        endDate_datetimeDate = self.parsedFileTables[path]['table'].index[-1].date()

        startDate_QDate = QtCore.QDate(startDate_datetimeDate)
        endDate_QDate = QtCore.QDate(endDate_datetimeDate)

        if key == 'plot' :
            self.plotStartDateEdit.setMinimumDate(startDate_QDate)
            self.plotStartDateEdit.setMaximumDate(endDate_QDate)
            self.plotEndDateEdit.setMinimumDate(startDate_QDate)
            self.plotEndDateEdit.setMaximumDate(endDate_QDate)
        else :
            self.correctionStartDateEdit.setMinimumDate(startDate_QDate)
            self.correctionStartDateEdit.setMaximumDate(endDate_QDate)
            self.correctionEndDateEdit.setMinimumDate(startDate_QDate)
            self.correctionEndDateEdit.setMaximumDate(endDate_QDate)

    def setDate(self, startDate_QDate, endDate_QDate, key):
        if key == 'plot' :
            self.plotStartDateEdit.setDate(startDate_QDate)
            self.plotEndDateEdit.setDate(endDate_QDate)
        else :
            self.correctionStartDateEdit.setDate(startDate_QDate)
            self.correctionEndDateEdit.setDate(endDate_QDate)

    def drawMainGraph(self, path):
        self.mainGraph.clear()

        table = self.parsedFileTables[path]['table']

        self.mainGraph.plot(table['전력량'][self.parsedFileTables[path]['plotStart']:self.parsedFileTables[path]['plotEnd']], '-')
        if self.parsedFileTables[path]['redPoint']:
            self.mainGraph.plot(table['전력량'][table['이상']=='이상'][self.parsedFileTables[path]['plotStart']:self.parsedFileTables[path]['plotEnd']], 'ro')
        self.mainGraph.margins(x=0)
        self.mainGraph.grid()
        self.mainGraph.set_title(path.split('/')[-1].split('.')[0])
        self.mainGraph.set_xlabel(" ".join(['기간 :', self.parsedFileTables[path]['plotStart'], "~", self.parsedFileTables[path]['plotEnd']]))
        self.mainGraph.set_ylabel("전력량 (kWh)")

        self.mainGraphClass.tight_layout()

        self.mainGraphCanvas.draw()

    def drawElecDistGraph(self, path):
        self.elecDistGraph.clear()

        self.parsedFileTables[path]['table']['전력량'].plot.hist(ax = self.elecDistGraph)
        self.mainGraph.set_ylabel("전력량 (kWh)")
        self.elecDistGraphClass.tight_layout()
        self.elecDistGraphCanvas.draw()

    def drawSeasonalGraphs(self, decomposed):
        for graph in self.seasonalGraphs :
            graph.clear()

        decomposed.observed.plot(ax = self.seasonalGraphs[0])
        self.seasonalGraphs[0].set_ylabel('Observed')
        decomposed.trend.plot(ax = self.seasonalGraphs[1])
        self.seasonalGraphs[1].set_ylabel('Trend')
        decomposed.seasonal.plot(ax = self.seasonalGraphs[2])
        self.seasonalGraphs[2].set_ylabel('Seasonal')
        decomposed.resid.plot(ax = self.seasonalGraphs[3])
        self.seasonalGraphs[3].set_ylabel('Residual')

        self.seasonalGraphClass.tight_layout()
        self.seasonalGraphCanvas.draw()

    def reloadParsedTable(self, path):
        showOutliers = self.parsedFileTables[path]['redPoint']
        self.showOutlierCheckBox.setChecked(showOutliers)
        self.loadParsedTable(path)
        self.dataTable.verticalScrollBar().setValue(self.parsedFileTables[path]['scrollPos'])


    def analyseTable(self, path, resNotShowing=False):
        targetParsedTable = self.parsedFileTables[path]['table']

        zeroPos = zero_runs(targetParsedTable['계차'])
        zeroPos[:, 0] -= 1

        consecZeroPos = np.where(zeroPos[:, 1] - zeroPos[:, 0] >= self.settingVars['sameConsec'])[0]
        # group of indices of items which are longer than sameConsec value

        zScore = norm.ppf(0.5 + 0.5 * self.settingVars['credibility'])

        decomposed = seasonal_decompose(targetParsedTable['전력량'])
        residue_mean = decomposed.resid.mean()
        residue_std = decomposed.resid.std()

        resid = decomposed.resid

        outlierIndices = resid[(resid> residue_mean + zScore*residue_std) | (resid < residue_mean - zScore*residue_std)].index

        targetParsedTable.loc[outlierIndices, '이상'] = '이상'
        targetParsedTable.loc[outlierIndices, '대체'] = 0

        zeroDiffPos = []
        for pos in consecZeroPos :
            zeroDiffPos += range(zeroPos[pos, 0], zeroPos[pos, 1])

        zeroDiffIndices = targetParsedTable.index[zeroDiffPos]

        targetParsedTable.loc[zeroDiffIndices, '이상'] = '이상'
        targetParsedTable.loc[zeroDiffIndices, '대체'] = 0

        allErrorIndices = pd.unique(np.concatenate((outlierIndices.values, zeroDiffIndices.values)))

        self.parsedFileTables[path]['table'] = targetParsedTable
        self.parsedFileTables[path]['decomposed'] = decomposed
        self.parsedFileTables[path]['numOfErrorsInitial'] = allErrorIndices.shape[0]
        self.parsedFileTables[path]['plotStart'] = targetParsedTable.index[0].strftime('%Y-%m-%d')
        self.parsedFileTables[path]['plotEnd'] = targetParsedTable.index[-1].strftime('%Y-%m-%d')

        if not resNotShowing :
            self.loadParsedTable(path)

    def loadParsedTable(self, path):
        table = self.parsedFileTables[path]['table']
        detailInfoText = []
        detailInfoText.append("전체 데이터 개수 : " + str(table.shape[0]))
        detailInfoText.append("최초 검출된 이상치 수 : " + str(self.parsedFileTables[path]['numOfErrorsInitial']))

        self.detailTextEdit.setText("\n".join(detailInfoText))

        self.setDateRange(path, key='plot')
        self.setDateRange(path, key='corr')
        self.setDate(QtCore.QDate().fromString(self.parsedFileTables[path]['plotStart'], 'yyyy-MM-dd'),
                     QtCore.QDate().fromString(self.parsedFileTables[path]['plotEnd'], 'yyyy-MM-dd'), 'plot')

        self.drawElecDistGraph(path)
        self.drawSeasonalGraphs(self.parsedFileTables[path]['decomposed'])
        self.drawMainGraph(path)
        self.showTable(table)

    def showTable(self, tableData):
        self.dataTable.setRowCount(0)
        self.dataTable.setColumnCount(0)
        if type(tableData) != str :
            size = tableData.shape
            self.dataTable.setRowCount(size[0])
            self.dataTable.setColumnCount(size[1])
            self.dataTable.setVerticalHeaderLabels(tableData.index.astype(str))
            self.dataTable.setHorizontalHeaderLabels(tableData.columns.astype(str))

            for rowNum in range(size[0]):
                for colNum in range(size[1]):
                    self.dataTable.setItem(rowNum, colNum,
                                              QtWidgets.QTableWidgetItem(str(tableData.iloc[rowNum, colNum])))

            self.dataTable.resizeRowsToContents()
            self.dataTable.resizeColumnsToContents()

    def recordCurrentPlotRange(self):
        if self.currentPath in self.parsedFileTables:
            self.parsedFileTables[self.currentPath]['plotStart'] = self.plotStartDateEdit.text()
            self.parsedFileTables[self.currentPath]['plotEnd'] = self.plotEndDateEdit.text()

    def applyPlotRange(self):
        if self.currentPath in self.parsedFileTables :
            self.parsedFileTables[self.currentPath]['plotStart'] = self.plotStartDateEdit.text()
            self.parsedFileTables[self.currentPath]['plotEnd'] = self.plotEndDateEdit.text()
            self.parsedFileTables[self.currentPath]['redPoint'] = self.showOutlierCheckBox.isChecked()

            self.drawMainGraph(self.currentPath)

    def clearPlotRange(self):
        if self.currentPath in self.parsedFileTables:
            table = self.parsedFileTables[self.currentPath]['table']
            self.setDate(QtCore.QDate(table.index[0]), QtCore.QDate(table.index[-1]), 'plot')
            self.parsedFileTables[self.currentPath]['redPoint'] = True
            self.showOutlierCheckBox.setChecked(self.parsedFileTables[self.currentPath]['redPoint'])


    def applyCorrectionRange(self):
        if self.currentPath in self.parsedFileTables:
            table = self.parsedFileTables[self.currentPath]['table']
            if self.partialCorrectionEnabled :
                startDate_str = self.correctionStartDateEdit.text()
                endDate_str = self.correctionEndDateEdit.text()
                for rowNum in range(table.index.get_loc(startDate_str).start, table.index.get_loc(endDate_str).stop) :
                    self.recordOutlierStatus(rowNum, 2, setAsWrong=True)
            else :
                for rowNum in [x.row() for x in self.dataTable.selectedIndexes()] :
                    self.recordOutlierStatus(rowNum, 2, setAsWrong=True)

    def clearCorrectionRange(self):
        if self.currentPath in self.parsedFileTables :
            table = self.parsedFileTables[self.currentPath]['table']
            if self.partialCorrectionEnabled :
                startDate_str = self.correctionStartDateEdit.text()
                endDate_str = self.correctionEndDateEdit.text()
                for rowNum in range(table.index.get_loc(startDate_str).start, table.index.get_loc(endDate_str).stop):
                    self.recordOutlierStatus(rowNum, 2, setAsWrong=False)
            else:
                for rowNum in [x.row() for x in self.dataTable.selectedIndexes()]:
                    self.recordOutlierStatus(rowNum, 2, setAsWrong=False)

    def setDetails(self):
        Dialog = SettingDialog(self.settingVars)
        Dialog.exec_()

    def moveGraphTo(self, indexNum):
        if self.currentPath in self.parsedFileTables :
            date = (self.parsedFileTables[self.currentPath]['table'].index[indexNum])
            self.setDate(QtCore.QDate(date), QtCore.QDate(date), 'plot')
            self.applyPlotRange()

    def filterTo(self, colNum):
        if colNum == 2 :
            if not self.rowFiltered :
                rowsToBeHidden = np.where(self.parsedFileTables[self.currentPath]['table']['이상'] == "")[0]
                for i in rowsToBeHidden :
                    self.dataTable.setRowHidden(i, True)
                self.rowFiltered = True
            else :
                for i in range(self.dataTable.rowCount()):
                    self.dataTable.setRowHidden(i, False)
                self.rowFiltered = False

    def toggleCondition(self, rowNum, colNum):
        if colNum == 2 :
            if self.dataTable.item(rowNum, colNum).text() :
                self.recordOutlierStatus(rowNum, colNum, setAsWrong=False)
            else :
                self.recordOutlierStatus(rowNum, colNum, setAsWrong=True)

    def recordOutlierStatus(self, rowNum, colNum, setAsWrong=True):
        if self.currentPath in self.parsedFileTables:
            if setAsWrong:
                self.dataTable.item(rowNum, colNum).setText("이상")
                self.dataTable.item(rowNum, colNum+1).setText('0')

                self.parsedFileTables[self.currentPath]['table'].iloc[rowNum, colNum] = '이상'
                self.parsedFileTables[self.currentPath]['table'].iloc[rowNum, colNum+1] = 0

            else :
                self.dataTable.item(rowNum, colNum).setText("")
                self.dataTable.item(rowNum, colNum + 1).setText(self.dataTable.item(rowNum, 0).text())

                self.parsedFileTables[self.currentPath]['table'].iloc[rowNum, colNum] = ''
                self.parsedFileTables[self.currentPath]['table'].iloc[rowNum, colNum + 1] = \
                self.parsedFileTables[self.currentPath]['table'].iloc[rowNum, 0]


    def enablePartialCorrection(self, stateNum):
        if stateNum == 0 :
            self.partialCorrectionEnabled = False
            self.correctionStartDateEdit.setEnabled(False)
            self.correctionEndDateEdit.setEnabled(False)
        else :
            self.partialCorrectionEnabled = True
            self.correctionStartDateEdit.setEnabled(True)
            self.correctionEndDateEdit.setEnabled(True)

    def setGraphPath(self):
        self.currentGraphSaveFolderPath = QtWidgets.QFileDialog.getExistingDirectory(self, '그래프 저장 폴더 지정')
        self.graphPathLabel.setText(self.currentGraphSaveFolderPath)

    def setDataPath(self):
        self.currentDataSaveFolderPath = QtWidgets.QFileDialog.getExistingDirectory(self, '수정 데이터 저장 폴더 지정')
        self.dataPathLabel.setText(self.currentDataSaveFolderPath)

    def saveGraphFile(self):
        if self.graphPathLabel.text() == "" :
            QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류", "그래프 파일 저장 경로를 먼저 설정해 주세요", QtWidgets.QMessageBox.Ok)
            return

        finishMessage = QtWidgets.QMessageBox(self.centralwidget)
        finishMessage.setWindowTitle("그래프 저장 완료")

        if self.onlyCurrentRadioButton.isChecked() :
            if self.currentPath in self.parsedFileTables :
                bldName = self.currentPath.split('/')[-1].split('.')[0]
                self.mainGraphClass.savefig("".join([self.currentGraphSaveFolderPath, '/', bldName, '.png']))
                finishMessage.setText("그래프가 저장되었습니다")

        else :
            figureNotSaved = []

            startDate_str = self.plotStartDateEdit.text()
            endDate_str = self.plotEndDateEdit.text()

            fig = figure()
            plot = fig.add_subplot(111)

            for path in self.filePathList :
                bldName = path.split('/')[-1].split('.')[0]
                self.statusbar.showMessage(" ".join([bldName, '그래프 저장 중...']))
                if path in self.parsedFileTables :
                    table = self.parsedFileTables[path]['table']
                else:
                    tempTable = self.openFile(path)
                    if type(tempTable) == pd.DataFrame :
                        self.parseInitialTable(path, tempTable, resNotShowing=True)
                        table = self.parsedFileTables[path]['table']
                    else :
                        figureNotSaved.append(path)
                        continue

                if (startDate_str in table.index) and (endDate_str in table.index) :
                    plot.plot(table['전력량'][startDate_str:endDate_str], '-')
                    if self.showOutlierCheckBox.isChecked():
                        plot.plot(table['전력량'][table['이상'] == '이상'][startDate_str:endDate_str], 'ro')
                    plot.margins(x=0)
                    plot.grid()
                    plot.set_title(bldName)
                    plot.set_xlabel(" ".join([str(startDate_str), "~", str(endDate_str)]))
                    plot.set_ylabel("전력량 (kWh)")

                    fig.tight_layout()
                    fig.savefig("".join([self.currentGraphSaveFolderPath, '/', bldName, '.png']))
                    plot.clear()
                else :
                    figureNotSaved.append(bldName)

            close(fig)

            finishMessage.setText("그래프 설정 기간이 유효한 파일의 그래프가 모두 저장되었습니다.\n저장되지 않은 그래프는 하단 상세보기를 참고하세요.")
            finishMessage.setDetailedText("\n".join(figureNotSaved))

        finishMessage.setStandardButtons(QtWidgets.QMessageBox.Ok)
        finishMessage.open()
        self.statusbar.showMessage(self.statusMessage)

    def saveDataFile(self):
        if self.dataPathLabel.text() == "" :
            QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류", "데이터 파일 저장 경로를 먼저 설정해 주세요", QtWidgets.QMessageBox.Ok)
            return

        finishMessage = QtWidgets.QMessageBox(self.centralwidget)
        finishMessage.setWindowTitle("파일 저장 완료")

        if self.changeEncodingCheckBox.isChecked():
            encoding = 'euc-kr'
        else :
            encoding = 'utf-8'

        if self.onlyCurrentRadioButton.isChecked() :
            if self.currentPath in self.parsedFileTables:
                bldName = self.currentPath.split('/')[-1].split('.')[0]
                self.pivotAndSave(self.parsedFileTables[self.currentPath]['table'], "".join([self.currentDataSaveFolderPath, '/', bldName, '.csv']), encoding)
                finishMessage.setText("파일이 저장되었습니다")

        else:
            dataNotSaved = []

            startDate_str = self.plotStartDateEdit.text()
            endDate_str = self.plotEndDateEdit.text()

            for path in self.filePathList:
                bldName = path.split('/')[-1].split('.')[0]
                self.statusbar.showMessage(" ".join([bldName, '파일 저장 중...']))
                if path in self.parsedFileTables:
                    table = self.parsedFileTables[path]['table']
                else :
                    tempTable = self.openFile(path)
                    if type(tempTable) == pd.DataFrame :
                        self.parseInitialTable(path, tempTable, resNotShowing=True)
                        table = self.parsedFileTables[path]['table']
                    else :
                        dataNotSaved.append(path)
                        continue

                if (startDate_str in table.index) and (endDate_str in table.index):
                    self.pivotAndSave(table, "".join([self.currentDataSaveFolderPath, '/', bldName, '.csv']), encoding)
                else:
                    dataNotSaved.append(bldName)

            finishMessage.setText("그래프 설정 기간이 유효한 데이터 파일이 모두 저장되었습니다.\n저장되지 않은 파일은 하단 상세보기를 참고하세요.")
            finishMessage.setDetailedText("\n".join(dataNotSaved))

        finishMessage.setStandardButtons(QtWidgets.QMessageBox.Ok)
        finishMessage.open()
        self.statusbar.showMessage(self.statusMessage)

    def pivotAndSave(self, parsedTable, filePathAndName, encoding='utf-8'):
        targetInputTable = parsedTable.loc[:, '대체':'대체'].copy()
        targetInputTable.index = pd.MultiIndex.from_tuples(targetInputTable.index.to_series().apply(lambda x : (x.date(), x.hour)))

        resTable = targetInputTable.unstack()
        resTable.columns = [str(x) + '시' for x in range(24)]
        resTable.index = resTable.index.strftime("%Y%m%d")
        resTable.index.name = '날짜'

        resTable.to_csv(filePathAndName, encoding=encoding)

    def saveAsShown(self):
        if self.dataTable.rowCount() == 0 :
            QtWidgets.QMessageBox.warning(self.centralwidget, "저장할 데이터 없음", "파일을 연 후 저장하세요", QtWidgets.QMessageBox.Ok)

        else :
            if self.currentPath in self.parsedFileTables :
                fileName, fileFormat = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, "화면에 표시된 대로 저장", filter= '엑셀 파일 (*.xlsx) ;; csv 파일 (*.csv)')
                if fileName:
                    table = self.parsedFileTables[self.currentPath]['table']

                    if fileFormat == "엑셀 파일 (*.xlsx)" :
                        if self.rowFiltered :
                            table[table['이상']=='이상'].to_excel(fileName)
                        else :
                            table.to_excel(fileName)
                    else :
                        if self.changeEncodingCheckBox.isChecked() :
                            encoding= 'euc-kr'
                        else :
                            encoding= 'utf-8'

                        if self.rowFiltered :
                            table[table['이상']=='이상'].to_csv(fileName, encoding=encoding)
                        else :
                            table.to_csv(fileName, encoding=encoding)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    kernel = Kernel()
    kernel.show()

    sys.exit(app.exec_())