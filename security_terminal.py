import sys
import sqlite3
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QRadioButton, QMessageBox
import time

employees = 20
guests = 5

curr = [("Алексеев","Илья","Алексеевич","23-Apr-1994","директор по информатизации","+79993456785","aleksee45@mail.ru","NULL","NULL"),
("Аржанов","Владислав","Александрович","27-Jan-1995","начальние отдела кадров","+79063194556","arhjanov12@yandex.ru","NULL","NULL"),
("Белоцерковец ","Дмитрий","Александрович","12-Sep-1983","менеджер","+79773332123","belotserkovets@gmail.com","NULL","NULL"),
("Богушев","Арсений","Александрович","09-Dec-1973","директор","+79264444334","Bogushev@mail.ru","NULL","NULL"),
("Гундарова","Софья","Анатольевна","30-Nov-1995","менеджер","+79256789012","Gundarova@yandex.ru","NULL","NULL"),
("Долженков","Борис","Алексеевич","23-Jun-2002","курьер","+79003196748","Dolzhenkov@gmail.com","NULL","NULL"),
("Журавова","Ангелина","Сергеевна","17-Aug-2002","специалист по корреспонденции","+79836571245","Zhuravova@gmail.com","NULL","NULL"),
("Клевцова","Варвара","Андреевна","15-Oct-2002","секретарь","+79023672156","Klevtsova@gmail.com","NULL","NULL"),
("Коваленко","Вероника","Александровна","17-Jul-1997","менеджер","+79271285522","Kovalenko@gmail.com","NULL","NULL"),
("Королев","Платон","Валеорьевич","13-Mar-1993","главный бухгалтер","+79773045689","Korolev@gmail.com","NULL","NULL"),
("Кубышкин","Роман","Евгеньевич","10-Oct-1985","менеджер по технологии","+79013219045","Kubyshkin@gmail.com","NULL","NULL"),
("Макаренко","Константин","Викторович","11-Nov-1984","бизнес аналитик","+79992341289","Makarenko@gmail.com","NULL","NULL"),
("Мартиросов","Артемий","Артурович","01-Feb-1974","smm - менеджер","+79027893459","Martirosov@gmail.com","NULL","NULL"),
("Мелкумян","Роберт","Робертович","16-May-1993","маркетолог","+79982341290","Melkumyan@gmail.com","NULL","NULL"),
("Олейник","Ольга","Викторовна","18-Jun-1993","руководитель проекта","+79762349987","Oleinik@gmail.com","NULL","NULL"),
("Полюцкий","Александр","Сергеевич","19-Jan-1981","юрист-консультант","+79673421894","Polyutsky@gmail.com","NULL","NULL"),
("Рустамов","Иброхим","Рустамович","29-Oct-1982","зав.хозяйством","+79231782392","Rustamov@gmail.com","NULL","NULL"),
("Рябцева","Алена","Александровна","14-Nov-1982","бухгалтер","+79321743981","Ryabtseva@gmail.com","NULL","NULL"),
("Саберова","Динара","Равилевна","28-Dec-1994","главный юрист","+79992341084","Saberova@gmail.com","NULL","NULL"),
("Сафонова","Ирина","Ивановна","15-Jul-1983","делопроизводитель","+79253419861","Safonov@gmail.com","NULL","NULL"),
("Стронина","София","Евгеньевна","31-Mar-2002","секретарь","+79162381629","Stronina@gmail.com","NULL","NULL"),
("Тарасов","Степан","Павлович","06-Jun-1996","менеджер","+79152371823","Тарасов@gmail.com","NULL","NULL"),
("Чекменёв","Кирилл","Андреевич","02-Aug-1998","дизайнер","+79172361959","Chekmenev@gmail.com","NULL","NULL"),
("Чернов","Максим","Дмитриевич","23-Dec-1999","аналитик","+79293652732","Chernov@gmail.com","NULL","NULL"),
("Шарофидинова","Ирода","Отабек","21-Mar-1991","уборщица","+79002893276","Sharofidinov@gmail.com","NULL","NULL"),
("Шундрик","Егор","Максимович","07-Apr-1992","расчетчик","+79281123119","Shundrick@gmail.com","NULL","NULL"),
("Шушняев","Никита","Максимовна","09-Sep-1991","сметчик","+79031732861","Shushnyaev@gmail.com","NULL","NULL")]

local = time.ctime(time.time())

with sqlite3.connect("employees.db") as base:
    sql = base.cursor()
    sql.execute('DROP TABLE IF EXISTS employees')
    sql.execute("""CREATE TABLE IF NOT EXISTS employees(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        birth TEXT,
        job TEXT,
        phone TEXT,
        email TEXT,
        enter TEXT ,
        exit TEXT 
        );
        """)
    sql.executemany("INSERT INTO employees VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)", curr)
base.commit()

with sqlite3.connect("guests.db") as base2:
    sql2 = base2.cursor()
    sql2.execute('DROP TABLE IF EXISTS guests')
    sql2.execute("""CREATE TABLE IF NOT EXISTS guests(
        firstname TEXT,
        name TEXT,
        lastname TEXT,
        birth TEXT,
        target TEXT,
        phone TEXT,
        email TEXT,
        enter INt,
        exit INT 
        );
        """)
base2.commit()

class PassControlApp(QWidget):
    def __init__(self):
        super().__init__()
        global sql
        global base
        global employees
        global guests
        self.sql = 0
        self.car = 0
        
        self.RadioButton = QRadioButton("Парковка")

        self.issue_pass_button2 = QPushButton('Войти как гость')
        self.issue_pass_button = QPushButton('Вход')
        self.issue_pass_button3 = QPushButton('Выход')
      
        self.issue_pass_button.clicked.connect(self.ENTRY)
        self.issue_pass_button3.clicked.connect(self.EXIT)
        self.issue_pass_button2.clicked.connect(self.GUEST_ENTRY)
        
        self.RadioButton.toggled.connect(self.UPDATE)

        self.mail = QLineEdit(self,placeholderText="Электронная почта")
        
        self.passv = QLineEdit(self,placeholderText="Имя")

        layout = QVBoxLayout()
        layout.addWidget(self.mail)
        layout.addWidget(self.passv)
        layout.addWidget(self.RadioButton)
        layout.addWidget(self.issue_pass_button2)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.issue_pass_button3)

        self.setLayout(layout)
        self.setWindowTitle('Терминал Охраны')

    def GUEST_ENTRY(self):
        pass1.show()

    def ENTRY(self):
        global guests
        global employees
        self.adc=self.mail.text().find("@")
        self.dfe = self.mail.text()

        self.local_time = time.ctime(time.time())
        if self.car == 1:

            if employees != 0:
                if employees < 5 and guests > 0:
                    employees = employees-1
                    guests = guests-1
                else:
                    employees = employees-1
                sql.execute(f"""UPDATE employees SET enter = ? where email = ? """, [self.local_time, self.dfe])

                sql.execute('SELECT email FROM employees')

                self.rows = sql.fetchall()
                if self.rows.count((self.mail.text(),)):
                    print("Сотрудник", self.dfe, "Вошёл")
                else:
                    print("Такой почты нет в базе данных")
                base.commit()
              
            else:
                print("Извините мест нет")

        elif self.car == 0:
            sql.execute(f"""UPDATE employees SET enter = ? where email = ? """,[self.local_time, self.dfe])
            base.commit()
            sql.execute('SELECT email FROM employees')
            self.rows = sql.fetchall()
            if self.rows.count((self.mail.text(),)):
                print("Сотрудник", self.dfe, "Вошёл")
            else:
                print("Такой почты нет в базе данных")

    def EXIT(self):
        global guests
        global employees
        self.dfe = self.mail.text()
        if self.car == 1:
            if employees < 5 and guests < 5:
                employees = employees+1
                guests = guests+1
            employees = employees+1
        self.local_time = time.ctime(time.time())
        sql.execute(f"""UPDATE employees SET exit = ? where email = ? AND enter != 'NULL' """, [self.local_time, self.dfe])
        sql.execute('SELECT email FROM employees')
        self.rows = sql.fetchall()
        if self.rows.count((self.mail.text(),)):
            print("Сотрудник", self.dfe, "Вышел")
        else:
            print("Такой почты нет в базе данных")
        base.commit()
    base.commit()

    def UPDATE(self):
        if self.car == 0:
            self.car = 1
        else:
            self.car = 0
        print(self.car)

class guest_win(QWidget):
    def __init__(self):

        super().__init__()
        self.car = 0
        global sql2
        global base2
        global employees
        global guests


        self.pass_label = QLabel('Пропускные документы: 0')

        self.issue_pass_button2 = QPushButton('Выход')
        self.issue_pass_button = QPushButton('Вход')
        self.RadioButton = QRadioButton("Парковка")

        self.issue_pass_button.clicked.connect(self.PASS)
        self.issue_pass_button2.clicked.connect(self.GUEST)
        self.RadioButton.toggled.connect(self.UPDATE)

        self.exit = QLineEdit(self,placeholderText="Ведите электронную почту для выхода")

        self.firstname = QLineEdit(self,placeholderText="Фамилия")
        self.name = QLineEdit(self,placeholderText="Имя")
        self.lastname = QLineEdit(self,placeholderText="Отчество")
        self.birth = QLineEdit(self,placeholderText="Дата рождения")
        self.target = QLineEdit(self,placeholderText="Причина посещения")
        self.phone = QLineEdit(self,placeholderText="Номер телефона")
        self.email = QLineEdit(self,placeholderText="Электронная почта")

        layout = QVBoxLayout()

        layout.addWidget(self.pass_label)

        layout.addWidget(self.firstname)
        layout.addWidget(self.name)
        layout.addWidget(self.lastname)
        layout.addWidget(self.birth)
        layout.addWidget(self.target)
        layout.addWidget(self.phone)
        layout.addWidget(self.email)

        layout.addWidget(self.RadioButton)
        layout.addWidget(self.issue_pass_button)
        layout.addWidget(self.exit)
        layout.addWidget(self.issue_pass_button2)

        self.setLayout(layout)
        self.setWindowTitle('Гостевой Терминал')

    def UPDATE(self):
        if self.car == 0:
            self.car = 1
        else:
            self.car = 0
        if guests == 0:
            print("Нет свободных мест!")

    def GUEST(self):
        global guests
        global employees
        if self.car == 1:
            employees = employees + 1
            guests = guests + 1
        self.exi = self.exit.text()
        self.time = time.time()
        self.local_time = time.ctime(time.time())
        sql2.execute(f"""UPDATE guests SET exit = ? where email = ? """, [self.time,self.exi])
        sql2.execute('SELECT email FROM guests')
        self.rows = sql2.fetchall()
        if self.rows.count((self.exit.text(),)):
            print("Гость", self.exi, "Вышел")
            sql2.execute('SELECT enter , exit FROM guests WHERE email = ? ', (self.pochtat,))
            self.rows2 = sql2.fetchall()
            self.tkk = self.rows2[0]
            self.tk,self.tx = self.tkk
            if self.tx-self.tk > 10:
                print(f"Гость {self.exi} - превысил время посещения на {(self.tx)-(self.tk)-10} секунд, Пожалуйста обратитесь к охраннику")
            if self.tx-self.tk < 10:
                print(f"Гость {self.exi} находился на территории {(self.tx)-(self.tk)} ")
        else:
            print("Такой почты нет в базе данных")


    def PASS(self):
        global guests
        global employees
        if self.car == 1:
            if guests == 0:
                print("Нет свободных мест!")
            else:
                employees = employees - 1
                guests = guests - 1
                self.time = time.time()
                self.familt = self.firstname.text()
                self.namet = self.name.text()
                self.otcht = self.lastname.text()
                self.datet = self.birth.text()
                self.celt = self.target.text()
                self.nomert = self.phone.text()
                self.pochtat = self.email.text()
                self.CORT = [(self.familt,self.namet,self.otcht,self.datet,self.celt,self.nomert,self.pochtat,self.time,0)]
                    
                sql2.execute('SELECT email FROM guests')
                self.rows = sql2.fetchall()
                if self.rows.count((self.email.text(),)):
                    print("Пользователь с такой почтой уже существует")
                else:
                    print("Гость", self.pochtat, "Вошёл")
                    sql2.executemany("INSERT INTO guests VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)",self.CORT)
                    base2.commit()
        else:
            self.time = time.time()
            self.familt = self.firstname.text()
            self.namet = self.name.text()
            self.otcht = self.lastname.text()
            self.datet = self.phone.text()
            self.celt = self.target.text()
            self.nomert = self.phone.text()
            self.pochtat = self.email.text()
            self.CORT = [(self.familt, self.namet, self.otcht, self.datet, self.celt, self.nomert, self.pochtat, self.time, 0)]
            sql2.execute('SELECT email FROM guests')
            self.rows = sql2.fetchall()
            if self.rows.count((self.email.text(),)):
                print("Пользователь с такой почтой уже существует")
            else:
                print("Гость", self.pochtat, "Вошёл")
                sql2.executemany("INSERT INTO guests VALUES(?, ? , ?, ?, ? , ?, ? , ?,?)", self.CORT)
                base2.commit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pass_control = PassControlApp()
    pass1 = guest_win()
    pass_control.show()
    sys.exit(app.exec())