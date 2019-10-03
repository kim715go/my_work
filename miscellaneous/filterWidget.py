# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

class FilterWidget(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(200, 330)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.upperButtonLayout = QtWidgets.QHBoxLayout()
        self.selectAllButton = QtWidgets.QPushButton()
        self.upperButtonLayout.addWidget(self.selectAllButton)

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.upperButtonLayout.addItem(spacerItem)

        self.sortButton = QtWidgets.QPushButton()
        self.upperButtonLayout.addWidget(self.sortButton)
        self.verticalLayout.addLayout(self.upperButtonLayout)

        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # self.listWidget.setDragEnabled(True)
        # self.listWidget.setDragDropMode(QtWidgets.QListWidget.InternalMove)

        self.verticalLayout.addWidget(self.listWidget)

        self.numOfUniqueLabel = QtWidgets.QLabel()
        self.verticalLayout.addWidget(self.numOfUniqueLabel)

        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.checkState = True

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Dialog")
        self.selectAllButton.setText("전체 선택/해제")
        self.sortButton.setText("오름차순으로 정렬")
        self.numOfUniqueLabel.setText("준비")
        # self.listWidget.setSortingEnabled(True)

        self.selectAllButton.clicked.connect(self.changeAllCheckState)
        self.sortButton.clicked.connect(self.sort)

    def setListItems(self, items):
        self.listWidget.clear()

        for item in items :
            temp = QtWidgets.QListWidgetItem()
            temp.setCheckState(QtCore.Qt.Checked)
            temp.setText(str(item))
            self.listWidget.addItem(temp)

        self.numOfUniqueLabel.setText("고유값 : %d개" % len(items))

    def changeAllCheckState(self):
        length = self.listWidget.count()
        if self.checkState : # checkState True; all Checked
            checkState = QtCore.Qt.Unchecked
            self.checkState = False
        else :
            checkState = QtCore.Qt.Checked
            self.checkState = True

        for i in range(length) :
            item = self.listWidget.item(i)
            item.setCheckState(checkState)

    def sort(self):
        self.listWidget.sortItems()

    def checkedItems(self):
        length = self.listWidget.count()
        res = []
        if length :
            for i in range(length) :
                item = self.listWidget.item(i)
                if item.checkState() == QtCore.Qt.Checked :
                    res.append(item.text())
        return res

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = FilterWidget()
    ui.show()
    sys.exit(app.exec_())

