
import random
import sys
import typing
from PyQt6.QtGui import QIcon, QFont, QPixmap, QMovie, QRegion
from PyQt6 import QtCore
from PyQt6.QtWidgets import QApplication ,QListWidget , QMainWindow , QLabel,  QVBoxLayout, QGridLayout, QWidget, QLineEdit, QPushButton, QMessageBox

f = open("periodictable.csv")
tabl = f.read()
tabl = tabl.splitlines()
class Window(QMainWindow):
    def __init__(self) :
        super(Window,self).__init__()
        self.centralwidget =QWidget(self)

        self.bat = QPushButton(self)
        
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 0, 700,1000))
        self.pixmap = QPixmap("Tabliza_Mendeleeva.jpg")
        self.label.setPixmap(self.pixmap)
        
        self.rull = QLineEdit(self)
        self.rull.move(250,500)

        self.bat.setText("Информация")
        self.bat.clicked.connect(self.prow)
        self.otvet = QLabel(self)
        self.vvod= self.rull.text()
        self.bat.move(150,500)
        self.otvet.setGeometry(QtCore.QRect(0, 500, 210, 210))
    def prow(self):
        self.vvod= self.rull.text()
        for k in tabl:
          if k.split(",")[1] == self.vvod:
             k=k.split(",")
             self.otvet.setText(f"Atomic Number:{k[0]}\n Symbol:{k[1]}\n Element:{k[2]}\n Original of name:{k[3]}\n Group:{k[4]}\n period:{k[5]}\n Atomic weight:{k[6]}  u\n Density:{k[7]}  g/cm*3\n Melting point:{k[8]} K\n Boiling point:{k[9]} K\n specific head capacity:{k[10]}  J/(g*k)\n Electronegativity:{k[11]}\n Abundance in earth's crust:{k[12]}  mg/kg")
   

def applic():
        app = QApplication(sys.argv)
        window = Window()

        window.show()
        sys.exit(app.exec())
if __name__ == "__main__":
    applic()