from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        windowSize = (1280, 720)

        self.resize(*windowSize)
        self.centralwidget = QtWidgets.QWidget()

        self.wholeLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        self.centralSplitter = QtWidgets.QSplitter(self.centralwidget)
        self.centralSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.leftSplitter = QtWidgets.QSplitter(self.centralSplitter)
        self.leftSplitter.setOrientation(QtCore.Qt.Vertical)

        self.unitSelectionAbstractWidget = QtWidgets.QWidget(self.leftSplitter)

        self.unitSelectionLayout = QtWidgets.QVBoxLayout(self.unitSelectionAbstractWidget)
        self.unitSelectionLayout.setContentsMargins(0, 0, 0, 0)

        self.unitLayout = QtWidgets.QHBoxLayout()

        self.unitLabel = QtWidgets.QLabel(self.unitSelectionAbstractWidget)

        self.unitLayout.addWidget(self.unitLabel)
        self.unitComboBox = QtWidgets.QComboBox(self.unitSelectionAbstractWidget)

        self.unitLayout.addWidget(self.unitComboBox)
        self.unitSelectionLayout.addLayout(self.unitLayout)
        self.unitListWidget = QtWidgets.QListWidget(self.unitSelectionAbstractWidget)

        self.unitSelectionLayout.addWidget(self.unitListWidget)
        self.addUnitButtonRowLayout = QtWidgets.QHBoxLayout()

        self.addSelectedButton = QtWidgets.QPushButton(self.unitSelectionAbstractWidget)

        self.addUnitButtonRowLayout.addWidget(self.addSelectedButton)
        self.addEntireButton = QtWidgets.QPushButton(self.unitSelectionAbstractWidget)

        self.addUnitButtonRowLayout.addWidget(self.addEntireButton)
        self.unitSelectionLayout.addLayout(self.addUnitButtonRowLayout)

        self.objectSelectionAbstractWidget = QtWidgets.QWidget(self.leftSplitter)

        self.objectSelectionLayout = QtWidgets.QVBoxLayout(self.objectSelectionAbstractWidget)
        self.objectSelectionLayout.setContentsMargins(0, 0, 0, 0)

        self.objectLabel = QtWidgets.QLabel(self.objectSelectionAbstractWidget)

        self.objectSelectionLayout.addWidget(self.objectLabel)
        self.objectListWidget = QtWidgets.QListWidget(self.objectSelectionAbstractWidget)

        self.objectSelectionLayout.addWidget(self.objectListWidget)
        self.deleteObjectButtonRowLayout = QtWidgets.QHBoxLayout()

        self.deleteSelectedButton = QtWidgets.QPushButton(self.objectSelectionAbstractWidget)

        self.deleteObjectButtonRowLayout.addWidget(self.deleteSelectedButton)
        self.deleteEntireButton = QtWidgets.QPushButton(self.objectSelectionAbstractWidget)

        self.deleteObjectButtonRowLayout.addWidget(self.deleteEntireButton)
        self.objectSelectionLayout.addLayout(self.deleteObjectButtonRowLayout)

        self.connectionInfoAbstractWidget = QtWidgets.QWidget(self.leftSplitter)

        self.connectionInfoLayout = QtWidgets.QVBoxLayout(self.connectionInfoAbstractWidget)
        self.connectionInfoLayout.setContentsMargins(0, 0, 0, 0)

        self.connectionInfoLabel = QtWidgets.QLabel(self.connectionInfoAbstractWidget)

        self.connectionInfoLayout.addWidget(self.connectionInfoLabel)
        self.connectionInfoBox = QtWidgets.QTextEdit(self.connectionInfoAbstractWidget)

        self.connectionInfoLayout.addWidget(self.connectionInfoBox)
        self.dateLayout = QtWidgets.QGridLayout()

        self.startDateLabel = QtWidgets.QLabel(self.connectionInfoAbstractWidget)
        self.startDateLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.dateLayout.addWidget(self.startDateLabel, 0, 0, 1, 1)
        self.startDateEdit = QtWidgets.QDateEdit(self.connectionInfoAbstractWidget)
        self.startDateEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.dateLayout.addWidget(self.startDateEdit, 1, 0, 1, 1)
        self.endDateLabel = QtWidgets.QLabel(self.connectionInfoAbstractWidget)
        self.endDateLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.dateLayout.addWidget(self.endDateLabel, 0, 1, 1, 1)
        self.endDateEdit = QtWidgets.QDateEdit(self.connectionInfoAbstractWidget)
        self.endDateEdit.setAlignment(QtCore.Qt.AlignCenter)

        self.dateLayout.addWidget(self.endDateEdit, 1, 1, 1, 1)
        self.connectionInfoLayout.addLayout(self.dateLayout)

        self.rightSplitter = QtWidgets.QSplitter(self.centralSplitter)
        self.rightSplitter.setOrientation(QtCore.Qt.Vertical)

        self.rightUpperSplitter = QtWidgets.QSplitter(self.rightSplitter)
        self.rightUpperSplitter.setOrientation(QtCore.Qt.Horizontal)

        self.detailOptionAbstractWidget = QtWidgets.QWidget(self.rightUpperSplitter)

        self.detailOptionLayout = QtWidgets.QVBoxLayout(self.detailOptionAbstractWidget)
        self.detailOptionLayout.setContentsMargins(0, 0, 0, 0)

        self.detailOptionGroupBoxLayout = QtWidgets.QGroupBox(self.detailOptionAbstractWidget)

        self.gridLayout = QtWidgets.QGridLayout(self.detailOptionGroupBoxLayout)

        self.sampleCheckBox = QtWidgets.QCheckBox(self.detailOptionGroupBoxLayout)

        self.gridLayout.addWidget(self.sampleCheckBox, 0, 1, 1, 1)
        self.sampleCheckBox2 = QtWidgets.QCheckBox(self.detailOptionGroupBoxLayout)

        self.gridLayout.addWidget(self.sampleCheckBox2, 1, 0, 1, 1)
        self.detailOptionLayout.addWidget(self.detailOptionGroupBoxLayout)
        self.runButtonLayout = QtWidgets.QHBoxLayout()

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.runButtonLayout.addItem(spacerItem)
        self.runButton = QtWidgets.QPushButton(self.detailOptionAbstractWidget)

        self.runButtonLayout.addWidget(self.runButton)
        self.detailOptionLayout.addLayout(self.runButtonLayout)

        self.resultAbstractWidget = QtWidgets.QWidget(self.rightUpperSplitter)

        self.resultLayout = QtWidgets.QVBoxLayout(self.resultAbstractWidget)
        self.resultLayout.setContentsMargins(0, 0, 0, 0)

        self.resultLabel = QtWidgets.QLabel(self.resultAbstractWidget)

        self.resultLayout.addWidget(self.resultLabel)
        self.resultListWidget = QtWidgets.QListWidget(self.resultAbstractWidget)

        self.resultLayout.addWidget(self.resultListWidget)

        self.previewAbstractWidget = QtWidgets.QWidget(self.rightSplitter)

        self.previewLayout = QtWidgets.QVBoxLayout(self.previewAbstractWidget)
        self.previewLayout.setContentsMargins(0, 0, 0, 0)

        self.previewLabel = QtWidgets.QLabel(self.previewAbstractWidget)

        self.previewLayout.addWidget(self.previewLabel)
        self.previewTableWidget = QtWidgets.QTableWidget(self.previewAbstractWidget)

        self.previewTableWidget.setColumnCount(0)
        self.previewTableWidget.setRowCount(0)
        self.previewLayout.addWidget(self.previewTableWidget)
        self.wholeLayout.addWidget(self.centralSplitter)


        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, windowSize[0], 21))

        self.menu_F = QtWidgets.QMenu(self.menubar)

        self.menu_S = QtWidgets.QMenu(self.menubar)

        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar()

        self.setStatusBar(self.statusbar)
        self.actionsave = QtWidgets.QAction()

        self.actionclose = QtWidgets.QAction()

        self.actionftp = QtWidgets.QAction()

        self.actionholiday = QtWidgets.QAction()

        self.actiontemp = QtWidgets.QAction()

        self.actionoffline = QtWidgets.QAction()

        self.menu_F.addAction(self.actionsave)
        self.menu_F.addAction(self.actionclose)
        self.menu_S.addAction(self.actionftp)
        self.menu_S.addAction(self.actionholiday)
        self.menu_S.addAction(self.actiontemp)
        self.menu_S.addAction(self.actionoffline)
        self.menubar.addAction(self.menu_F.menuAction())
        self.menubar.addAction(self.menu_S.menuAction())

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("MainWindow")
        self.unitLabel.setText("분석 단위")
        self.addSelectedButton.setText("선택 항목 추가")
        self.addEntireButton.setText("전체 항목 추가")
        self.objectLabel.setText("분석 대상")
        self.deleteSelectedButton.setText("선택 항목 삭제")
        self.deleteEntireButton.setText("전체 항목 삭제")
        self.connectionInfoLabel.setText("연결 정보")
        self.startDateLabel.setText("시작 일자")
        self.endDateLabel.setText("종료 일자")
        self.detailOptionGroupBoxLayout.setTitle("세부 설정")
        self.sampleCheckBox.setText("CheckBox")
        self.sampleCheckBox2.setText("CheckBox")
        self.runButton.setText("실행")
        self.resultLabel.setText("분석 결과")
        self.previewLabel.setText("미리보기")
        self.menu_F.setTitle("파일(F)")
        self.menu_S.setTitle("설정(S)")
        self.actionsave.setText("저장")
        self.actionsave.setIconText("저장")
        self.actionclose.setText("종료")
        self.actionftp.setText("서버 연결 설정")
        self.actionholiday.setText("평/휴일 정보 설정")
        self.actiontemp.setText("기온 정보 설정")
        self.actionoffline.setText("오프라인으로 실행")

        self.previewTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        self.addSelectedButton.clicked.connect(self.addSelected)
        self.addEntireButton.clicked.connect(self.addEntire)
        self.deleteSelectedButton.clicked.connect(self.deleteSelected)
        self.deleteEntireButton.clicked.connect(self.deleteEntire)
        self.runButton.clicked.connect(self.run)

                                        #top - right - bottom - left (clockwise) ; setting only top parent splitter would change all
        self.centralSplitter.setStyleSheet('QSplitter[orientation="1"]::handle {border-style : none ridge none ridge; \
                                        border-width: 0px 1px 0px 1px; border-color : grey; margin : 0px 3px 0px 3px} \
                                        QSplitter[orientation="2"]::handle {border-style : ridge none ridge none; \
                                        border-width: 1px 0px 1px 0px; border-color : grey; margin : 3px 0px 3px 0px}')

    def addSelected(self):
        pass

    def addEntire(self):
        pass

    def deleteSelected(self):
        pass

    def deleteEntire(self):
        pass

    def run(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.show()
    sys.exit(app.exec_())

