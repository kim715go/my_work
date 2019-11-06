# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(1366, 886)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralWidgetLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.centralWidgetSplitter = QtWidgets.QSplitter(self.centralwidget)
        self.centralWidgetSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.leftColumnSplitter = QtWidgets.QSplitter(self.centralWidgetSplitter)
        self.leftColumnSplitter.setOrientation(QtCore.Qt.Vertical)
        self.abstractWidgetForLeftColumnUpper = QtWidgets.QWidget(self.leftColumnSplitter)

        self.leftColumnUpperLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForLeftColumnUpper)
        self.leftColumnUpperLayout.setContentsMargins(0, 0, 0, 0)

        self.leftTopRowLayout = QtWidgets.QHBoxLayout()
        self.openFileButton = QtWidgets.QPushButton(self.abstractWidgetForLeftColumnUpper)
        self.leftTopRowLayout.addWidget(self.openFileButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.leftTopRowLayout.addItem(spacerItem)
        self.setDetailButton = QtWidgets.QPushButton(self.abstractWidgetForLeftColumnUpper)
        self.leftTopRowLayout.addWidget(self.setDetailButton)
        self.leftColumnUpperLayout.addLayout(self.leftTopRowLayout)

        self.buildingForCorrectionLabel = QtWidgets.QLabel(self.abstractWidgetForLeftColumnUpper)
        self.leftColumnUpperLayout.addWidget(self.buildingForCorrectionLabel)
        self.buildingForCorrectionList = QtWidgets.QListWidget(self.abstractWidgetForLeftColumnUpper)
        self.buildingForCorrectionList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.leftColumnUpperLayout.addWidget(self.buildingForCorrectionList)

        self.deleteSelectedRowLayout = QtWidgets.QHBoxLayout()

        self.deleteSelectedButton = QtWidgets.QPushButton(self.abstractWidgetForLeftColumnUpper)
        self.deleteSelectedRowLayout.addWidget(self.deleteSelectedButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.deleteSelectedRowLayout.addItem(spacerItem1)
        self.deleteEntireButton = QtWidgets.QPushButton(self.abstractWidgetForLeftColumnUpper)
        self.deleteSelectedRowLayout.addWidget(self.deleteEntireButton)

        self.leftColumnUpperLayout.addLayout(self.deleteSelectedRowLayout)

        self.leftColumnSplitLine = QtWidgets.QFrame(self.abstractWidgetForLeftColumnUpper)
        self.leftColumnSplitLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.leftColumnSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.leftColumnUpperLayout.addWidget(self.leftColumnSplitLine)

        self.abstractWidgetForLeftColumnLower = QtWidgets.QWidget(self.leftColumnSplitter)
        self.leftColumnLowerLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForLeftColumnLower)
        self.leftColumnLowerLayout.setContentsMargins(0, 0, 0, 0)

        self.elecDistLabel = QtWidgets.QLabel(self.abstractWidgetForLeftColumnLower)
        self.leftColumnLowerLayout.addWidget(self.elecDistLabel)

        self.elecDistGraphClass = plt.Figure()
        self.elecDistGraph = self.elecDistGraphClass.add_subplot(111)
        self.elecDistGraphCanvas = FigureCanvas(self.elecDistGraphClass)
        self.leftColumnLowerLayout.addWidget(self.elecDistGraphCanvas)

        self.seasonalLabel = QtWidgets.QLabel(self.abstractWidgetForLeftColumnLower)
        self.leftColumnLowerLayout.addWidget(self.seasonalLabel)

        self.seasonalGraphClass = plt.Figure()
        self.seasonalGraphs = self.seasonalGraphClass.subplots(4, 1, sharex=True, gridspec_kw={'hspace':0})
        self.seasonalGraphCanvas = FigureCanvas(self.seasonalGraphClass)
        self.leftColumnLowerLayout.addWidget(self.seasonalGraphCanvas)

        self.detailLabel = QtWidgets.QLabel(self.abstractWidgetForLeftColumnLower)
        self.leftColumnLowerLayout.addWidget(self.detailLabel)

        self.detailTextEdit = QtWidgets.QTextEdit(self.abstractWidgetForLeftColumnLower)
        self.leftColumnLowerLayout.addWidget(self.detailTextEdit)

        self.abstractWidgetForRightColumn = QtWidgets.QWidget(self.centralWidgetSplitter)

        self.rightColumnLayout = QtWidgets.QHBoxLayout(self.abstractWidgetForRightColumn)
        self.rightColumnLayout.setContentsMargins(0, 0, 0, 0)

        self.mainSplitLine = QtWidgets.QFrame(self.abstractWidgetForRightColumn)
        self.mainSplitLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.mainSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rightColumnLayout.addWidget(self.mainSplitLine)

        self.rightColumnInsideSplitter = QtWidgets.QSplitter(self.abstractWidgetForRightColumn)
        self.rightColumnInsideSplitter.setOrientation(QtCore.Qt.Vertical)

        self.abstractWidgetForRightColumnUpper = QtWidgets.QWidget(self.rightColumnInsideSplitter)

        self.rightColumnUpperRowLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForRightColumnUpper)
        self.rightColumnUpperRowLayout.setContentsMargins(0, 0, 0, 0)

        self.dataLabelRowLayout = QtWidgets.QHBoxLayout()

        self.dataLabel = QtWidgets.QLabel(self.abstractWidgetForRightColumnUpper)
        self.dataLabelRowLayout.addWidget(self.dataLabel)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dataLabelRowLayout.addItem(spacerItem3)

        self.saveAsShownButton = QtWidgets.QPushButton(self.abstractWidgetForRightColumnUpper)
        self.dataLabelRowLayout.addWidget(self.saveAsShownButton)

        self.rightColumnUpperRowLayout.addLayout(self.dataLabelRowLayout)

        self.dataTable = QtWidgets.QTableWidget(self.abstractWidgetForRightColumnUpper)
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.rightColumnUpperRowLayout.addWidget(self.dataTable)

        self.rightColumnInsideSplitLine = QtWidgets.QFrame(self.abstractWidgetForRightColumnUpper)
        self.rightColumnInsideSplitLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.rightColumnInsideSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rightColumnUpperRowLayout.addWidget(self.rightColumnInsideSplitLine)

        self.rightColumnLowerRowSplitter = QtWidgets.QSplitter(self.rightColumnInsideSplitter)
        self.rightColumnLowerRowSplitter.setOrientation(QtCore.Qt.Horizontal)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.abstractWidgetForOptionSection = QtWidgets.QWidget(self.rightColumnLowerRowSplitter)

        self.optionSectionLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForOptionSection)
        self.optionSectionLayout.setContentsMargins(0, 0, 0, 0)

        self.correctionRangeGroupBox = QtWidgets.QGroupBox(self.abstractWidgetForOptionSection)
        self.correctionRangeGroupBoxLayout = QtWidgets.QGridLayout(self.correctionRangeGroupBox)

        self.correctPartialCheckBox = QtWidgets.QCheckBox(self.correctionRangeGroupBox)
        self.correctPartialCheckBox.setSizePolicy(sizePolicy)
        self.correctionRangeGroupBoxLayout.addWidget(self.correctPartialCheckBox, 0, 0, 1, 2)

        self.correctionRangeLabel = QtWidgets.QLabel(self.correctionRangeGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.correctionRangeLabel.sizePolicy().hasHeightForWidth())
        self.correctionRangeLabel.setSizePolicy(sizePolicy)
        self.correctionRangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.correctionRangeGroupBoxLayout.addWidget(self.correctionRangeLabel, 1, 0, 1, 2)

        self.correctionStartDateEdit = QtWidgets.QDateEdit(self.correctionRangeGroupBox)
        self.correctionStartDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.correctionStartDateEdit.setCalendarPopup(True)
        self.correctionRangeGroupBoxLayout.addWidget(self.correctionStartDateEdit, 2, 0, 1, 1)

        self.correctionEndDateEdit = QtWidgets.QDateEdit(self.correctionRangeGroupBox)
        self.correctionEndDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.correctionEndDateEdit.setCalendarPopup(True)
        self.correctionRangeGroupBoxLayout.addWidget(self.correctionEndDateEdit, 2, 1, 1, 1)

        self.applyCorrectionRangeButton = QtWidgets.QPushButton(self.correctionRangeGroupBox)
        self.correctionRangeGroupBoxLayout.addWidget(self.applyCorrectionRangeButton, 3, 0, 1, 1)

        self.clearCorrectionRangeButton = QtWidgets.QPushButton(self.correctionRangeGroupBox)
        self.correctionRangeGroupBoxLayout.addWidget(self.clearCorrectionRangeButton, 3, 1, 1, 1)

        self.optionSectionLayout.addWidget(self.correctionRangeGroupBox)

        self.plotRangeGroupBox = QtWidgets.QGroupBox(self.abstractWidgetForOptionSection)
        self.plotRangeGroupBoxLayout = QtWidgets.QGridLayout(self.plotRangeGroupBox)

        self.plotRangeLabel = QtWidgets.QLabel(self.plotRangeGroupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.plotRangeLabel.sizePolicy().hasHeightForWidth())
        self.plotRangeLabel.setSizePolicy(sizePolicy)
        self.plotRangeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.plotRangeGroupBoxLayout.addWidget(self.plotRangeLabel, 0, 0, 1, 2)

        self.plotStartDateEdit = QtWidgets.QDateEdit(self.plotRangeGroupBox)
        self.plotStartDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.plotStartDateEdit.setCalendarPopup(True)
        self.plotRangeGroupBoxLayout.addWidget(self.plotStartDateEdit, 1, 0, 1, 1)

        self.plotEndDateEdit = QtWidgets.QDateEdit(self.plotRangeGroupBox)
        self.plotEndDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.plotEndDateEdit.setCalendarPopup(True)
        self.plotRangeGroupBoxLayout.addWidget(self.plotEndDateEdit, 1, 1, 1, 1)

        self.showOutlierCheckBox = QtWidgets.QCheckBox(self.plotRangeGroupBox)
        self.showOutlierCheckBox.setSizePolicy(sizePolicy)
        self.plotRangeGroupBoxLayout.addWidget(self.showOutlierCheckBox, 2, 0, 1, 2)

        self.applyPlotRangeButton = QtWidgets.QPushButton(self.plotRangeGroupBox)
        self.plotRangeGroupBoxLayout.addWidget(self.applyPlotRangeButton, 3, 0, 1, 1)

        self.clearPlotRangeButton = QtWidgets.QPushButton(self.plotRangeGroupBox)
        self.plotRangeGroupBoxLayout.addWidget(self.clearPlotRangeButton, 3, 1, 1, 1)

        self.optionSectionLayout.addWidget(self.plotRangeGroupBox)

        self.savePathGroupbox = QtWidgets.QGroupBox(self.abstractWidgetForOptionSection)

        self.savePathGroupboxLayout = QtWidgets.QGridLayout(self.savePathGroupbox)

        self.graphPathButton = QtWidgets.QPushButton(self.savePathGroupbox)
        self.savePathGroupboxLayout.addWidget(self.graphPathButton, 2, 0, 1, 1)

        self.dataPathButton = QtWidgets.QPushButton(self.savePathGroupbox)
        self.savePathGroupboxLayout.addWidget(self.dataPathButton, 0, 0, 1, 1)

        self.dataPathLabel = QtWidgets.QLineEdit(self.savePathGroupbox)
        self.savePathGroupboxLayout.addWidget(self.dataPathLabel, 0, 1, 1, 1)

        self.graphPathLabel = QtWidgets.QLineEdit(self.savePathGroupbox)
        self.savePathGroupboxLayout.addWidget(self.graphPathLabel, 2, 1, 1, 1)

        self.optionSectionLayout.addWidget(self.savePathGroupbox)

        self.applyRangeOptionGroupbox = QtWidgets.QGroupBox(self.abstractWidgetForOptionSection)
        self.applyRangeOptionGroupboxLayout = QtWidgets.QVBoxLayout(self.applyRangeOptionGroupbox)

        self.onlyCurrentRadioButton = QtWidgets.QRadioButton(self.applyRangeOptionGroupbox)
        self.applyRangeOptionGroupboxLayout.addWidget(self.onlyCurrentRadioButton)

        self.applyEntireRadioButton = QtWidgets.QRadioButton(self.applyRangeOptionGroupbox)
        self.applyRangeOptionGroupboxLayout.addWidget(self.applyEntireRadioButton)

        self.changeEncodingCheckBox = QtWidgets.QCheckBox(self.applyRangeOptionGroupbox)
        self.applyRangeOptionGroupboxLayout.addWidget(self.changeEncodingCheckBox)

        self.optionSectionLayout.addWidget(self.applyRangeOptionGroupbox)

        self.saveButtonRowLayout = QtWidgets.QHBoxLayout()

        self.dataFileSaveButton = QtWidgets.QPushButton(self.abstractWidgetForOptionSection)
        self.saveButtonRowLayout.addWidget(self.dataFileSaveButton)

        self.graphFileSaveButton = QtWidgets.QPushButton(self.abstractWidgetForOptionSection)
        self.saveButtonRowLayout.addWidget(self.graphFileSaveButton)

        self.optionSectionLayout.addLayout(self.saveButtonRowLayout)

        self.abstractWidgetForRightColumnLower = QtWidgets.QWidget(self.rightColumnLowerRowSplitter)

        self.rightColumnLowerLayout = QtWidgets.QHBoxLayout(self.abstractWidgetForRightColumnLower)
        self.rightColumnLowerLayout.setContentsMargins(0, 0, 0, 0)

        self.mainRightLowerRowSplitLine = QtWidgets.QFrame(self.abstractWidgetForRightColumnLower)
        self.mainRightLowerRowSplitLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.mainRightLowerRowSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.rightColumnLowerLayout.addWidget(self.mainRightLowerRowSplitLine)

        self.mainGraphSectionLayout = QtWidgets.QVBoxLayout()

        self.graphLabel = QtWidgets.QLabel(self.abstractWidgetForRightColumnLower)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.graphLabel.setSizePolicy(sizePolicy)
        self.mainGraphSectionLayout.addWidget(self.graphLabel)

        self.mainGraphClass = plt.Figure()
        self.mainGraph = self.mainGraphClass.add_subplot(111)
        self.mainGraphCanvas = FigureCanvas(self.mainGraphClass)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.mainGraphCanvas.setSizePolicy(sizePolicy)
        self.mainGraphSectionLayout.addWidget(self.mainGraphCanvas)

        self.rightColumnLowerLayout.addLayout(self.mainGraphSectionLayout)

        self.rightColumnLayout.addWidget(self.rightColumnInsideSplitter)

        self.centralWidgetLayout.addWidget(self.centralWidgetSplitter)

        self.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar()
        self.setStatusBar(self.statusbar)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("MainWindow")
        self.openFileButton.setText("대상 파일 열기")
        self.setDetailButton.setText("세부 설정")
        self.buildingForCorrectionLabel.setText("대상 파일 목록")
        self.deleteSelectedButton.setText("선택 항목 삭제")
        self.deleteEntireButton.setText("전체 항목 삭제")
        self.elecDistLabel.setText("전략량 분포")
        self.seasonalLabel.setText("seasonal decomposition")
        self.detailLabel.setText("파일 정보")
        self.dataLabel.setText("데이터")
        self.saveAsShownButton.setText("현재 화면에 표시된 대로 표 저장")
        self.graphLabel.setText("그래프")

        self.correctionRangeGroupBox.setTitle("이상치 일괄 설정/해제")
        self.correctPartialCheckBox.setText("아래 구간을 모두 이상치로 설정/해제")
        self.correctionRangeLabel.setText("이상치 설정/해제 범위")
        self.applyCorrectionRangeButton.setText('이상 설정')
        self.clearCorrectionRangeButton.setText('이상 해제')

        self.plotRangeGroupBox.setTitle('그래프 설정')
        self.plotRangeLabel.setText("그래프 구간 설정")
        self.showOutlierCheckBox.setText("이상치를 그래프 상에 표시")
        self.applyPlotRangeButton.setText("적용")
        self.clearPlotRangeButton.setText("초기화")

        self.savePathGroupbox.setTitle("저장 경로 지정")
        self.graphPathButton.setText("그래프 저장 폴더")
        self.dataPathButton.setText("데이터 저장 폴더")
        self.applyRangeOptionGroupbox.setTitle("적용 범위 지정")
        self.onlyCurrentRadioButton.setText("현재 파일만 저장")
        self.applyEntireRadioButton.setText("목록 내 파일 전체 저장")
        self.changeEncodingCheckBox.setText('파일 인코딩을 euc-kr로 저장')
        self.dataFileSaveButton.setText("수정사항 데이터 저장")
        self.graphFileSaveButton.setText("파일로 그래프 저장")

        self.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.openFileButton.clicked.connect(self.openFiles)
        self.setDetailButton.clicked.connect(self.setDetails)
        self.deleteSelectedButton.clicked.connect(self.deleteSelected)
        self.deleteEntireButton.clicked.connect(self.deleteEntire)
        self.saveAsShownButton.clicked.connect(self.saveAsShown)
        self.applyCorrectionRangeButton.clicked.connect(self.applyCorrectionRange)
        self.clearCorrectionRangeButton.clicked.connect(self.clearCorrectionRange)
        self.applyPlotRangeButton.clicked.connect(self.applyPlotRange)
        self.clearPlotRangeButton.clicked.connect(self.clearPlotRange)
        self.graphPathButton.clicked.connect(self.setGraphPath)
        self.dataPathButton.clicked.connect(self.setDataPath)
        self.dataFileSaveButton.clicked.connect(self.saveDataFile)
        self.graphFileSaveButton.clicked.connect(self.saveGraphFile)

    def openFiles(self):
        pass

    def setDetails(self):
        pass

    def deleteSelected(self):
        pass

    def deleteEntire(self):
        pass

    def applyCorrectionRange(self):
        pass

    def clearCorrectionRange(self):
        pass

    def applyPlotRange(self):
        pass

    def clearPlotRange(self):
        pass

    def setDataPath(self):
        pass

    def setGraphPath(self):
        pass

    def saveDataFile(self):
        pass

    def saveGraphFile(self):
        pass

    def saveAsShown(self):
        pass

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

