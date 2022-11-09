import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import os
from widgets.reformat import *
    
class window(QWidget):
    def __init__(self, parent = None):
        super(window, self).__init__(parent)
        self.resolution = 512
        self.half_res = self.resolution/2
        self.resize(self.resolution,self.resolution)
        self.setWindowTitle("MyToolbox")
        #self.label = QLabel(self)
        #self.label.setText("Hello World")
        #font = QFont()
        #font.setFamily("Arial")
        #font.setPointSize(16)
        #self.label.setFont(font)
        #self.label.move(50,80)
        self.setAcceptDrops(True)

        self.mPixmap = QPixmap()
        self.mModified = True
        self.currentPos = [self.half_res,self.half_res]
        self.update()

        self.setToolTip('Drag files here!')

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        #self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.filelists = []
        self.contextMenu = None
        self.initMenu()
        self.initUI()
    
    def initUI(self):
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)     
        
        qbtn = QPushButton('Reload', self)
        qbtn.clicked.connect(lambda: self.initMenu())
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(200, 50)

        qbtn = QPushButton('Add', self)
        qbtn.clicked.connect(lambda: self.newOp())
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(350, 50)

    def newOp(self):
        text, ok = QInputDialog.getText(self, 'NewOp', 
        'Enter Op Name:')
        with open(f"widgets/{text}.py","w") as f:
            f.write("from PyQt5.QtCore import *\nfrom PyQt5.QtGui import *\nfrom PyQt5.QtWidgets import *\ndef run(parent, filelists):\n\tpass\n")
        #os.chdir(".")
        os.startfile(os.path.normpath(f"widgets/{text}.py"))
        self.initMenu()

    def load_module(self, pluginName):
        plugin=__import__("widgets."+pluginName, fromlist=[pluginName])
        return plugin
    
    def initMenu(self):
        self.contextMenu = QMenu(self) 
        for filename in os.listdir("widgets"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            pluginName=os.path.splitext(filename)[0]
            plugin = self.load_module(pluginName)
            action  = QAction('&'+pluginName, self)
            action.triggered.connect(lambda: self.action(plugin.run))
            self.contextMenu.addAction(action)
            
    def paintEvent(self, event):
        if self.mModified:
            pixmap = QPixmap(self.size())
            pixmap.fill(Qt.white)
            painter = QPainter(pixmap)
            self.drawEye(painter, self.currentPos)
            self.mPixmap = pixmap
            self.mModified = False

        qp = QPainter(self)
        qp.drawPixmap(0, 0, self.mPixmap)
    
    
    def drawCircle(self,qp,center,rad):
        qp.drawEllipse(center[0]-rad, center[1]-rad,rad*2, rad*2)

    def drawEye(self, qp, pos):
        pen = QPen(Qt.black, 20, Qt.SolidLine)
        qp.setPen(pen)
        left_center = [self.resolution*0.35,self.half_res]
        right_center = [self.resolution*0.65,self.half_res]
        radius = self.resolution * 0.1
        self.drawCircle(qp,left_center,radius)
        self.drawCircle(qp,right_center,radius)
        x = (pos[0]-self.half_res)/self.half_res#[-1,1]
        y = (pos[1]-self.half_res)/self.half_res#[-1,1]
        left_center[0] = left_center[0]+radius*0.85*x
        left_center[1] = left_center[1]+radius*0.85*y
        right_center[0] = right_center[0]+radius*0.85*x
        right_center[1] = right_center[1]+radius*0.85*y
        brush = QBrush(Qt.SolidPattern)
        qp.setBrush(brush)
        self.drawCircle(qp,left_center,radius*0.1)
        self.drawCircle(qp,right_center,radius*0.1)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        self.mModified = True
        self.currentPos = [event.pos().x(),event.pos().y()]
        self.update()

    def dragLeaveEvent(self, event):
        self.mModified = True
        self.currentPos = [self.half_res,self.half_res]
        self.update()

    def dropEvent(self, event):
        self.filelists = [u.toLocalFile() for u in event.mimeData().urls()]
        self.contextMenu.exec_(self.mapToGlobal(event.pos()))
    
    def action(self, func):
        func(self, self.filelists)
        self.mModified = True
        self.currentPos = [self.half_res,self.half_res]
        self.update()
    
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore() 
    
def main():
   app = QApplication(sys.argv)
   ex = window()
   ex.show()
   sys.exit(app.exec_())
if __name__ == '__main__':
   main()