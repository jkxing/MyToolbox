from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os

def run(parent, filelists):
    text, ok = QInputDialog.getText(parent, 'Input Dialog', 
        'Enter new suffix:')
    for item in filelists:
        os.rename(item,item+"."+text)