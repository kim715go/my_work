# 자동 업로드 프로그램 v.1.0.0 (2019/5/16)
# 자동 업로드 프로그램 v.1.0.1 (2019/5/16)
# 자동 업로드 프로그램 v.1.0.2 (2019/6/19) (경로명에 공백이 있을 경우 발생하는 오류 수정)

import autoUploaderUI as aU

from PyQt5 import QtWidgets, QtCore, QtGui

from pywinauto.findwindows import find_windows
from pywinauto.application import Application
from time import time as currentTimeStamp
from time import sleep

from datetime import datetime


class UploadMachine(QtCore.QThread):
    sendStatusMessageSignal = QtCore.pyqtSignal(str)
    uploadFinishedSignal = QtCore.pyqtSignal(str)
    updateRemainingTimeSignal = QtCore.pyqtSignal(str)

    def __init__(self, argsFromKernel):
        super().__init__()
        self.windowName = argsFromKernel['windowName']
        self.filePathForUpload = argsFromKernel['uploadList'][:]
        self.ocrFileOpenButtonCoords = (155, 660)

    def run(self):
        totalLength = len(self.filePathForUpload)
        count = 0

        ocrMainApp = Application()
        ocrPopupApp = Application()
        ocrFileOpenApp = Application()

        window = find_windows(title= self.windowName)

        ocrMainWindow = ocrMainApp.connect(handle = window[0])
        ocrMainWindow = ocrMainApp.window(handle = window[0])

        while count < totalLength :
            ocrMainWindow.click_input(coords = self.ocrFileOpenButtonCoords)

            startTime = currentTimeStamp()
            path = self.filePathForUpload[count]

            fileOpen = find_windows(title = "열기")
            ocrFileOpenApp = Application()
            ocrFileOpenWindow = ocrFileOpenApp.connect(handle = fileOpen[0])
            ocrFileOpenWindow = ocrFileOpenApp.window(handle = fileOpen[0])
            ocrFileOpenWindow.type_keys(path, with_spaces = True) # 1.0.2에서 수정
            sleep(0.1)
            ocrFileOpenWindow.type_keys('{ENTER}')

            sleep(0.4)

            window2 = find_windows(title = self.windowName)
            ocrPopupApp = Application()
            ocrPopupWindow = ocrPopupApp.connect(handle= window2[0])
            ocrPopupWindow = ocrPopupApp.window(handle = window2[0])
            ocrPopupWindow.type_keys('y')

            message = " ".join(["(", str(count+1), "/", str(totalLength), ")", path, "업로드 중..."])
            self.sendStatusMessageSignal.emit(message)


            while True :
                tempWindow = find_windows(title = self.windowName)
                if len(tempWindow) == 3 :
                    break
                sleep(5)


            ocrPopupApp = Application()
            ocrPopupWindow = ocrPopupApp.connect(handle = tempWindow[0])
            ocrPopupWindow = ocrPopupApp.window(handle = tempWindow[0])
            ocrPopupWindow.type_keys('{ENTER}')

            count += 1

            self.uploadFinishedSignal.emit(path)
            sleep(0.1)

            endTime = currentTimeStamp()

            timeSpentForEach = round((endTime - startTime) * (totalLength-count))
            minutes = timeSpentForEach // 60
            seconds = timeSpentForEach % 60
            remainingTime = "".join([str(minutes), ":", str(seconds)])
            self.updateRemainingTimeSignal.emit(remainingTime)

        self.sendStatusMessageSignal.emit("업로드 완료")


class Kernel(aU.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.windowName = '오토베이스_OCR'

        self.fileForUploadPathList = []
        self.fileUploadedPathList = []

        self.statusMessage = "준비"
        self.statusbar.showMessage(self.statusMessage)

        self.uploadEngine = ""
        self.argsForUploadEngine = {'windowName':self.windowName, 'uploadList':self.fileForUploadPathList}

        self.setDetailButton.setEnabled(False)

        self.logfileName = ""

        self.setWindowTitle("자동 업로드 프로그램 v.1.0.2 (2019/6/19)")

    def openFiles(self):
        pathList, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "파일 불러오기", filter="csv 파일 (*.csv)",
                                                             options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if pathList :
            for path in pathList :
                if path not in self.fileForUploadPathList:
                    path = path.replace('/', "\\")
                    self.buildingForUploadList.addItem(path)
                    self.fileForUploadPathList.append(path)

    def deleteFromUploadList(self, selected):
        for path in selected:
            if path in self.fileForUploadPathList:
                self.fileForUploadPathList.remove(path)

        self.buildingForUploadList.clear()
        if self.fileForUploadPathList :
            self.buildingForUploadList.addItems(self.fileForUploadPathList)

    def deleteSelected(self):
        selectedItems = [x.text() for x in self.buildingForUploadList.selectedItems()]
        self.deleteFromUploadList(selectedItems)

    def deleteEntire(self):
        self.buildingForUploadList.selectAll()
        self.deleteSelected()
        self.updateStatusMessage(self.statusMessage)

    def getOCRHandle(self):
        return find_windows(title = self.windowName)

    @QtCore.pyqtSlot(str)
    def updateStatusMessage(self, message):
        self.statusbar.showMessage(message)

    @QtCore.pyqtSlot(str)
    def moveToFinished(self, finishedPath):
        self.deleteFromUploadList([finishedPath])
        self.fileUploadedPathList.append(finishedPath)
        self.buildingUploadedList.addItem(finishedPath)
        self.recordLogfile(finishedPath)

    @QtCore.pyqtSlot(str)
    def updateRemainingTime(self, remainingTimeString):
        self.remainingTimeShowLabel.setText(remainingTimeString)

    def getLogfileName(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileDialog.setDefaultSuffix("txt")
        while True :
            logfileName, _ = fileDialog.getSaveFileName(self, "로그 파일 저장", '저장 현황 로그', filter = "텍스트 파일 (*.txt)",
                                                        options=QtWidgets.QFileDialog.DontUseNativeDialog)
            if logfileName :
                if not logfileName.endswith(".txt") :
                    logfileName += ".txt"
                break
        self.logfileName = logfileName
        print(logfileName)

    def recordLogfile(self, content):
        with open(self.logfileName, 'a+') as f :
            f.write("".join([datetime.today().strftime("%Y%m%d %H:%M:%S"), " ",  content, '\n']))

    def startUpload(self):
        windowHandles = self.getOCRHandle()

        if windowHandles :
            self.getLogfileName()

            self.uploadEngine = UploadMachine(self.argsForUploadEngine)
            self.uploadEngine.sendStatusMessageSignal.connect(self.updateStatusMessage)
            self.uploadEngine.uploadFinishedSignal.connect(self.moveToFinished)
            self.uploadEngine.updateRemainingTimeSignal.connect(self.updateRemainingTime)

            self.uploadEngine.start()

        else :
            QtWidgets.QMessageBox.warning(self, "OCR 프로그램 없음", "OCR 프로그램을 먼저 실행시켜 주세요", QtWidgets.QMessageBox.Ok)
            return


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Kernel()
    ui.show()
    sys.exit(app.exec_())
