#ver 1.6.1 (2019/3/18)
#두 번 이상 클릭해야 열 수 있는 배전도 반영

# importing modules
from PyQt5 import QtCore, QtGui, QtWidgets

from pywinauto import application
from pywinauto.findwindows import find_window, WindowNotFoundError

from datetime import timedelta, datetime, date

from mss import tools
import mss

from cv2 import cv2
import numpy as np

from os import rename, mkdir
from pywinauto import mouse
from pywinauto import keyboard

from time import sleep
from random import sample as randomSample
from string import ascii_letters

from os.path import isdir

from pandas import read_excel

import sys


# 이 클래스는 연/월 문자열을 조금 더 편리하게 사용하기 위해 만든 것입니다.
# 캡처한 화면을 저장할 때 파일 이름 등에 활용됩니다.
class YearMonth():
    def __init__(self, year, month):
        if year > 0 and month > 0 and month < 13 : 
            pass
        else : 
            raise ValueError("invalid year or month input")
        self.year = year
        self.month = month
    
    def __str__(self):
        return str(self.year) + "/" + str(self.month)
    
    def reduceMonth(self, times) : 
        leap = self.month - times
        if leap > 0 : 
            self.month = leap
        else : 
            yearLeap = leap // 12
            monthLeap = leap % 12
            
            if monthLeap == 0 : 
                self.year += yearLeap - 1
                self.month = 12
            else : 
                self.year += yearLeap
                self.month = monthLeap
        
    def reduceYear(self, times) : 
        self.year -= times
        
    def returnType(self, year=True, month=True) : 
        if year and month : 
            return str(self.year) + str(self.month).zfill(2)
        elif year : 
            return str(self.year)
        elif month : 
            return str(self.month).zfill(2)
        else : 
            raise ValueError('either year or month should be true')


def _captureRepeatPart(sct, output, windows):
    sleep(0.4)
    sct_img = sct.grab(monitor)
    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    #windows['ab'].type_keys('{VK_SUBTRACT}')
    windows['ab'].set_focus()
    keyboard.send_keys('{VK_SUBTRACT}')
    

def createFolder(folderName) : 
    if not isdir(folderName) : 
        mkdir(folderName)
    

def captureSave(option, tagName, endPoint, repTime, screen, fileNamePrefix, status, windows, isSimple) :
    numOfShot = 0
        
    if option == 'd' : 
        if isSimple :
           folderName = tagName
        else :
            folderName = tagName +'/' + 'hourly'
            createFolder(folderName)

        while status['isRunning'] and numOfShot <= repTime:
            if status['isPaused'] :
                pass
            else :
                output = folderName+'/'+fileNamePrefix + endPoint.strftime('%Y%m%d')+'.png'
                _captureRepeatPart(screen, output, windows)
                numOfShot += 1
                endPoint -= timedelta(days=1)

    elif option == 'm' :
        if isSimple :
            folderName = tagName
        else :
            folderName = tagName + '/' + 'monthly'
            createFolder(folderName)
        
        endPoint = YearMonth(endPoint.year, endPoint.month)

        while status['isRunning'] and numOfShot <= repTime :
            if status['isPaused'] :
                pass
            else :
                output = folderName + '/' + fileNamePrefix + endPoint.returnType()+'.png'
                _captureRepeatPart(screen, output, windows)
                numOfShot += 1
                endPoint.reduceMonth(1)
    
    elif option == 'y' :
        if isSimple :
            folderName = tagName
        else :
            folderName = tagName +'/' + 'yearly'
            createFolder(folderName)

        endPoint = YearMonth(endPoint.year, endPoint.month)

        while status['isRunning'] and numOfShot <= repTime :
            if status['isPaused'] :
                pass
            else :
                output = folderName + '/' + fileNamePrefix + endPoint.returnType(month=False)+'.png'
                _captureRepeatPart(screen, output, windows)
                numOfShot += 1
                endPoint.reduceYear(1)
        

today = date.today()
# startDate = date(2017,1,1)
# endDate = date(2018,10,31)
# bldName = "인문관5동"
# option = {'y'} #d for days(hourly data), m for months(daily data), y for years(monthly data)

###getting building pictures
def windowWrapper(windowNameInRegex) :
    app = application.Application()
    handle = find_window(title_re = windowNameInRegex)
    window = app.connect(handle = handle)
    window = app.window(handle = handle)
    return window

# findWindowAndFocus('.*Web.*')

def captureCurrent(fileName):
    with mss.mss() as sct : 
        sct.shot(output = fileName)


# ###getting realFiles######

# #### detecting positions of tags 

# image = cv2.imread(tagFileName)

def rawImageAndContours(fileName) :
    image = cv2.imread(fileName)

    #converting image into hue - saturation - value(brightness)
    hsvCon = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # masking image to extract tag positions
    hsvLow = np.array([55, 0, 0], np.uint8)
    hsvHigh = np.array([179, 255, 255], np.uint8)
    mask = cv2.inRange(hsvCon, hsvLow, hsvHigh)

    # finding the contours
    contours = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[1]

    return image, contours

monitor = {'top':140, 'left':10, 'height':520-140, 'width':555-10}
yPosArrange = 5/6
# contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]


def addInfoOfOption(optionList, startDate, endDate) :
    optionWithInfo = {}
    for opt in optionList :
        info = [] #the first item indicates how many times the '-' key should be pressed \
                  #  to get to the last day of our period of interest
                  #the second item indicates how many times the '-' key should be pressed \
                  #  to get to the first day of our period of interest from the last day
                  #the third item is the key to access the specific period page
        if opt == 'd':
            info = [(today - endDate).days, (endDate - startDate).days, 'o']

        elif opt == 'm':
            info = [(today.year - endDate.year)*12 + today.month - endDate.month,
                    (endDate.year - startDate.year)*12 + endDate.month - startDate.month, 'y']

        elif opt =='y' :
            info = [today.year - endDate.year, endDate.year - startDate.year, 'm']

        optionWithInfo[opt] = info

    return optionWithInfo

def checkIfRectangle(image, singleContour) :
    #dependent on the global 'image' variable
    M = cv2.moments(singleContour)
    contourPerimeter = cv2.arcLength(singleContour, True)
    approximation = cv2.approxPolyDP(singleContour, 0.09*contourPerimeter, True)

    if len(approximation) == 4 :
        if M['m00'] > 100 :
            groupX = np.sort([x[0][0] for x in approximation])
            groupY = np.sort([x[0][1] for x in approximation])

            if image[groupY[0] + 3][groupX[3] - 3][0] == 112 or image[groupY[0] + 3][groupX[3] - 3][1] == 112 :

                #########getting what we want
                xPosMouse = int(np.mean(groupX))
                yPosMouse = int(groupY[0] + yPosArrange * (groupY[3] - groupY[0]))

                mouse.click(button='right', coords=(xPosMouse, yPosMouse))
                keyboard.send_keys('o')
                sleep(.3)

                with mss.mss() as sct:
                    img = sct.grab({'top': 144, 'left': 14, 'height': 1, 'width': 1})

                    if img.pixel(0, 0) != (236, 233, 216):
                        return False,

                    else:
                        keyboard.send_keys('{ESC}')
                        return True, (groupX[3], groupY[3]), (xPosMouse, yPosMouse)
                        # first for checking whether it is a rectangle
                        # second for writing tag number on the taglistpicture.png
                        # third for moving mouse pointer to do the capture

            else :
                return False,
        else :
            return False,
    else :
        return False,


# count = 0 (add by 1 every time a valid tag is found)
def mainWork(image, tagNumber, optionWithInfo, req, contour, tagName, tagNamePosition, tagDetailPosition, dummyFolderName, status, windows, isSimple):
    contour = contour.astype('int')
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.putText(image, str(tagNumber), tagNamePosition, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
    tagNameWithFolder = dummyFolderName + "/" + tagName
    createFolder(tagNameWithFolder)

    totalLength = len(optionWithInfo)
    keyList = list(optionWithInfo.keys())
    count = 0
    while status['isRunning'] and count < totalLength :
        if status['isPaused'] :
            pass
        else :
            #windows['ab'].set_focus()
            mouse.click(button='right', coords = tagDetailPosition)
            sleep(0.5)
            keyboard.send_keys(optionWithInfo[keyList[count]][2])
            #windows['ab'].type_keys(optionWithInfo[keyList[count]][2])
            sleep(0.3)
            keyboard.send_keys('{F2 3}')
            #windows['ab'].type_keys('{F2 3}')
            sleep(0.1)
            keyboard.send_keys('{VK_SUBTRACT '+str(optionWithInfo[keyList[count]][0])+'}')
            #windows['ab'].type_keys('{VK_SUBTRACT '+str(optionWithInfo[keyList[count]][0])+'}')
            sleep(0.2)

            with mss.mss() as sct :
                captureSave(keyList[count], tagNameWithFolder, req['endDate'], optionWithInfo[keyList[count]][1], sct, req['fileNamePrefix'], status, windows, isSimple)

            count += 1
            windows['ab'].set_focus()
            keyboard.send_keys('{ESC}')
            #windows['ab'].type_keys('{ESC}')
            sleep(0.3)
    #windows['ab'].type_keys('{ESC}')
    windows['ab'].set_focus()
    keyboard.send_keys('{ESC}')


def returnCurrentTime():
    return "".join(['[',datetime.now().strftime("%H:%M:%S"),']'])


class CaptureFunc(QtCore.QObject) :

    statusSig = QtCore.pyqtSignal(str)

    def __init__(self, req, isSimple, wholeFolderName, status, windows) :
        super().__init__()
        self.req= req
        self.isSimple = isSimple
        self.wholeFolderName = wholeFolderName
        self.status = status
        self.windows = windows

    def run(self) : 
        self.dummyFolderName = self.wholeFolderName + '/' + "".join(randomSample(ascii_letters, 10))
        self.dummyTagFileName = self.dummyFolderName + '/' + 'taglistPicture.png'
        # capturing the current view
        createFolder(self.dummyFolderName)
        captureCurrent(self.dummyTagFileName)

        # opening the tag view
        image, contours = rawImageAndContours(self.dummyTagFileName)

        # setting option information
        optionWithInfo = addInfoOfOption(self.req['option'], self.req['startDate'], self.req['endDate'])

        self.statusSig.emit("".join(["건물 정보 및 옵션 로딩 완료. 캡처를 시작합니다. ", returnCurrentTime()]))

        # doing the main work
        tagNumber = 0
        count = 0
        totalLen = len(contours)
        while self.status['isRunning'] and count < totalLen :
            if self.status['isPaused'] :
                pass
            else :
                checkInfo = checkIfRectangle(image, contours[count])
                if checkInfo[0] :
                    tagNumber += 1
                    tagName = 'tag' + str(tagNumber)
                    self.statusSig.emit("".join([tagName, ' 캡처를 시작합니다. ', returnCurrentTime()]))
                    mainWork(image, tagNumber, optionWithInfo, self.req, contours[count], tagName, checkInfo[1], checkInfo[2], self.dummyFolderName, self.status, self.windows, self.isSimple)
                                                                                            # checkInfo[1] : for writing tag number on the taglistpicture.png
                                                                                            # checkInfo[2] : for moving mouse pointer to do the capture
                    self.statusSig.emit("".join([tagName, ' 캡처가 완료되었습니다. ', returnCurrentTime()]))

            count += 1

        if self.status['isRunning'] :
            self.finalWork(image)
            self.statusSig.emit("".join(["캡처가 완료되었습니다. ", returnCurrentTime() ]))

    def finalWork(self, image):
        cv2.imwrite(self.dummyTagFileName, image)
        if self.req['bldName'] :
            rename(self.dummyTagFileName, self.dummyFolderName + '/' + self.req['bldName'] + '.png')
            rename(self.dummyFolderName, self.wholeFolderName + '/' + self.req['bldName'])
        self.windows['pr'].set_focus()


class WholeCaptureThread(QtCore.QThread) : 
    wholeSignal = QtCore.pyqtSignal(str)
    updateStatusSignal = QtCore.pyqtSignal(str)
    finishedSignal = QtCore.pyqtSignal()

    def __init__(self, req, captureOptions, status, bldPosTable, windows) :
        super().__init__()
        self.req = req
        self.captureOptions = captureOptions
        self.status = status
        self.bldPosTable = bldPosTable
        self.windows = windows
        self.wholeFolderName = datetime.now().strftime("%Y%m%d_%H%M%S")
        createFolder(self.wholeFolderName)

    def changeBldName(self, targetBldName) : 
        self.req['bldName'] = targetBldName
        if self.req['fileNamePrefix'] == "" or self.req['fileNamePrefix'] == "_" : 
            pass
        else : 
            self.req['fileNamePrefix'] = self.req['bldName'] + "_"

    def obtainUnitCaptureClass(self, unitCaptureClass):
        self.unitCap = unitCaptureClass

    def run(self) :
        if self.captureOptions['isWhole']:
            self.wholeSignal.emit("건물 전체 위치 로딩 완료. " + returnCurrentTime())

            bldList = self.bldPosTable.건물명.unique()
            totalLength = len(bldList)
            count = 0
            while self.status['isRunning'] and count < totalLength :
                if self.status['isPaused'] :
                        pass
                else :
                    self.windows['ab'].set_focus()
                    eachBldPos = self.bldPosTable.loc[self.bldPosTable['건물명'] == bldList[count]]
                    howManyClicks = eachBldPos.shape[0]
                    for i in range(howManyClicks) :
                        mouse.click(button='left', coords = (eachBldPos.iloc[i].x, eachBldPos.iloc[i].y))
                        sleep(0.5)
                    sleep(4)
                    bldName = str(bldList[count])
                    self.wholeSignal.emit(bldName + " 시작")
                    self.updateStatusSignal.emit("".join(['(', str(count+1), '/', str(totalLength), ')', " ", bldName]))
                    self.changeBldName(bldName)
                    self.unitCap.run()

                    if self.status['isRunning'] : 
                        self.wholeSignal.emit(bldName + " 종료")
                        count += 1
                        self.windows['ab'].set_focus()
                        for i in range(howManyClicks) : 
                            mouse.click(button='left', coords = (34, 1018))
                            sleep(0.5)
                        sleep(0.5)
                    
            if self.status['isRunning'] : 
                self.wholeSignal.emit("모든 캡처가 끝났습니다. " + returnCurrentTime())

        elif self.captureOptions['isSingle'] :
            optionWithInfo = addInfoOfOption(self.req['option'], self.req['startDate'], self.req['endDate'])
            dummyTagName = "".join(randomSample(ascii_letters, 10))
            dummyFolderName = self.wholeFolderName + '/' + dummyTagName
            createFolder(dummyFolderName)

            self.wholeSignal.emit("캡처를 시작합니다. " + returnCurrentTime())
            totalLength = len(optionWithInfo)
            keyList = list(optionWithInfo.keys())
            count = 0
            while self.status['isRunning'] and count < totalLength:
                if self.status['isPaused']:
                    pass
                else:
                    self.windows['ab'].set_focus()
                    keyboard.send_keys('{F2 3}')
                    #self.windows['ab'].type_keys('{F2 3}')
                    sleep(0.1)
                    keyboard.send_keys('{VK_SUBTRACT ' + str(optionWithInfo[keyList[count]][0]) + '}')
                    #self.windows['ab'].type_keys('{VK_SUBTRACT ' + str(optionWithInfo[keyList[count]][0]) + '}')
                    sleep(0.2)

                    with mss.mss() as sct:
                        captureSave(keyList[count], dummyFolderName, self.req['endDate'],
                                    optionWithInfo[keyList[count]][1], sct, self.req['fileNamePrefix'], self.status, self.windows,
                                    self.captureOptions['isSimple'])
                    count += 1

            if self.req['bldName'] :
                rename(dummyFolderName, self.wholeFolderName + "/" + self.req['bldName'])

            self.wholeSignal.emit("캡처가 모두 끝났습니다. " + returnCurrentTime())
            self.windows['pr'].set_focus()

        
        else :
            while self.status['isRunning'] :
                if self.status['isPaused'] :
                    pass
                else :
                    self.unitCap.run()
                    break
    
        if self.status['isRunning'] : 
            self.finishedSignal.emit()


class Ui_MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.status = {'isRunning':False, 'isPaused':False}
        today = date.today()

        self.resize(459, 625)
        self.centralwidget = QtWidgets.QWidget()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.title = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.verticalLayout_2.addWidget(self.title)
        self.cautionRow = QtWidgets.QHBoxLayout()
        self.cautionSet = QtWidgets.QVBoxLayout()
        self.cautionTitle = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("맑은 고딕")
        font.setPointSize(10)
        self.cautionTitle.setFont(font)
        self.cautionSet.addWidget(self.cautionTitle)
        self.cautionContent = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cautionContent.sizePolicy().hasHeightForWidth())
        self.cautionContent.setSizePolicy(sizePolicy)
        self.cautionContent.setFont(font)
        self.cautionSet.addWidget(self.cautionContent)
        self.cautionRow.addLayout(self.cautionSet)
        self.verticalLayout_2.addLayout(self.cautionRow)
        self.inputRow = QtWidgets.QHBoxLayout()
        self.smallInputRow = QtWidgets.QHBoxLayout()
        self.verticalInputRow = QtWidgets.QVBoxLayout()
        self.horizontalInputRow = QtWidgets.QHBoxLayout()
        self.checkIfWhole = QtWidgets.QCheckBox(self.centralwidget)
        self.checkIfWhole.setFont(font)
        self.checkIfWhole.toggled.connect(self.checkWholeFunc)
        self.horizontalInputRow.addWidget(self.checkIfWhole)
        self.checkIfSingle = QtWidgets.QCheckBox(self.centralwidget)
        self.checkIfSingle.setFont(font)
        self.checkIfSingle.toggled.connect(self.checkSingleFunc)
        self.horizontalInputRow.addWidget(self.checkIfSingle)
        self.verticalInputRow.addLayout(self.horizontalInputRow)

        self.bldNameTitle = QtWidgets.QLabel(self.centralwidget)
        self.bldNameTitle.setFont(font)
        self.bldNameTitle.setAlignment(QtCore.Qt.AlignCenter)
        self.smallInputRow.addWidget(self.bldNameTitle)
        self.bldNameInput = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bldNameInput.sizePolicy().hasHeightForWidth())
        self.bldNameInput.setSizePolicy(sizePolicy)
        self.bldNameInput.setFont(font)
        self.smallInputRow.addWidget(self.bldNameInput)
        self.verticalInputRow.addLayout(self.smallInputRow)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.inputRow.addLayout(self.verticalInputRow)
        self.inputRow.addItem(spacerItem)
        self.dateSet = QtWidgets.QGridLayout()
        self.startTitle = QtWidgets.QLabel(self.centralwidget)
        self.startTitle.setFont(font)
        self.dateSet.addWidget(self.startTitle, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.startDate = QtWidgets.QDateEdit(self.centralwidget)
        self.startDate.setFont(font)
        self.startDate.setAlignment(QtCore.Qt.AlignCenter)
        self.startDate.setDate(QtCore.QDate(today.year, today.month, 1))
        self.startDate.setMaximumDate(QtCore.QDate(today))
        self.startDate.setCalendarPopup(True)
        self.dateSet.addWidget(self.startDate, 2, 0, 1, 1)
        self.endDate = QtWidgets.QDateEdit(self.centralwidget)
        self.endDate.setFont(font)
        self.endDate.setAlignment(QtCore.Qt.AlignCenter)
        self.endDate.setCalendarPopup(True)
        self.endDate.setDate(QtCore.QDate(today))
        self.dateSet.addWidget(self.endDate, 2, 1, 1, 1)
        self.endTitle = QtWidgets.QLabel(self.centralwidget)
        self.endTitle.setFont(font)
        self.dateSet.addWidget(self.endTitle, 0, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.inputRow.addLayout(self.dateSet)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.inputRow.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.inputRow)
        self.optionRow = QtWidgets.QHBoxLayout()
        self.checks = QtWidgets.QGroupBox(self.centralwidget)
        self.checks.setFont(font)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.checks)
        self.checksSet = QtWidgets.QVBoxLayout()
        self.hourlyCheck = QtWidgets.QCheckBox(self.checks)
        self.hourlyCheck.setFont(font)
        self.hourlyCheck.setChecked(True)
        self.checksSet.addWidget(self.hourlyCheck)
        self.dailyCheck = QtWidgets.QCheckBox(self.checks)
        self.dailyCheck.setFont(font)
        self.checksSet.addWidget(self.dailyCheck)
        self.monthlyCheck = QtWidgets.QCheckBox(self.checks)
        self.monthlyCheck.setFont(font)
        self.checksSet.addWidget(self.monthlyCheck)
        self.horizontalLayout_2.addLayout(self.checksSet)
        self.optionRow.addWidget(self.checks)
        self.optionRight = QtWidgets.QVBoxLayout()
        self.fileNameOptions = QtWidgets.QGroupBox(self.centralwidget)
        self.fileNameOptions.setFont(font)
        self.verticalLayoutInBox = QtWidgets.QVBoxLayout(self.fileNameOptions)
        self.checkIfSimple = QtWidgets.QCheckBox(self.fileNameOptions)
        self.checkIfSimple.setFont(font)
        self.fileNameSet = QtWidgets.QHBoxLayout()
        self.dateOnly = QtWidgets.QRadioButton(self.fileNameOptions)
        self.dateOnly.setChecked(False)
        self.fileNameSet.addWidget(self.dateOnly)
        self.underscore = QtWidgets.QRadioButton(self.fileNameOptions)
        self.underscore.setChecked(True)
        self.fileNameSet.addWidget(self.underscore)
        self.bld = QtWidgets.QRadioButton(self.fileNameOptions)
        self.fileNameSet.addWidget(self.bld)
        self.verticalLayoutInBox.addWidget(self.checkIfSimple)
        self.verticalLayoutInBox.addLayout(self.fileNameSet)
        self.optionRight.addWidget(self.fileNameOptions)
        self.startAbortRow = QtWidgets.QHBoxLayout()
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.startAbortRow.addItem(spacerItem2)
        self.startCapture = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startCapture.sizePolicy().hasHeightForWidth())
        self.startCapture.setSizePolicy(sizePolicy)
        self.startCapture.setFont(font)
        self.startAbortRow.addWidget(self.startCapture)
        self.abortCapture = QtWidgets.QPushButton(self.centralwidget)
        self.abortCapture.setSizePolicy(sizePolicy)
        self.abortCapture.setFont(font)
        self.abortCapture.setDisabled(True)
        self.pauseCapture = QtWidgets.QPushButton(self.centralwidget)
        self.pauseCapture.setSizePolicy(sizePolicy)
        self.pauseCapture.setFont(font)
        self.pauseCapture.setDisabled(True)
        self.startAbortRow.addWidget(self.pauseCapture)
        self.startAbortRow.addWidget(self.abortCapture)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.startAbortRow.addItem(spacerItem3)
        self.optionRight.addLayout(self.startAbortRow)
        self.optionRow.addLayout(self.optionRight)
        self.verticalLayout_2.addLayout(self.optionRow)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem4)
        self.statusTitle = QtWidgets.QLabel(self.centralwidget)
        self.statusTitle.setFont(font)
        self.verticalLayout_2.addWidget(self.statusTitle)
        self.statusTextBox = QtWidgets.QTextBrowser(self.centralwidget)
        self.statusTextBox.setFont(font)
        self.verticalLayout_2.addWidget(self.statusTextBox)
        self.horizontalButtonRow = QtWidgets.QHBoxLayout()
        self.saveLog = QtWidgets.QPushButton(self.centralwidget)
        self.saveLog.setFont(font)
        self.saveLog.setDisabled(True)
        #self.saveLog.setDisabled(True)
        self.horizontalButtonRow.addWidget(self.saveLog)
        self.clearLog = QtWidgets.QPushButton(self.centralwidget)
        self.clearLog.setFont(font)
        self.clearLog.setDisabled(True)
        self.horizontalButtonRow.addWidget(self.clearLog)
        self.exitProgram = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exitProgram.sizePolicy().hasHeightForWidth())
        self.exitProgram.setSizePolicy(sizePolicy)
        self.exitProgram.setFont(font)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalButtonRow.addItem(spacerItem5)
        self.horizontalButtonRow.addWidget(self.exitProgram)
        self.verticalLayout_2.addLayout(self.horizontalButtonRow)


        self.statusBar = QtWidgets.QStatusBar(self)
        font.setPointSize(9)
        self.statusBar.setFont(font)
        self.setStatusBar(self.statusBar)
        self.statusBarMessage = "준비"
        self.setCentralWidget(self.centralwidget)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("AutoBase Image Capturer (v 1.6.1) - 2019/3/18")
        self.title.setText("AutoBase Image Capturer (ver 1.6.1)")
        self.cautionTitle.setText("주의사항")
        self.cautionContent.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'맑은 고딕\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1. 프로그램이 실행되는 동안 다른 작업을 수행할 경우 캡처가 제대로 되지 않습니다.</p>\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">2. 듀얼모니터의 경우 1번 모니터(작업표시줄이 있는 모니터)에 오토베이스 프로그램을 두어야 합니다.</p></body></html>")
        self.checkIfWhole.setText("캠퍼스 전체")
        self.checkIfSingle.setText("단일 태그")
        self.bldNameTitle.setText("건물명")
        self.startTitle.setText("시작일자")
        self.endTitle.setText("종료일자")
        self.checks.setTitle("캡처 옵션")
        self.hourlyCheck.setText("시간 단위")
        self.dailyCheck.setText("일 단위")
        self.monthlyCheck.setText("월 단위")
        self.fileNameOptions.setTitle("파일 이름 옵션")
        self.checkIfSimple.setText("태그 하위 폴더 미생성")
        self.dateOnly.setText("날짜만")
        self.underscore.setText("_만 추가")
        self.bld.setText("건물 정보 추가")
        self.startCapture.setText("캡처 시작")
        self.pauseCapture.setText("일시중지")
        self.abortCapture.setText("캡처 중단")
        self.statusTitle.setText("진행 상황")
        self.saveLog.setText("로그 저장")
        self.clearLog.setText("로그 지우기")
        self.exitProgram.setText("프로그램 종료")
        self.statusBar.showMessage(self.statusBarMessage)

        self.startCapture.clicked.connect(self.captureStart)
        self.abortCapture.clicked.connect(self.abortCaptureFunc)
        self.pauseCapture.clicked.connect(self.pauseCaptureFunc)
        self.saveLog.clicked.connect(self.saveLogFunc)
        self.clearLog.clicked.connect(self.clearLogFunc)
        self.exitProgram.clicked.connect(self.closeWindow)

    def setPrerequisites(self) :
        # 1) setting timescale option
        self.option = []

        if self.hourlyCheck.isChecked():
            self.option.append('d')
        if self.dailyCheck.isChecked():
            self.option.append('m')
        if self.monthlyCheck.isChecked():
            self.option.append('y')

        # 2) setting periods
        self.startDate_dateModule = date(self.startDate.date().year(), self.startDate.date().month(), self.startDate.date().day())
        self.endDate_dateModule = date(self.endDate.date().year(), self.endDate.date().month(), self.endDate.date().day())

        # 3) getting building name
        if self.checkIfWhole.isChecked() : 
            self.bldName = "wholeBld"
        else : 
            self.bldName = self.bldNameInput.text().strip()

        # 4) setting file name option
        if self.dateOnly.isChecked() :
            self.fileNamePrefix = ""
        elif self.underscore.isChecked():
            self.fileNamePrefix = "_"
        else :
            self.fileNamePrefix = self.bldName + '_'

        return {'option' : self.option, 'startDate' : self.startDate_dateModule, 'endDate' : self.endDate_dateModule, 'bldName' : self.bldName, 'fileNamePrefix' : self.fileNamePrefix}

    def captureStart(self):

        self.programWin = windowWrapper(".*AutoBase Image Capturer.*")

        if isdir(self.bldNameInput.text()) : 
            QtWidgets.QMessageBox.warning(self.centralwidget, "폴더 중복", \
            '입력하신 건물명과 동일한 이름의 폴더가 있습니다. 중복되지 않는 건물명을 입력해 주세요.', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok )
            return
        try : 
            self.autobaseWin = windowWrapper('.*Web View.*')
        except WindowNotFoundError :
            QtWidgets.QMessageBox.warning(self.centralwidget, "화면 확인", \
             "오토베이스 화면이 없습니다. 오토베이스를 먼저 실행해 주세요.", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return
        #checking whether capture options are checked
        checkTest = [self.hourlyCheck.isChecked(), self.dailyCheck.isChecked(), self.monthlyCheck.isChecked()]
        howManyChecked = len([x for x in checkTest if x == True])
        if howManyChecked == 0 :
            QtWidgets.QMessageBox.warning(self.centralwidget, '캡처 옵션 오류', \
                                          '캡처 옵션을 한 개 이상 선택해 주세요.', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
            return
        elif howManyChecked >1 :
            if self.checkIfSingle.isChecked() :
                QtWidgets.QMessageBox.warning(self.centralwidget, '캡처 옵션 오류', \
                                          '단일 태그 캡처 시 하나의 캡처 옵션만 선택해야 합니다.', QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
            elif self.checkIfSimple.isChecked() :
                QtWidgets.QMessageBox.warning(self.centralwidget, '폴더 옵션 오류', \
                                              "태그 폴더 내 하위 폴더 미생성시 하나의 캡처 옵션만 선택해야 합니다.", QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Ok)
                return
        if not self.checkIfWhole.isChecked() and self.bld.isChecked() and self.bldNameInput.text().strip() == "" : 
            QtWidgets.QMessageBox.warning(self.centralwidget, "캡처 옵션 오류", \
            "건물명이 입력되어 있지 않은 상태에서 건물 명 추가 옵션이 선택되어 있습니다.", QtWidgets.QMessageBox.Ok)
            return

        self.req = self.setPrerequisites()

        go = QtWidgets.QMessageBox.question(self.centralwidget, "캡처 실행", \
        '입력한 조건대로 캡처를 시작할까요?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

        if go == QtWidgets.QMessageBox.Yes :
            pass
        else : 
            return

        bldPosTable = None

        if self.checkIfWhole.isChecked() : 
            try : 
                bldPosTable = read_excel("bldPosList.xlsx", encoding = sys.getfilesystemencoding())
            except FileNotFoundError : 
                QtWidgets.QMessageBox.warning(self.centralwidget, "건물 위치 오류", "건물 위치 파일이 필요합니다", QtWidgets.QMessageBox.Ok)
                name, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "open", filter = "Excel file (*.xlsx *.xls)", options=QtWidgets.QFileDialog.DontUseNativeDialog)
                if name : 
                    # try :
                    #     name.encode("ascii")
                    # except UnicodeEncodeError :
                    #     QtWidgets.QMessageBox.warning(self.centralwidget, "파일 경로 오류", "파일 경로 또는 파일 이름에 한글이 포함되어 있으면 파일을 열 수 없습니다.", QtWidgets.QMessageBox.Ok)
                    #     return
                    bldPosTable = read_excel(name, encoding = sys.getfilesystemencoding())
                    if bldPosTable.shape[1] != 3 :
                        QtWidgets.QMessageBox.warning(self.centralwidget, "파일 형식 오류", "지원하지 않는 형식의 파일입니다.", QtWidgets.QMessageBox.Ok)
                        return
                    else : 
                        self.autobaseWin.set_focus()
                else : 
                    QtWidgets.QMessageBox.warning(self.centralwidget, "파일 오류", "잘못된 파일이거나 파일이 선택되지 않았습니다.", QtWidgets.QMessageBox.Ok)
                    return
        
        self.autobaseWin.set_focus()
        self.startCapture.setDisabled(True)
        self.pauseCapture.setEnabled(True)
        self.abortCapture.setEnabled(True)

        self.windows = {'ab' : self.autobaseWin, 'pr':self.programWin}
        self.bldPosTable = bldPosTable

        self.captureOptions = {'isWhole' : self.checkIfWhole.isChecked(), 'isSingle':self.checkIfSingle.isChecked(), 'isSimple' : self.checkIfSimple.isChecked()}
        self.wholeCap = WholeCaptureThread(self.req, self.captureOptions, self.status, self.bldPosTable, self.windows)
        self.wholeCap.wholeSignal.connect(self.updateText)
        self.wholeCap.updateStatusSignal.connect(self.updateStatusBar)
        self.wholeCap.finishedSignal.connect(self.finishedWell)

        self.unitCap = CaptureFunc(self.req, self.captureOptions['isSimple'], self.wholeCap.wholeFolderName, self.status, self.windows)
        self.unitCap.statusSig.connect(self.updateText)

        self.wholeCap.obtainUnitCaptureClass(self.unitCap)
        self.status['isRunning'] = True
        self.changeStatusMessage('실행중...')
        self.wholeCap.start()

        ## for log file ##
        whatToCap = "캡처 대상 : "
        if self.checkIfWhole.isChecked() : 
            whatToCap += "캠퍼스 전체"
        elif self.checkIfSingle.isChecked() : 
            whatToCap += "단일 태그"
        else : 
            whatToCap += "단일 건물"
        self.statusTextBox.append(whatToCap)

        howOften = "캡처 범위 : "
        if 'd' in self.req['option'] : 
            howOften += "시간 단위 (Y) "
        else : 
            howOften += "시간 단위 (N) "
        
        if 'm' in self.req['option'] : 
            howOften += "일 단위 (Y) "
        else : 
            howOften += "일 단위 (N) "
        
        if 'y' in self.req['option'] : 
            howOften += "월 단위 (Y)"
        else : 
            howOften += "월 단위 (N)"
        self.statusTextBox.append(howOften)

        if self.checkIfSimple.isChecked() : 
            self.statusTextBox.append("하위 폴더 생성 여부 : N")
        else : 
            self.statusTextBox.append("하위 폴더 생성 여부 : Y")

        prefix = "파일 이름 옵션 : "
        if self.dateOnly.isChecked() :
            prefix += "날짜만"
        elif self.underscore.isChecked():
            prefix += "_만 추가"
        else :
            prefix += "건물 정보 추가"
        self.statusTextBox.append(prefix)

        self.statusTextBox.append("".join(["캡처 기간 : ", self.startDate_dateModule.strftime("%Y/%m/%d"), " ~ ", self.endDate_dateModule.strftime("%Y/%m/%d")]))


    def checkWholeFunc(self) : 
        if self.checkIfWhole.isChecked() : 
            self.bldNameInput.setDisabled(True)
            self.checkIfSingle.setDisabled(True)
            self.statusBar.showMessage("전체 선택")
        else : 
            self.bldNameInput.setEnabled(True)
            self.checkIfSingle.setEnabled(True)
            self.statusBar.showMessage(self.statusBarMessage)

    def checkSingleFunc(self):
        if self.checkIfSingle.isChecked() :
            self.checkIfWhole.setDisabled(True)
            self.bldNameTitle.setText("태그명")
            self.statusBar.showMessage("단일 태그 선택")

        else :
            self.checkIfWhole.setEnabled(True)
            self.bldNameTitle.setText("건물명")
            self.statusBar.showMessage(self.statusBarMessage)

    def closeWindow(self):
        sys.exit()

    def finishedWell(self) : 
        self.status['isRunning'] = False
        self.startCapture.setEnabled(True)
        self.pauseCapture.setDisabled(True)
        self.abortCapture.setDisabled(True)
        self.changeStatusMessage("준비")
        if self.statusTextBox.toPlainText() :
            self.saveLog.setEnabled(True)
            self.clearLog.setEnabled(True)
        if self.checkIfWhole : 
            self.bldNameInput.clear()
        
    def pauseCaptureFunc(self):
        if self.status['isPaused'] :
            self.autobaseWin.set_focus()
            self.pauseCapture.setText("일시중지")
            self.status['isPaused'] = False
            self.statusBar.showMessage(self.statusBarMessage)
            if self.statusTextBox.toPlainText() :
                self.saveLog.setEnabled(True)
                self.clearLog.setEnabled(True)
        else :
            self.status['isPaused'] = True
            self.pauseCapture.setText("다시 시작")
            self.statusBar.showMessage("일시중지")
            self.saveLog.setDisabled(True)
            self.clearLog.setDisabled(True)

    def abortCaptureFunc(self):
        self.status['isRunning'] = False
        self.status['isPaused'] = False
        self.startCapture.setEnabled(True)
        self.pauseCapture.setDisabled(True)
        self.abortCapture.setDisabled(True)
        self.changeStatusMessage("준비")
        if self.statusTextBox.toPlainText():
            self.saveLog.setEnabled(True)
            self.clearLog.setEnabled(True)

        if self.checkIfWhole : 
            self.bldNameInput.clear()

    @QtCore.pyqtSlot(str)
    def updateText(self, text) : 
        self.statusTextBox.append(text)

    @QtCore.pyqtSlot(str)
    def updateStatusBar(self, content) : 
        self.changeStatusMessage(content)
        
    def changeStatusMessage(self, text) : 
        self.statusBarMessage = text
        self.statusBar.showMessage(self.statusBarMessage)

    def saveLogFunc(self):
        name, _ = QtWidgets.QFileDialog.getSaveFileName(self.centralwidget, '로그 저장', filter = 'text file (*.txt)', options=QtWidgets.QFileDialog.DontUseNativeDialog)
        if name :
            with open(name+'.txt', 'w') as f :
                f.write(self.statusTextBox.toPlainText())

    def clearLogFunc(self):
        go = QtWidgets.QMessageBox.warning(self.centralwidget, "로그 삭제", "화면 상의 모든 로그가 삭제됩니다.", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if go == QtWidgets.QMessageBox.Yes :
            self.statusTextBox.clear()
            self.clearLog.setDisabled(True)
            self.saveLog.setDisabled(True)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    
    ui.show()
    sys.exit(app.exec_())

