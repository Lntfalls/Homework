import random
import sys
from PyQt6.QtCore import QSize, Qt 
from PyQt6.QtWidgets import QApplication,QListWidget , QMainWindow , QLabel,  QVBoxLayout, QGridLayout, QWidget, QLineEdit, QPushButton, QMessageBox

class Window(QMainWindow):
        def __init__(self):    
            super().__init__()
            self.setFixedSize(QSize(250,600))
             
            self.setWindowTitle("Вероятность выпадения чисел")
            
            but1=QPushButton(self)
            but1.setText("Рассчитать вероятность для всех чисел")
            but1.setFixedSize(250,25)
            but1.move(0,0)
            but1.setCheckable(True)
            
            but1.clicked.connect(self.the_button_was_toggled)
            
            cubic_info=QLineEdit(self)
            cubic_info.setText("Колличество кубиков")
            cubic_info.setFixedSize(125,25)
            cubic_info.move(125,23)
            cubic_info.setDisabled(True)

            self.cubic=QLineEdit(self)
            self.cubic.setText("3")
            self.cubic.move(0,23)
            self.cubic.setFixedSize(125,25)

            broski_info=QPushButton(self)
            broski_info.setText("Колличество бросков")
            broski_info.setFixedSize(125,25)
            broski_info.move(125,46)
            broski_info.setDisabled(True)
            
            self.broski=QLineEdit(self)
            self.broski.setText("100")
            self.broski.move(0,46)
            self.broski.setFixedSize(125,25)
            
            self.rez = QListWidget(self)
            self.rez.addItems(["Результат:"])
            self.rez.move(0,70)
            self.rez.setFixedSize(250,530)

        
        def the_button_was_toggled(self):
            
            self.rez.clear()  
            self.rez.addItems(["Результат:"])
            cube=int(self.cubic.text())
            bros=int(self.broski.text())
            
            self.chisla=[]
            for n in range(bros):
                count=0
                for h in range(cube):
                    x=random.randint(1,6)
                    count+=x
                self.chisla.append(count)

            chis = cube - 1

            for n in range(cube - 1, 6 * cube):
                chis += 1
                a = self.chisla.count(chis)
                rezult = str(chis) + "=" + str(float(a / len(self.chisla) * 100)) + "%"
                self.rez.addItem(str(rezult))



        

app = QApplication(sys.argv)

window=Window()
window.show()

app.exec()