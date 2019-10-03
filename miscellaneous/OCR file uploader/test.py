from pywinauto.findwindows import find_windows as fw
from pywinauto.application import Application as App
from time import sleep

windowName = "오토베이스_OCR"

app = App()
pos = fw(title = windowName)
print(pos)

window = app.connect(handle = pos[0])
window = app.window(handle = pos[0])
window.click_input(coords=(155,660))

while True : 
    pos2 = fw(title=windowName)
    print(pos2)
    sleep(2)

