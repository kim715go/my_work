# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pandas as pd
from filterWidget import FilterWidget

class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.resize(853, 749)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)

        self.openFileButtonLayout = QtWidgets.QHBoxLayout()

        self.openFileButton = QtWidgets.QPushButton()
        self.openFileButtonLayout.addWidget(self.openFileButton)
        horizontalSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.openFileButtonLayout.addItem(horizontalSpacer)

        self.verticalLayout.addLayout(self.openFileButtonLayout)

        self.dataTable = QtWidgets.QTableWidget()
        self.dataTable.setColumnCount(0)
        self.dataTable.setRowCount(0)

        self.horizontalHeader = self.dataTable.horizontalHeader()
        self.horizontalHeader.sectionClicked.connect(self.showTableFilter)

        self.verticalLayout.addWidget(self.dataTable)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.verticalLayout.addWidget(self.buttonBox)

        self.keywords = dict([(i, []) for i in range(self.dataTable.columnCount())])

        self.retranslateUi()

        self.tables = []

    def retranslateUi(self):
        self.setWindowTitle("Form")
        self.openFileButton.setText("Open file..")

        self.openFileButton.clicked.connect(self.openFiles)

    def openFiles(self):
        pathList, _ = QtWidgets.QFileDialog.getOpenFileName(self, "파일 불러오기", filter="csv 파일 (*.csv);;엑셀 파일 (*.xlsx *.xls)")
        table = self.openFile(pathList)
        if type(table) is pd.DataFrame :
            self.tables.append(table)
            self.showTable(self.tables[0])

    def openFile(self, path):
        if path.endswith(".csv"):
            try :
                table = pd.read_csv(path, engine='python', index_col=0, parse_dates=True)
            except UnicodeDecodeError:
                table = pd.read_csv(path, engine='python', index_col=0, parse_dates=True, encoding='euc-kr')
            except FileNotFoundError:
                QtWidgets.QMessageBox.warning(self, "파일 경로 오류", "주어진 경로의 파일이 존재하지 않습니다.\n" + path, QtWidgets.QMessageBox.Ok)
                return
        else :
            table = pd.read_excel(path)

        return table

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


    def slotSelect(self, state):
        for checkbox in self.checkBoxs:
            checkbox.setChecked(QtCore.Qt.Checked == state)

    def showTableFilter(self, index):
        menu = FilterWidget()
        headerPos = self.dataTable.mapToGlobal(self.horizontalHeader.pos())

        uniqueItems = self.tables[0].iloc[:,index].drop_duplicates().values

        menu.setListItems(uniqueItems)

        posY = headerPos.y() + self.horizontalHeader.height()
        posX = headerPos.x() + self.horizontalHeader.sectionPosition(index)
        menu.move(QtCore.QPoint(posX, posY))
        menu.exec_()

        print(menu.checkedItems())

    # def on_view_horizontalHeader_sectionClicked(self, index):
    #     # self.clearFilter()
    #     self.menu = QtWidgets.QMenu(self)
    #     self.col = index
    #
    #     data_unique = []
    #
    #     self.checkBoxs = []
    #
    #     btn = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
    #                                  QtCore.Qt.Horizontal, self.menu)
    #     btn.accepted.connect(self.menuClose)
    #     btn.rejected.connect(self.menu.close)
    #     checkableAction = QtWidgets.QWidgetAction(self.menu)
    #     checkableAction.setDefaultWidget(btn)
    #     self.menu.addAction(checkableAction)
    #
    #     checkBox = QtWidgets.QCheckBox("Select all", self.menu)
    #     checkableAction = QtWidgets.QWidgetAction(self.menu)
    #     checkableAction.setDefaultWidget(checkBox)
    #     self.menu.addAction(checkableAction)
    #     checkBox.setChecked(True)
    #     checkBox.stateChanged.connect(self.slotSelect)
    #
    #     for i in range(self.dataTable.rowCount()):
    #         if not self.dataTable.isRowHidden(i):
    #             item = self.dataTable.item(i, index)
    #             if item.text() not in data_unique:
    #                 data_unique.append(item.text())
    #                 checkBox = QtWidgets.QCheckBox(item.text(), self.menu)
    #                 checkBox.setChecked(True)
    #                 checkableAction = QtWidgets.QWidgetAction(self.menu)
    #                 checkableAction.setDefaultWidget(checkBox)
    #                 self.menu.addAction(checkableAction)
    #                 self.checkBoxs.append(checkBox)
    #
    #
    #     g = self.dataTable.mapToGlobal(self.horizontalHeader.pos())
    #     # headerPos = self.dataTable.mapToGlobal(self.horizontalHeader.pos())
    #
    #     posY = self.dataTable.mapToGlobal(self.horizontalHeader.pos()).y() + self.horizontalHeader.height()
    #     # posY = headerPos.y()
    #     posX = self.dataTable.mapToGlobal(self.horizontalHeader.pos()).x() + self.horizontalHeader.sectionPosition(index)
    #
    #     self.menu.setStyleSheet("QMenu { menu-scrollable: 1; menu-fillscreenwithscroll:0; }")
    #     # self.menu.setStyleSheet("QMenu { menu-scrollable: 1; overflow: auto;}")
    #     # self.menu.setStyleSheet("QMenu { height: auto; max-height:300px; }")
    #
    #     print(posX, posY)
    #     self.menu.exec_(QtCore.QPoint(posX, posY))

    def menuClose(self):
        self.keywords[self.col] = []
        for element in self.checkBoxs:
            if element.isChecked():
                self.keywords[self.col].append(element.text())
        self.filterdata()
        self.menu.close()


    def clearFilter(self):
        for i in range(self.dataTable.rowCount()):
            self.dataTable.setRowHidden(i, False)

    def filterdata(self):

        columnsShow = dict([(i, True) for i in range(self.dataTable.rowCount())])

        for i in range(self.dataTable.rowCount()):
            for j in range(self.dataTable.columnCount()):
                item = self.dataTable.item(i, j)
                if self.keywords[j]:
                    if item.text() not in self.keywords[j]:
                        columnsShow[i] = False
        for key, value in columnsShow.iteritems():
            self.dataTable.setRowHidden(key, not value)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyle(CustomStyle())
    ui = Ui_Form()
    ui.show()
    sys.exit(app.exec_())

