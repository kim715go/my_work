# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from datetime import datetime

import matplotlib as mpl
mpl.rc('font', family = 'HCR Dotum')


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        font = QtGui.QFont()
        font.setFamily("Malgun Gothic")
        font.setPointSize(10)

        today = datetime.today()

        self.resize(1080, 728)
        self.setFont(font)

        self.centralwidget = QtWidgets.QWidget()

        self.wholeLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.mainSplitter = QtWidgets.QSplitter(self.centralwidget)
        self.mainSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.mainLeftColumnSpliter = QtWidgets.QSplitter(self.mainSplitter)
        self.mainLeftColumnSpliter.setOrientation(QtCore.Qt.Vertical)

        #the first part of leftside - unit for splitting
        self.abstractWidgetForBuildingChoice = QtWidgets.QWidget(self.mainLeftColumnSpliter)
        self.buildingChoiceSectionLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForBuildingChoice)
        self.buildingChoiceSectionLayout.setContentsMargins(0, 0, 0, 0)
        
        self.buildingChoiceGrid = QtWidgets.QGridLayout()

        # self.dataConnectionLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        # self.dataConnectionLabel.setFont(font)
        # self.buildingChoiceGrid.addWidget(self.dataConnectionLabel, 0, 0, 1, 1)
        #
        # self.dataConnectionButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        # self.dataConnectionButton.setFont(font)
        # self.buildingChoiceGrid.addWidget(self.dataConnectionButton, 0, 1, 1, 1)

        self.chooseCampusLabel = QtWidgets.QLabel(self.abstractWidgetForBuildingChoice)
        self.chooseCampusLabel.setFont(font)
        self.buildingChoiceGrid.addWidget(self.chooseCampusLabel, 1, 0, 1, 1)

        self.chooseCategoryLabel = QtWidgets.QLabel(self.abstractWidgetForBuildingChoice)
        self.buildingChoiceGrid.addWidget(self.chooseCategoryLabel, 2, 0, 1, 1)
        self.chooseCategoryLabel.setFont(font)

        self.chooseCategoryComboBox = QtWidgets.QComboBox(self.abstractWidgetForBuildingChoice)
        self.buildingChoiceGrid.addWidget(self.chooseCategoryComboBox, 2, 1, 1, 1)
        self.chooseCategoryComboBox.setFont(font)

        self.chooseCampusComboBox = QtWidgets.QComboBox(self.abstractWidgetForBuildingChoice)
        self.buildingChoiceGrid.addWidget(self.chooseCampusComboBox, 1, 1, 1, 1)
        self.chooseCampusComboBox.setFont(font)

        self.chooseDetailComboBox = QtWidgets.QComboBox(self.abstractWidgetForBuildingChoice)
        self.buildingChoiceGrid.addWidget(self.chooseDetailComboBox, 3, 1, 1, 1)
        self.chooseDetailComboBox.setFont(font)

        self.buildingChoiceSectionLayout.addLayout(self.buildingChoiceGrid)

        self.showBuildingList = QtWidgets.QListWidget(self.abstractWidgetForBuildingChoice)
        self.buildingChoiceSectionLayout.addWidget(self.showBuildingList)
        self.showBuildingList.setFont(font)
        self.showBuildingList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.addBuildingButtonRow = QtWidgets.QHBoxLayout()
        
        self.addSelectedButton = QtWidgets.QPushButton(self.abstractWidgetForBuildingChoice)
        self.addSelectedButton.setFont(font)
        self.addBuildingButtonRow.addWidget(self.addSelectedButton)

        self.addEntireButton = QtWidgets.QPushButton(self.abstractWidgetForBuildingChoice)
        self.addEntireButton.setFont(font)
        self.addBuildingButtonRow.addWidget(self.addEntireButton)

        self.buildingChoiceSectionLayout.addLayout(self.addBuildingButtonRow)

        self.mainLeftColumnFirstSplitLine = QtWidgets.QFrame(self.abstractWidgetForBuildingChoice)
        self.mainLeftColumnFirstSplitLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.mainLeftColumnFirstSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.buildingChoiceSectionLayout.addWidget(self.mainLeftColumnFirstSplitLine)

        self.abstractWidgetForCorrectionBuildings = QtWidgets.QWidget(self.mainLeftColumnSpliter)
        self.correctionBuildingLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForCorrectionBuildings)
        self.correctionBuildingLayout.setContentsMargins(0, 0, 0, 0)

        self.buildingForCorrectionLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionBuildings)
        self.buildingForCorrectionLabel.setFont(font)
        self.correctionBuildingLayout.addWidget(self.buildingForCorrectionLabel)

        self.buildingForCorrectionList = QtWidgets.QListWidget(self.abstractWidgetForCorrectionBuildings)
        self.buildingForCorrectionList.setFont(font)
        self.buildingForCorrectionList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.correctionBuildingLayout.addWidget(self.buildingForCorrectionList)

        self.buildingForCorrectionButtonRow = QtWidgets.QHBoxLayout()

        self.deleteSelectedButton = QtWidgets.QPushButton(self.abstractWidgetForCorrectionBuildings)
        self.deleteSelectedButton.setFont(font)
        self.buildingForCorrectionButtonRow.addWidget(self.deleteSelectedButton)

        self.deleteEntireButton = QtWidgets.QPushButton(self.abstractWidgetForCorrectionBuildings)
        self.deleteEntireButton.setFont(font)
        self.buildingForCorrectionButtonRow.addWidget(self.deleteEntireButton)

        self.correctionBuildingLayout.addLayout(self.buildingForCorrectionButtonRow)
        
        self.mainLeftColumnSecondSplitLine = QtWidgets.QFrame(self.abstractWidgetForCorrectionBuildings)
        self.mainLeftColumnSecondSplitLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.mainLeftColumnSecondSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.correctionBuildingLayout.addWidget(self.mainLeftColumnSecondSplitLine)

        self.abstractWidgetForCorrectionOptions = QtWidgets.QWidget(self.mainLeftColumnSpliter)
        self.optionGrid = QtWidgets.QGridLayout(self.abstractWidgetForCorrectionOptions)
        self.optionGrid.setContentsMargins(0, 0, 0, 0)

        self.replacementOptionLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionOptions)
        self.replacementOptionLabel.setFont(font)
        self.optionGrid.addWidget(self.replacementOptionLabel, 5, 0, 1, 1)

        self.quartileCalcGroupBox = QtWidgets.QGroupBox(self.abstractWidgetForCorrectionOptions)
        self.quartileCalcGroupBox.setFont(font)
        self.quartileGroupBoxLayout = QtWidgets.QVBoxLayout(self.quartileCalcGroupBox)

        self.noInterpolationRadioButton = QtWidgets.QRadioButton(self.quartileCalcGroupBox)
        self.noInterpolationRadioButton.setFont(font)
        self.noInterpolationRadioButton.setChecked(True)
        self.quartileGroupBoxLayout.addWidget(self.noInterpolationRadioButton)

        self.yesInterpolationRadioButton = QtWidgets.QRadioButton(self.quartileCalcGroupBox)
        self.yesInterpolationRadioButton.setFont(font)
        self.quartileGroupBoxLayout.addWidget(self.yesInterpolationRadioButton)

        self.optionGrid.addWidget(self.quartileCalcGroupBox, 4, 0, 1, 1)

        self.normalDistGroupBox = QtWidgets.QGroupBox(self.abstractWidgetForCorrectionOptions)
        self.normalDistGroupBox.setFont(font)
        self.normalDistGroupBoxLayout = QtWidgets.QVBoxLayout(self.normalDistGroupBox)

        self.reliabilitySpinBox = QtWidgets.QDoubleSpinBox(self.normalDistGroupBox)
        self.reliabilitySpinBox.setSuffix("%")
        self.reliabilitySpinBox.setDecimals(1)
        self.reliabilitySpinBox.setMinimum(0.1)
        self.reliabilitySpinBox.setMaximum(99.9)
        self.reliabilitySpinBox.setValue(95.0)
        self.reliabilitySpinBox.setFont(font)
        
        self.normalDistGroupBoxLayout.addWidget(self.reliabilitySpinBox)

        self.optionGrid.addWidget(self.normalDistGroupBox, 4, 1, 1, 1)

        self.endDateLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionOptions)
        self.endDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.endDateLabel.setFont(font)
        self.optionGrid.addWidget(self.endDateLabel, 0, 1, 1, 1)

        self.abnormalOptionLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionOptions)
        self.abnormalOptionLabel.setFont(font)
        self.optionGrid.addWidget(self.abnormalOptionLabel, 2, 0, 1, 1)

        self.abnormal_IQR_checkbox = QtWidgets.QCheckBox(self.abstractWidgetForCorrectionOptions)
        self.abnormal_IQR_checkbox.setChecked(True)
        self.abnormal_IQR_checkbox.setFont(font)
        self.optionGrid.addWidget(self.abnormal_IQR_checkbox, 3, 0, 1, 1)

        self.abnormal_ND_checkbox = QtWidgets.QCheckBox(self.abstractWidgetForCorrectionOptions)
        self.abnormal_ND_checkbox.setFont(font)
        self.optionGrid.addWidget(self.abnormal_ND_checkbox, 3, 1, 1, 1)

        self.startDateLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionOptions)
        self.startDateLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.startDateLabel.setFont(font)
        self.optionGrid.addWidget(self.startDateLabel, 0, 0, 1, 1)

        self.startDateEdit = QtWidgets.QDateEdit(self.abstractWidgetForCorrectionOptions)
        self.startDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.startDateEdit.setFont(font)
        self.startDateEdit.setCalendarPopup(True)
        self.startDateEdit.setMaximumDate(QtCore.QDate(today))
        self.startDateEdit.setDate(QtCore.QDate(today.year, today.month, 1))
        self.optionGrid.addWidget(self.startDateEdit, 1, 0, 1, 1)
        
        self.endDateEdit = QtWidgets.QDateEdit(self.abstractWidgetForCorrectionOptions)
        self.endDateEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.endDateEdit.setFont(font)
        self.endDateEdit.setDate(QtCore.QDate(today))
        self.endDateEdit.setCalendarPopup(True)
        self.optionGrid.addWidget(self.endDateEdit, 1, 1, 1, 1)
        
        self.replacementOptionComboBox = QtWidgets.QComboBox(self.abstractWidgetForCorrectionOptions)
        self.replacementOptionComboBox.setFont(font)
        self.optionGrid.addWidget(self.replacementOptionComboBox, 5, 1, 1, 1)

        self.normalRangeLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionOptions)
        self.normalRangeLabel.setFont(font)
        self.optionGrid.addWidget(self.normalRangeLabel, 6, 0, 1, 1)

        self.rangeSpinBoxLayout = QtWidgets.QHBoxLayout()

        self.startRangeSpinBox = QtWidgets.QSpinBox(self.abstractWidgetForCorrectionOptions)
        self.startRangeSpinBox.setFont(font)
        self.startRangeSpinBox.setMinimum(-1000)
        self.startRangeSpinBox.setMaximum(10000)
        self.rangeSpinBoxLayout.addWidget(self.startRangeSpinBox)

        self.rangeMiddleLabel = QtWidgets.QLabel(self.abstractWidgetForCorrectionOptions)
        self.rangeMiddleLabel.setFont(font)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.rangeMiddleLabel.setSizePolicy(sizePolicy)
        self.rangeSpinBoxLayout.addWidget(self.rangeMiddleLabel)

        self.endRangeSpinBox = QtWidgets.QSpinBox(self.abstractWidgetForCorrectionOptions)
        self.endRangeSpinBox.setFont(font)
        self.endRangeSpinBox.setMinimum(-1000)
        self.endRangeSpinBox.setMaximum(10000)
        self.rangeSpinBoxLayout.addWidget(self.endRangeSpinBox)

        self.optionGrid.addLayout(self.rangeSpinBoxLayout, 6, 1, 1, 1)

        self.dynamicalErrorCheckbox = QtWidgets.QCheckBox(self.abstractWidgetForCorrectionOptions)
        self.dynamicalErrorCheckbox.setFont(font)
        self.optionGrid.addWidget(self.dynamicalErrorCheckbox, 7, 1, 1, 1)

        self.startPauseCorrectionButton = QtWidgets.QPushButton(self.abstractWidgetForCorrectionOptions)
        self.startPauseCorrectionButton.setFont(font)
        self.optionGrid.addWidget(self.startPauseCorrectionButton, 8, 1, 1, 1)

        self.clearAbortButton = QtWidgets.QPushButton(self.abstractWidgetForCorrectionOptions)
        self.clearAbortButton.setFont(font)
        self.optionGrid.addWidget(self.clearAbortButton, 8, 0, 1, 1)
        
        self.abstractWidgetForMainRightColumn = QtWidgets.QWidget(self.mainSplitter)
        self.mainRightColumnLayout = QtWidgets.QHBoxLayout(self.abstractWidgetForMainRightColumn)
        self.mainRightColumnLayout.setContentsMargins(0, 0, 0, 0)
        
        self.mainSplitLine = QtWidgets.QFrame(self.abstractWidgetForMainRightColumn)
        self.mainSplitLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.mainSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.mainRightColumnLayout.addWidget(self.mainSplitLine)
        
        self.mainRightColumnSplitter = QtWidgets.QSplitter(self.abstractWidgetForMainRightColumn)
        self.mainRightColumnSplitter.setOrientation(QtCore.Qt.Vertical)
        self.abstractWidgetForDataShowSection = QtWidgets.QWidget(self.mainRightColumnSplitter)
        
        self.dataShowSectionLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForDataShowSection)
        self.dataShowSectionLayout.setContentsMargins(0, 0, 0, 0)
        
        self.dataShowSectionHeadLayout = QtWidgets.QHBoxLayout()
        
        self.dataLabel = QtWidgets.QLabel(self.abstractWidgetForDataShowSection)
        self.dataLabel.setFont(font)
        self.dataShowSectionHeadLayout.addWidget(self.dataLabel)
        
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.dataShowSectionHeadLayout.addItem(spacerItem)
        
        self.showGraphCheckBox = QtWidgets.QCheckBox(self.abstractWidgetForDataShowSection)
        self.showGraphCheckBox.setFont(font)
        self.dataShowSectionHeadLayout.addWidget(self.showGraphCheckBox)

        self.dataConnectionButton = QtWidgets.QPushButton(self.abstractWidgetForDataShowSection)
        self.dataConnectionButton.setFont(font)
        self.dataShowSectionHeadLayout.addWidget(self.dataConnectionButton)

        self.dataShowSectionLayout.addLayout(self.dataShowSectionHeadLayout)

        self.dataTable = QtWidgets.QTableWidget(self.abstractWidgetForDataShowSection)
        self.dataTable.setFont(font)
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)
        self.dataShowSectionLayout.addWidget(self.dataTable)

        self.mainRightColumnSplitLine = QtWidgets.QFrame(self.abstractWidgetForDataShowSection)
        self.mainRightColumnSplitLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.mainRightColumnSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.dataShowSectionLayout.addWidget(self.mainRightColumnSplitLine)

        self.mainRightLowerRowSplitter = QtWidgets.QSplitter(self.mainRightColumnSplitter)
        self.mainRightLowerRowSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.abstractWidgetForGraphSection = QtWidgets.QWidget(self.mainRightLowerRowSplitter)

        self.graphSectionLayout = QtWidgets.QHBoxLayout(self.abstractWidgetForGraphSection)
        self.graphSectionLayout.setContentsMargins(0, 0, 0, 0)

        self.graphContainer = QtWidgets.QVBoxLayout()

        self.graphLabel = QtWidgets.QLabel(self.abstractWidgetForGraphSection)
        self.graphLabel.setFont(font)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.graphLabel.setSizePolicy(sizePolicy)
        self.graphContainer.addWidget(self.graphLabel)

        self.graphClass = plt.Figure()
        self.graph = self.graphClass.add_subplot(111)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.graphCanvas = FigureCanvas(self.graphClass)
        self.graphCanvas.setSizePolicy(sizePolicy)
        self.graphContainer.addWidget(self.graphCanvas)

        self.graphSectionLayout.addLayout(self.graphContainer)
        
        self.mainRightLowerRowSplitLine = QtWidgets.QFrame(self.abstractWidgetForGraphSection)
        self.mainRightLowerRowSplitLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.mainRightLowerRowSplitLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.graphSectionLayout.addWidget(self.mainRightLowerRowSplitLine)

        self.graphAndSaveOptionSplitter = QtWidgets.QSplitter(self.mainRightLowerRowSplitter)
        self.graphAndSaveOptionSplitter.setOrientation(QtCore.Qt.Vertical)

        self.abstractWidgetForGraphOptionSection = QtWidgets.QWidget(self.graphAndSaveOptionSplitter)
        self.graphOptionLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForGraphOptionSection)

        self.graphOptionBox = QtWidgets.QGroupBox(self.abstractWidgetForGraphOptionSection)
        self.graphOptionBoxLayout = QtWidgets.QVBoxLayout(self.graphOptionBox)

        self.scaleOptionLabel = QtWidgets.QLabel(self.graphOptionBox)
        self.scaleOptionLabel.setFont(font)
        self.graphOptionBoxLayout.addWidget(self.scaleOptionLabel)

        self.zoomSlider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self.graphOptionBox)
        self.zoomSlider.setMaximum(5)
        self.zoomSlider.setMinimum(1)
        self.zoomSlider.setValue(3)
        self.zoomSlider.setFont(font)
        self.zoomSlider.setTickInterval(1)
        self.zoomSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)

        self.graphOptionBoxLayout.addWidget(self.zoomSlider)

        self.graphOptionLayout.addWidget(self.graphOptionBox)

        self.abstractWidgetForSaveOptionSection = QtWidgets.QWidget(self.graphAndSaveOptionSplitter)
        self.saveOptionLayout = QtWidgets.QVBoxLayout(self.abstractWidgetForSaveOptionSection)

        self.saveOptionGroupBox = QtWidgets.QGroupBox(self.abstractWidgetForSaveOptionSection)
        self.saveOptionGroupBoxLayout = QtWidgets.QGridLayout(self.saveOptionGroupBox)

        self.dataFileSaveButton = QtWidgets.QPushButton(self.saveOptionGroupBox)
        self.dataFileSaveButton.setFont(font)
        self.saveOptionGroupBoxLayout.addWidget(self.dataFileSaveButton, 1, 0, 1, 1)
        
        self.dataUploadButton = QtWidgets.QPushButton(self.saveOptionGroupBox)
        self.dataUploadButton.setFont(font)
        self.saveOptionGroupBoxLayout.addWidget(self.dataUploadButton, 1, 1, 1, 1)

        self.graphFileSaveButton = QtWidgets.QPushButton(self.saveOptionGroupBox)
        self.graphFileSaveButton.setFont(font)
        self.saveOptionGroupBoxLayout.addWidget(self.graphFileSaveButton, 3, 0, 1, 1)

        self.saveOptionLayout.addWidget(self.saveOptionGroupBox)

        self.mainRightColumnLayout.addWidget(self.mainRightColumnSplitter)
        self.wholeLayout.addWidget(self.mainSplitter)
        self.setCentralWidget(self.centralwidget)
        
        self.statusbar = QtWidgets.QStatusBar(self)
        self.setStatusBar(self.statusbar)
        font.setPointSize(9)
        self.statusbar.setFont(font)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Correction Program v 1.0.0 (2019/4/12)")
        # self.dataConnectionLabel.setText("데이터 연결됨")
        # self.dataConnectionButton.setText("데이터 연결 관리")
        self.chooseCampusLabel.setText("캠퍼스 선택")
        self.chooseCategoryLabel.setText("분류 선택")
        self.addSelectedButton.setText("선택 항목 추가")
        self.addEntireButton.setText("전체 항목 추가")
        self.buildingForCorrectionLabel.setText("보정 대상 건물")
        self.deleteSelectedButton.setText("선택 항목 삭제")
        self.deleteEntireButton.setText("전체 항목 삭제")
        self.replacementOptionLabel.setText("보정치 산정 옵션")
        self.quartileCalcGroupBox.setTitle("사분위수 계산 방법")
        self.noInterpolationRadioButton.setText("보간 안 함")
        self.yesInterpolationRadioButton.setText("보간 함")
        self.normalDistGroupBox.setTitle("신뢰수준")
        self.startPauseCorrectionButton.setText("보정 시작")
        self.endDateLabel.setText("종료 일자")
        self.abnormalOptionLabel.setText("이상치 판단 방법")
        self.abnormal_IQR_checkbox.setText("IQR 방식")
        self.abnormal_ND_checkbox.setText("정규분포 방식")
        self.startDateLabel.setText("시작 일자")
        self.clearAbortButton.setText("초기화")
        self.dataLabel.setText("데이터")
        self.showGraphCheckBox.setText("그래프 보기")
        self.dataConnectionButton.setText("데이터 연결 관리")
        self.graphLabel.setText("그래프")
        self.graphOptionBox.setTitle("그래프 설정")
        self.scaleOptionLabel.setText("그래프 확대/축소")
        self.saveOptionGroupBox.setTitle("저장 옵션")
        self.dataFileSaveButton.setText("파일로 데이터 저장")
        self.dataUploadButton.setText("보정치 서버에 업로드")
        self.graphFileSaveButton.setText("파일로 그래프 저장")

        self.replacementOptionComboBox.addItem("평균")
        self.replacementOptionComboBox.addItem("중앙값")

        self.startRangeSpinBox.setValue(0)
        self.endRangeSpinBox.setValue(3000)
        
        self.normalRangeLabel.setText("정상 범위")
        self.rangeMiddleLabel.setText(" ~ ")
        self.dynamicalErrorCheckbox.setText('동적으로 오류 탐색')

        self.dataConnectionButton.clicked.connect(self.dataConnectCheck)
        self.addSelectedButton.clicked.connect(self.addSelected)
        self.addEntireButton.clicked.connect(self.addEntire)

        self.deleteSelectedButton.clicked.connect(self.deleteSelected)
        self.deleteEntireButton.clicked.connect(self.deleteEntire)

        self.clearAbortButton.clicked.connect(self.clearAbortToggle)
        self.startPauseCorrectionButton.clicked.connect(self.startPauseToggle)


    def dataConnectCheck(self):
        pass

    def addSelected(self):
        pass

    def addEntire(self):
        pass

    def deleteSelected(self):
        pass

    def deleteEntire(self):
        pass

    def clearAbortToggle(self):
        pass

    def startPauseToggle(self):
        pass

    def clearProgram(self):
        pass

    def abortProgram(self):
        pass

    def startCorrection(self):
        pass

    def pauseCorrection(self):
        pass




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()

    ui.show()
    sys.exit(app.exec_())

