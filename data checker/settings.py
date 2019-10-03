# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(280, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMinimumSize(QtCore.QSize(280, 100))
        Dialog.setMaximumSize(QtCore.QSize(280, 100))
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.sameConsecLabel = QtWidgets.QLabel(Dialog)
        self.sameConsecLabel.setObjectName("sameConsecLabel")
        self.gridLayout.addWidget(self.sameConsecLabel, 1, 0, 1, 1)
        self.credibSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.credibSpinBox.setObjectName("credibSpinBox")
        self.gridLayout.addWidget(self.credibSpinBox, 2, 1, 1, 1)
        self.sameConsecSpinBox = QtWidgets.QSpinBox(Dialog)
        self.sameConsecSpinBox.setObjectName("sameConsecSpinBox")
        self.gridLayout.addWidget(self.sameConsecSpinBox, 1, 1, 1, 1)
        self.credibLabel = QtWidgets.QLabel(Dialog)
        self.credibLabel.setObjectName("credibLabel")
        self.gridLayout.addWidget(self.credibLabel, 2, 0, 1, 1)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "세부 설정"))
        self.sameConsecLabel.setText(_translate("Dialog", "동일 측정값 이상 기준 횟수"))
        self.credibSpinBox.setSuffix(_translate("Dialog", "%"))
        self.credibLabel.setText(_translate("Dialog", "오류 검출 신뢰도"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("Dialog", "New Row"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "New Column"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.item(0, 0)
        item.setText(_translate("Dialog", "1"))
        self.tableWidget.setSortingEnabled(__sortingEnabled)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

