# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainpage.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.offsetbox import AnchoredText

from datetime import datetime

import matplotlib as mpl
mpl.rc('font', family = 'HCR Dotum')

class ExtendedQLabel(QtWidgets.QLabel):
    doubleClicked = QtCore.pyqtSignal()
    def __init__(self, *args):
        super().__init__(*args)

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        self.doubleClicked.emit()



class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1024, 768)

        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)

        self.setFont(font)
        self.setAutoFillBackground(True)

        self.centralwidget = QtWidgets.QWidget()

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.mainTitleLabel = ExtendedQLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainTitleLabel.sizePolicy().hasHeightForWidth())
        self.mainTitleLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.mainTitleLabel.setFont(font)

        self.verticalLayout.addWidget(self.mainTitleLabel)
        self.topRowLayout = QtWidgets.QHBoxLayout()

        self.deptChoiceLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deptChoiceLabel.sizePolicy().hasHeightForWidth())
        self.deptChoiceLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)
        self.deptChoiceLabel.setFont(font)

        self.topRowLayout.addWidget(self.deptChoiceLabel)
        self.deptChoiceBox = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deptChoiceBox.sizePolicy().hasHeightForWidth())
        self.deptChoiceBox.setSizePolicy(sizePolicy)
        self.deptChoiceBox.setFont(font)

        self.topRowLayout.addWidget(self.deptChoiceBox)
        self.deptChoiceButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deptChoiceButton.sizePolicy().hasHeightForWidth())
        self.deptChoiceButton.setSizePolicy(sizePolicy)
        self.deptChoiceButton.setFont(font)

        self.topRowLayout.addWidget(self.deptChoiceButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.topRowLayout.addItem(spacerItem)
        self.asofLabel = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asofLabel.sizePolicy().hasHeightForWidth())
        self.asofLabel.setSizePolicy(sizePolicy)
        self.asofLabel.setFont(font)

        self.topRowLayout.addWidget(self.asofLabel)
        self.asofDateShow = QtWidgets.QDateEdit(self.centralwidget)
        self.asofDateShow.setReadOnly(True)

        self.topRowLayout.addWidget(self.asofDateShow)
        self.verticalLayout.addLayout(self.topRowLayout)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setFont(font)
        self.tabWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tabWidget.setAutoFillBackground(True)

        self.overviewTab = QtWidgets.QWidget()
        self.overviewTab.setAutoFillBackground(True)

        self.overviewTabLayout = QtWidgets.QGridLayout(self.overviewTab)

        expanding = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.monthlyGraphClass = plt.Figure()
        self.monthlyGraph = self.monthlyGraphClass.add_subplot(111)
        self.monthlyGraphCanvas = FigureCanvas(self.monthlyGraphClass)
        self.monthlyGraphCanvas.setSizePolicy(expanding)
        self.overviewTabLayout.addWidget(self.monthlyGraphCanvas, 1, 0, 1, 1)

        self.overviewGraphClass = plt.Figure()
        self.overviewGraph = self.overviewGraphClass.add_subplot(111)
        self.overviewGraphCanvas = FigureCanvas(self.overviewGraphClass)
        self.overviewGraphCanvas.setSizePolicy(expanding)
        self.overviewTabLayout.addWidget(self.overviewGraphCanvas, 0, 0, 1, 1)


        self.infoCellLayout = QtWidgets.QVBoxLayout()

        self.infoCellUpperLayout = QtWidgets.QGridLayout()

        self.allowedLabel = QtWidgets.QLabel(self.overviewTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.allowedLabel.sizePolicy().hasHeightForWidth())
        self.allowedLabel.setSizePolicy(sizePolicy)
        self.allowedLabel.setFont(font)

        self.infoCellUpperLayout.addWidget(self.allowedLabel, 0, 0, 1, 1)
        self.differenceLabel = QtWidgets.QLabel(self.overviewTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.differenceLabel.sizePolicy().hasHeightForWidth())
        self.differenceLabel.setSizePolicy(sizePolicy)
        self.differenceLabel.setFont(font)

        self.infoCellUpperLayout.addWidget(self.differenceLabel, 2, 0, 1, 1)
        self.differencePanel = QtWidgets.QLCDNumber(self.overviewTab)
        self.differencePanel.setFont(font)
        self.differencePanel.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.differencePanel.setDigitCount(6)

        self.infoCellUpperLayout.addWidget(self.differencePanel, 2, 1, 1, 1)
        self.tonDifference = QtWidgets.QLabel(self.overviewTab)
        self.tonDifference.setFont(font)

        self.infoCellUpperLayout.addWidget(self.tonDifference, 2, 2, 1, 1)
        self.allowedPanel = QtWidgets.QLCDNumber(self.overviewTab)
        self.allowedPanel.setFont(font)
        self.allowedPanel.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.allowedPanel.setDigitCount(6)

        self.infoCellUpperLayout.addWidget(self.allowedPanel, 0, 1, 1, 1)
        self.tonExpected = QtWidgets.QLabel(self.overviewTab)
        self.tonExpected.setFont(font)

        self.infoCellUpperLayout.addWidget(self.tonExpected, 1, 2, 1, 1)
        self.expectedPanel = QtWidgets.QLCDNumber(self.overviewTab)
        self.expectedPanel.setFont(font)
        self.expectedPanel.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.expectedPanel.setDigitCount(6)

        self.infoCellUpperLayout.addWidget(self.expectedPanel, 1, 1, 1, 1)
        self.tonAllowed = QtWidgets.QLabel(self.overviewTab)
        self.tonAllowed.setFont(font)

        self.infoCellUpperLayout.addWidget(self.tonAllowed, 0, 2, 1, 1)
        self.expectedLabel = QtWidgets.QLabel(self.overviewTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.expectedLabel.sizePolicy().hasHeightForWidth())
        self.expectedLabel.setSizePolicy(sizePolicy)
        self.expectedLabel.setFont(font)

        self.infoCellUpperLayout.addWidget(self.expectedLabel, 1, 0, 1, 1)
        self.infoCellUpperLayout.setColumnStretch(1, 2)
        self.infoCellLayout.addLayout(self.infoCellUpperLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        self.infoCellLayout.addItem(spacerItem1)
        self.costLabel = QtWidgets.QLabel(self.overviewTab)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.costLabel.setFont(font)

        self.infoCellLayout.addWidget(self.costLabel)
        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.costPanel = QtWidgets.QLCDNumber(self.overviewTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.costPanel.sizePolicy().hasHeightForWidth())
        self.costPanel.setSizePolicy(sizePolicy)
        self.costPanel.setAutoFillBackground(True)
        self.costPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.costPanel.setSmallDecimalPoint(False)
        self.costPanel.setDigitCount(8)
        self.costPanel.setMode(QtWidgets.QLCDNumber.Dec)
        self.costPanel.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.costPanel.setProperty("value", -21.0)

        self.horizontalLayout.addWidget(self.costPanel)
        self.costUnitLabel = QtWidgets.QLabel(self.overviewTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.costUnitLabel.sizePolicy().hasHeightForWidth())
        self.costUnitLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(12)
        self.costUnitLabel.setFont(font)

        self.horizontalLayout.addWidget(self.costUnitLabel)
        self.infoCellLayout.addLayout(self.horizontalLayout)
        self.overviewTabLayout.addLayout(self.infoCellLayout, 0, 1, 1, 1)

        self.threeYearGraphClass = plt.Figure()
        self.threeYearGraph = self.threeYearGraphClass.add_subplot(111)
        self.threeYearGraphCanvas = FigureCanvas(self.threeYearGraphClass)
        self.threeYearGraphCanvas.setSizePolicy(expanding)
        self.overviewTabLayout.addWidget(self.threeYearGraphCanvas, 1, 1, 1, 1)

        self.overviewTabLayout.setColumnStretch(0, 2)
        self.overviewTabLayout.setColumnStretch(1, 1)
        self.tabWidget.addTab(self.overviewTab, "")

        self.buildingwiseTab = QtWidgets.QWidget()
        self.buildingwiseTab.setAutoFillBackground(True)

        self.buildingwiseTabLayout = QtWidgets.QHBoxLayout(self.buildingwiseTab)

        self.buildingwiseGraphClass = plt.Figure()
        self.buildingwiseGraph = self.buildingwiseGraphClass.add_subplot(111)
        self.buildingwiseGraphCanvas = FigureCanvas(self.buildingwiseGraphClass)
        self.buildingwiseGraphCanvas.setSizePolicy(expanding)
        self.buildingwiseTabLayout.addWidget(self.buildingwiseGraphCanvas)

        self.tabWidget.addTab(self.buildingwiseTab, "")
        self.adminTab = QtWidgets.QWidget()
        self.adminTab.setAutoFillBackground(True)

        self.adminTabLayout = QtWidgets.QGridLayout(self.adminTab)

        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.adminTabLayout.addItem(spacerItem2, 8, 1, 1, 1)
        self.asofChangeLabel = QtWidgets.QLabel(self.adminTab)

        self.adminTabLayout.addWidget(self.asofChangeLabel, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.adminTabLayout.addItem(spacerItem3, 0, 1, 1, 1)
        self.topDownLabel = QtWidgets.QLabel(self.adminTab)

        self.adminTabLayout.addWidget(self.topDownLabel, 2, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.adminTabLayout.addItem(spacerItem4, 1, 0, 1, 1)
        self.bottomUpLabel = QtWidgets.QLabel(self.adminTab)

        self.adminTabLayout.addWidget(self.bottomUpLabel, 1, 1, 1, 1)
        self.asofDateChange = QtWidgets.QDateEdit(self.adminTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.asofDateChange.sizePolicy().hasHeightForWidth())
        self.asofDateChange.setSizePolicy(sizePolicy)

        self.adminTabLayout.addWidget(self.asofDateChange, 5, 1, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.adminTabLayout.addItem(spacerItem5, 3, 1, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.adminTabLayout.addItem(spacerItem6, 1, 5, 1, 1)
        self.applyChangeButton = QtWidgets.QPushButton(self.adminTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.applyChangeButton.sizePolicy().hasHeightForWidth())
        self.applyChangeButton.setSizePolicy(sizePolicy)

        self.adminTabLayout.addWidget(self.applyChangeButton, 4, 4, 1, 1)
        self.cancelChangeButton = QtWidgets.QPushButton(self.adminTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelChangeButton.sizePolicy().hasHeightForWidth())
        self.cancelChangeButton.setSizePolicy(sizePolicy)

        self.adminTabLayout.addWidget(self.cancelChangeButton, 5, 4, 1, 1)
        self.priceChangeLabel = QtWidgets.QLabel(self.adminTab)

        self.adminTabLayout.addWidget(self.priceChangeLabel, 4, 2, 1, 1)
        self.priceInput = QtWidgets.QLineEdit(self.adminTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.priceInput.sizePolicy().hasHeightForWidth())
        self.priceInput.setSizePolicy(sizePolicy)

        self.adminTabLayout.addWidget(self.priceInput, 5, 2, 1, 1)
        self.bottomUpButton = QtWidgets.QPushButton(self.adminTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottomUpButton.sizePolicy().hasHeightForWidth())
        self.bottomUpButton.setSizePolicy(sizePolicy)

        self.adminTabLayout.addWidget(self.bottomUpButton, 1, 2, 1, 1)
        self.topDownButton = QtWidgets.QPushButton(self.adminTab)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topDownButton.sizePolicy().hasHeightForWidth())
        self.topDownButton.setSizePolicy(sizePolicy)
        self.topDownButton.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.adminTabLayout.addWidget(self.topDownButton, 2, 2, 1, 1)

        self.verticalLayout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar()

        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        self.setupVariables()
        self.signalAndSlotConnect()
        self.setupStructure()


    def retranslateUi(self):
        self.setWindowTitle("온실가스 배출량 알리미")
        self.mainTitleLabel.setText("온실가스 배출량 알리미")
        self.deptChoiceLabel.setText("기관 선택")
        self.deptChoiceButton.setText("조회")
        self.asofLabel.setText("기준 일자")
        self.allowedLabel.setText("금년도 배출허용량")
        self.differenceLabel.setText("예상 과부족량")
        self.tonDifference.setText("톤")
        self.tonExpected.setText("톤")
        self.tonAllowed.setText("톤")
        self.expectedLabel.setText("금년도 예상배출량")
        self.costLabel.setText("배출권 구입 예상 비용")
        self.costUnitLabel.setText("만 원")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.overviewTab), "온실가스 배출량 분석")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.buildingwiseTab), "건물별 보기")
        self.asofChangeLabel.setText("기준 일자 변경")
        self.topDownLabel.setText("하향식 데이터 업로드")
        self.bottomUpLabel.setText("상향식 데이터 업로드")
        self.applyChangeButton.setText("적용")
        self.cancelChangeButton.setText("취소")
        self.priceChangeLabel.setText("배출권 가격 변경 (원)")
        self.bottomUpButton.setText("업로드")
        self.topDownButton.setText("업로드")


    def asofDateSet(self, which='show'):
        if which == 'show' : # self.asofDateInfo -> self.asofDateShow
            self.asofDateShow.setDate(QtCore.QDate(self.asofDateInfo.year, self.asofDateInfo.month, self.asofDateInfo.day))
        else : # self.asofDateInfo -> self.asofDateChange
            self.asofDateChange.setDate(QtCore.QDate(self.asofDateInfo.year, self.asofDateInfo.month, self.asofDateInfo.day))

    def setupVariables(self):
        # default settings for variables
        self.asofDateInfo = datetime(2018, 6, 30)
        self.deptInfo = {'deptName':"음악대학", 'allowedAmount':0, 'expectedAmount':0, 'difference':0}
        self.price = 2.2
        self.statusText = "온실가스 배출 데이터 조회"

        self.mainData = pd.read_excel('rawData.xlsx', index_col=0, date_parser=True)/1000
        self.bldInfo = pd.read_excel("bldNames.xlsx", index_col=0)


        self.statusbar.showMessage(self.statusText)
        self.asofDateSet()

        self.allowedPanel.setProperty('value', self.deptInfo['allowedAmount'])
        self.expectedPanel.setProperty('value', self.deptInfo['expectedAmount'])
        self.differencePanel.setProperty('value', self.deptInfo['difference'])
        self.costPanel.setProperty('value', self.deptInfo['difference']*self.price)

        self.monthName = ['1월', '2월', '3월', '4월', '5월', '6월', '7월', '8월', '9월', '10월', '11월', '12월']
        self.asofDateSet('change')

    def signalAndSlotConnect(self):
        # signal and slot connect
        self.deptChoiceButton.clicked.connect(self.deptChoiceFunc)
        self.mainTitleLabel.doubleClicked.connect(self.mainTitleDoubleClickedFunc)
        self.bottomUpButton.clicked.connect(self.bottomUpUploadFunc)
        self.topDownButton.clicked.connect(self.topDownUploadFunc)
        self.applyChangeButton.clicked.connect(self.applyChangeFunc)
        self.cancelChangeButton.clicked.connect(self.cancelChangeFunc)


    def setupStructure(self):
        ######## now start using table data ######

        self.departments = self.bldInfo['기관명'].unique()
        self.deptChoiceBox.addItems(self.departments)

        self.previousYears = self.mainData.loc[:, self.mainData.columns.year < self.asofDateInfo.year]
        self.howManyYears = 3
        self.yearlySumTable = self.previousYears.groupby(self.previousYears.columns.year, axis=1).sum()
        self.monthlySumTable = self.previousYears.groupby(self.previousYears.columns.month, axis=1).sum()

        self.currentYear = self.mainData.loc[:, self.mainData.columns > datetime(self.asofDateInfo.year-1, 12, 1)]
        self.currentYear.iloc[:, 0] = 0
        self.currentCumsum = self.currentYear.cumsum(axis=1)

        self.alreadyEmitted = self.currentCumsum.loc[:, self.currentCumsum.columns <= self.asofDateInfo]
        self.expectedEmitted = self.currentCumsum.loc[:, self.currentCumsum.columns >= self.asofDateInfo]

        self.yearBaseAnalysis = pd.DataFrame(index = self.currentYear.index)
        self.yearBaseAnalysis['0'] = 0
        self.yearBaseAnalysis['기배출량'] = self.currentYear.loc[:, self.currentYear.columns <= self.asofDateInfo].sum(axis=1)
        self.yearBaseAnalysis['예상배출량'] = self.currentYear.loc[:, self.currentYear.columns > self.asofDateInfo].sum(axis=1)

        self.y2018total = self.currentYear.sum(axis=1)
        self.y2018allowed = self.yearlySumTable.mean(axis=1)*0.9

        self.monthlyAllowed = self.monthlySumTable / self.howManyYears * 0.9

        self.setDeptFilter()

        self.makeOverview()
        self.makeBldwiseView()

    def setDeptFilter(self):
        self.deptFilter = self.bldInfo['기관명'] == self.deptInfo['deptName']

    def makeOverview(self):
        yearBaseAnalysisFiltered = self.yearBaseAnalysis.cumsum(axis=1).loc[self.deptFilter, :].sum()

        y2018allowedFiltered = self.y2018allowed[self.deptFilter].sum()
        y2018totalFiltered = self.y2018total[self.deptFilter].sum()


        self.deptInfo['allowedAmount'] = int(round(y2018allowedFiltered))
        self.deptInfo['expectedAmount'] = int(round(y2018totalFiltered))
        self.deptInfo['difference'] = self.deptInfo['expectedAmount'] - self.deptInfo['allowedAmount']

        self.allowedPanel.setProperty('value', self.deptInfo['allowedAmount'])
        self.expectedPanel.setProperty('value', self.deptInfo['expectedAmount'])
        self.differencePanel.setProperty('value', self.deptInfo['difference'])
        self.costPanel.setProperty('value', self.deptInfo['difference']*self.price)

        self.overviewGraph.plot(yearBaseAnalysisFiltered[:'기배출량'], [0.15, 0.15],  '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='c')
        self.overviewGraph.plot(yearBaseAnalysisFiltered['기배출량':], [0.15, 0.15], '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='orange')


        for i in range(1, len(yearBaseAnalysisFiltered)):
            self.overviewGraph.text((yearBaseAnalysisFiltered[i] + yearBaseAnalysisFiltered[i-1])/2, 0.15, yearBaseAnalysisFiltered.index[i], va='center', ha = 'center')

        self.overviewGraph.plot([0, y2018allowedFiltered], [0, 0], '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='pink')
        self.overviewGraph.text(y2018allowedFiltered/2, 0, '금년도 배출허용량', va='center', ha = 'center')


        alreadyEmittedFiltered = self.alreadyEmitted.loc[self.deptFilter].sum()
        expectedEmittedFiltered = self.expectedEmitted.loc[self.deptFilter].sum()
        currentCumsumFiltered = self.currentCumsum.loc[self.deptFilter].sum()

        self.overviewGraph.plot(alreadyEmittedFiltered, [-0.15]*len(alreadyEmittedFiltered), '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='c')
        self.overviewGraph.plot(expectedEmittedFiltered, [-0.15]*len(expectedEmittedFiltered), '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='orange')

        for i in range(1, len(currentCumsumFiltered)):
            self.overviewGraph.text((currentCumsumFiltered[i] + currentCumsumFiltered[i-1])/2, -0.15, self.monthName[i-1], va='center', ha = 'center')

        if y2018totalFiltered > y2018allowedFiltered:
            self.overviewGraph.plot([y2018allowedFiltered, y2018totalFiltered], [0, 0], '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='red')
            self.overviewGraph.text((y2018allowedFiltered+y2018totalFiltered)/2, 0, '초과량', va='center', ha='center')
        else :
            self.overviewGraph.plot([y2018allowedFiltered, y2018totalFiltered], [0.15, 0.15], '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='green')
            self.overviewGraph.text((y2018allowedFiltered+y2018totalFiltered)/2, 0.15, '잉여량', va='center', ha='center')
            self.overviewGraph.plot([y2018allowedFiltered, y2018totalFiltered], [-0.15, -0.15], '|-', linewidth=40, ms=45, mew=2, mec='w', mfc='w', solid_capstyle='butt', color='green')
            self.overviewGraph.text((y2018allowedFiltered+y2018totalFiltered)/2, -0.15, '잉여량', va='center', ha='center')



        monthlyDict = {}

        monthlyAllowedFiltered = pd.Series(self.monthlyAllowed.loc[self.deptFilter].sum())
        monthlyExpectedFiltered = pd.Series(self.currentYear.loc[self.deptFilter].iloc[:,1:].sum())

        monthlyAllowedFiltered.index=self.monthName
        monthlyExpectedFiltered.index = self.monthName

        monthlyDifferenceFiltered = monthlyExpectedFiltered - monthlyAllowedFiltered

        for i in range(len(alreadyEmittedFiltered)-1):
            if monthlyDifferenceFiltered[i] > 0 :
                monthlyDict[self.monthName[i]] = [monthlyAllowedFiltered[i], 0, monthlyDifferenceFiltered[i], 0]
            else :
                monthlyDict[self.monthName[i]] = [monthlyExpectedFiltered[i], 0, 0, -monthlyDifferenceFiltered[i]]

        for j in range(len(alreadyEmittedFiltered)-1, 12) :
            if monthlyDifferenceFiltered[j] > 0:
                monthlyDict[self.monthName[j]] = [0, monthlyAllowedFiltered[j], monthlyDifferenceFiltered[j], 0]
            else:
                monthlyDict[self.monthName[j]] = [0, monthlyExpectedFiltered[j], 0, -monthlyDifferenceFiltered[j]]

        monthlyTable=pd.DataFrame(monthlyDict, index=['기배출량', '예상배출량', '초과량', '잉여량']).transpose()
        monthlyTable = monthlyTable.loc[self.monthName]


        self.overviewGraph.set_ylim(-0.25, 0.25)
        self.overviewGraph.set_yticks([0.15, 0, -0.15])
        self.overviewGraph.set_yticklabels(['배출예상', '허용량', '월별비교'])
        self.overviewGraph.set_title("기관별 온실가스 배출 현황 및 예상")
        # self.overviewGraph.set_xlabel("(단위 : tCO2)")
        # self.overviewGraphClass.tight_layout()
        self.yearlySumTable.loc[self.deptFilter].sum().plot.bar(ax = self.threeYearGraph, rot=0, color='c')
        self.threeYearGraphClass.tight_layout(rect=[0,0,1,0.95])
        self.threeYearGraph.set_title("최근 3개년간 배출량")

        monthlyTable.plot.bar(ax = self.monthlyGraph, rot=0, stacked=True, color=['c', 'orange', 'red', 'green'])
        #
        self.threeYearGraphCanvas.draw()
        self.overviewGraphCanvas.draw()
        self.monthlyGraphCanvas.draw()

    def makeBldwiseView(self):
        yearBaseAnalysisFiltered = self.yearBaseAnalysis.cumsum(axis=1).loc[self.deptFilter, :]

        y2018allowedFiltered = self.y2018allowed[self.deptFilter]
        y2018totalFiltered = self.y2018total[self.deptFilter]

        alreadyEmittedFiltered = self.alreadyEmitted.loc[self.deptFilter].iloc[:,-1]

        bldDict ={}

        for bldName in yearBaseAnalysisFiltered.index :
            res = [0,0,0,0]
            res[0] = alreadyEmittedFiltered[bldName]
            if y2018totalFiltered.loc[bldName] > y2018allowedFiltered.loc[bldName] :
                res[2] = y2018totalFiltered.loc[bldName] - y2018allowedFiltered.loc[bldName]

            else :
                res[3] = y2018allowedFiltered.loc[bldName] - y2018totalFiltered.loc[bldName]
            res[1] = y2018totalFiltered.loc[bldName] - res[0] - res[2]
            bldDict[bldName] = res

        bldwiseTable = pd.DataFrame(bldDict, index=['기배출량', '예상배출량', '초과량', '잉여량']).transpose()

        bldFiltered = self.bldInfo[self.deptFilter]

        bldwiseTable.index = ([x + "동\n" for x in bldFiltered.index] + bldFiltered['건물명']).tolist()

        bldwiseTable.plot.barh(ax = self.buildingwiseGraph, rot=0, stacked = True, color=['c', 'orange', 'red', 'green'])
        self.buildingwiseGraph.set_title("건물별 온실가스 배출 현황 및 예상")
        self.buildingwiseGraphClass.tight_layout()
        self.buildingwiseGraphCanvas.draw()


    def deptChoiceFunc(self):
        self.deptInfo['deptName'] = self.deptChoiceBox.currentText()
        self.setDeptFilter()

        self.overviewGraph.clear()
        self.threeYearGraph.clear()
        self.monthlyGraph.clear()
        self.buildingwiseGraph.clear()

        self.makeOverview()
        self.makeBldwiseView()

    def mainTitleDoubleClickedFunc(self):
        self.tabWidget.addTab(self.adminTab, "")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.adminTab), "관리")
        self.statusbar.showMessage("온실가스 배출 데이터 조회 - 관리자")

    def bottomUpUploadFunc(self):
        pass

    def topDownUploadFunc(self):
        pass

    def applyChangeFunc(self):
        self.price = float(self.priceInput.text())
        self.asofDateInfo = datetime(self.asofDateChange.date().year(), self.asofDateChange.date().month(), self.asofDateChange.date().day())
        self.asofDateSet()

    def cancelChangeFunc(self):
        self.asofDateSet('change')
        self.priceInput.clear()



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())
