# -*- coding: utf-8 -*-
# self.setWindowTitle("자동 업로드 프로그램 v.1.0.0 (2019/05/16)")

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(561, 465)
        self.centralwidget = QtWidgets.QWidget(self)

        self.wholeLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.leftColumnLayout = QtWidgets.QVBoxLayout()

        self.openFileButtonRowLayout = QtWidgets.QHBoxLayout()

        self.openFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.openFileButtonRowLayout.addWidget(self.openFileButton)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.openFileButtonRowLayout.addItem(spacerItem)

        self.leftColumnLayout.addLayout(self.openFileButtonRowLayout)

        self.buildingForUploadLabel = QtWidgets.QLabel(self.centralwidget)
        self.leftColumnLayout.addWidget(self.buildingForUploadLabel)

        self.buildingForUploadList = QtWidgets.QListWidget(self.centralwidget)
        self.buildingForUploadList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.leftColumnLayout.addWidget(self.buildingForUploadList)

        self.deleteButtonRowLayout = QtWidgets.QHBoxLayout()

        self.deleteSelectedButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButtonRowLayout.addWidget(self.deleteSelectedButton)

        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.deleteButtonRowLayout.addItem(spacerItem1)

        self.deleteEntireButton = QtWidgets.QPushButton(self.centralwidget)
        self.deleteButtonRowLayout.addWidget(self.deleteEntireButton)

        self.leftColumnLayout.addLayout(self.deleteButtonRowLayout)

        self.wholeLayout.addLayout(self.leftColumnLayout)

        self.leftToRightLabel = QtWidgets.QLabel(self.centralwidget)
        self.wholeLayout.addWidget(self.leftToRightLabel)

        self.rightColumnLayout = QtWidgets.QVBoxLayout()

        self.setDetailButtonRowLayout = QtWidgets.QHBoxLayout()

        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.setDetailButtonRowLayout.addItem(spacerItem2)

        self.setDetailButton = QtWidgets.QPushButton(self.centralwidget)
        self.setDetailButtonRowLayout.addWidget(self.setDetailButton)

        self.rightColumnLayout.addLayout(self.setDetailButtonRowLayout)

        self.buildingUploadedLabel = QtWidgets.QLabel(self.centralwidget)
        self.rightColumnLayout.addWidget(self.buildingUploadedLabel)

        self.buildingUploadedList = QtWidgets.QListWidget(self.centralwidget)
        self.rightColumnLayout.addWidget(self.buildingUploadedList)

        self.startUploadButtonRowLayout = QtWidgets.QHBoxLayout()

        self.startUploadButton = QtWidgets.QPushButton(self.centralwidget)
        self.startUploadButtonRowLayout.addWidget(self.startUploadButton)

        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.startUploadButtonRowLayout.addItem(spacerItem3)

        self.remainingTimeNameLabel = QtWidgets.QLabel(self.centralwidget)
        self.startUploadButtonRowLayout.addWidget(self.remainingTimeNameLabel)

        self.remainingTimeShowLabel = QtWidgets.QLabel(self.centralwidget)
        self.startUploadButtonRowLayout.addWidget(self.remainingTimeShowLabel)

        self.rightColumnLayout.addLayout(self.startUploadButtonRowLayout)

        self.wholeLayout.addLayout(self.rightColumnLayout)

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar()

        self.setStatusBar(self.statusbar)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("자동 업로드 프로그램 v.1.0.0 (2019/5/16)")
        self.openFileButton.setText("대상 파일 열기")
        self.buildingForUploadLabel.setText("업로드할 파일")
        self.deleteSelectedButton.setText("선택 항목 삭제")
        self.deleteEntireButton.setText("전체 항목 삭제")
        self.leftToRightLabel.setText("▶▶▶")
        self.setDetailButton.setText("세부 설정")
        self.buildingUploadedLabel.setText("업로드된 파일")
        self.startUploadButton.setText("업로드 시작")
        self.remainingTimeNameLabel.setText("예상 잔여 시간")
        self.remainingTimeShowLabel.setText("0:00")

        self.openFileButton.clicked.connect(self.openFiles)
        self.setDetailButton.clicked.connect(self.setDetails)
        self.deleteSelectedButton.clicked.connect(self.deleteSelected)
        self.deleteEntireButton.clicked.connect(self.deleteEntire)
        self.startUploadButton.clicked.connect(self.startUpload)

    def openFiles(self):
        pass

    def setDetails(self):
        pass

    def deleteSelected(self):
        pass

    def deleteEntire(self):
        pass

    def startUpload(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

