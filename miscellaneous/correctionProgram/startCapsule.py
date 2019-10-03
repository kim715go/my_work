# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd


class Ui_Dialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.resize(464, 144)
        self.sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setMinimumSize(QtCore.QSize(464, 144))
        self.setMaximumSize(QtCore.QSize(464, 144))
        self.totalLayout = QtWidgets.QVBoxLayout(self)

        self.dataLabel = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dataLabel.sizePolicy().hasHeightForWidth())
        self.dataLabel.setSizePolicy(sizePolicy)
        self.totalLayout.addWidget(self.dataLabel)

        self.gridLayout = QtWidgets.QGridLayout()

        self.metaPath = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.metaPath, 1, 1, 1, 1)

        self.bldgPath = QtWidgets.QLineEdit(self)
        self.gridLayout.addWidget(self.bldgPath, 0, 1, 1, 1)

        self.bldgLabel = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.bldgLabel, 0, 0, 1, 1)

        self.metaLabel = QtWidgets.QLabel(self)
        self.gridLayout.addWidget(self.metaLabel, 1, 0, 1, 1)

        self.bldgButton = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.bldgButton, 0, 2, 1, 1)

        self.metaButton = QtWidgets.QPushButton(self)
        self.gridLayout.addWidget(self.metaButton, 1, 2, 1, 1)

        self.totalLayout.addLayout(self.gridLayout)

        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.totalLayout.addItem(spacerItem)

        self.lowerLayout = QtWidgets.QHBoxLayout()

        self.checkBox = QtWidgets.QCheckBox(self)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.lowerLayout.addWidget(self.checkBox)

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Reset)
        self.lowerLayout.addWidget(self.buttonBox)
        self.totalLayout.addLayout(self.lowerLayout)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Reset).clicked.connect(self.reset)

        self.bldgButton.clicked.connect(lambda : self.getFilePath('bldg'))
        self.metaButton.clicked.connect(lambda : self.getFilePath('meta'))


    def retranslateUi(self):
        self.setWindowTitle("프로그램 실행하기")
        self.dataLabel.setText("데이터 파일 열기")
        self.bldgLabel.setText("전력 데이터")
        self.metaLabel.setText("건물 메타데이터")
        self.bldgButton.setText("파일 열기")
        self.metaButton.setText("파일 열기")
        self.checkBox.setText("앞으로도 이 파일을 계속 사용")

        self.bldgPath.setReadOnly(True)
        self.metaPath.setReadOnly(True)


    def getFile(self, whereToShow):
        pass

    def reset(self):
        self.bldgPath.clear()
        self.metaPath.clear()
        self.checkBox.setChecked(False)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_Dialog()
    ui.show()

    sys.exit(app.exec_())

