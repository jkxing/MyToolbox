from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import cv2
def run(parent, filelists):
	size, ok = QInputDialog.getText(parent, 'Input Dialog', 
        'Enter new suffix:')
	w,h = [int(s) for s in size.split("x")]
	for file in filelists:
		img = cv2.imread(file)
		img = cv2.resize(img,(w,h))
		cv2.imwrite(file,img)
	pass
