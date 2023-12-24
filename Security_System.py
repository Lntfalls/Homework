import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt6.QtCore import QTimer, QSize
import sqlite3
import pandas as pd
from datetime import datetime

conn = sqlite3.connect('security_system.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS passes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_number INTEGER,
        first_name TEXT,
        last_name TEXT, 
        entry_time DATETIME,
        exit_time DATETIME 
    )
''')
conn.commit()

conn_guest = sqlite3.connect('guest_system.db')
cursor_guest = conn_guest.cursor()
cursor_guest.execute('''
    CREATE TABLE IF NOT EXISTS guest_passes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        guest_name TEXT,
        guest_lastname TEXT,
        guest_duration TEXT,
        entry_time_1 DATETIME,
        exit_time_1 DATETIME
    )
''')
conn_guest.commit()


class SecurityApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.employee_data = pd.read_excel('bds.xlsx')
        self.setFixedSize(QSize(300, 400))

    def init_ui(self):
        self.sotrudnik = QLabel('Войти как сотрудник:')

        self.pass_number_edit = QLineEdit(self,placeholderText="Номер пропуска...")

        self.first_name_edit = QLineEdit(self,placeholderText="Имя...")

        self.last_name_edit = QLineEdit(self,placeholderText="Фамилия...")

        self.entry_button = QPushButton('Вход')
        self.exit_button = QPushButton('Выход')

        self.guest = QLabel('Войти как гость:')

        self.guest_duration_edit = QLineEdit(self,placeholderText="Время пребывания...")

        self.guest_name_edit = QLineEdit(self,placeholderText="Имя...")

        self.guest_lastname_edit = QLineEdit(self,placeholderText="Фамилия...")

        self.guest_entry_button = QPushButton('Вход')
        self.guest_exit_button = QPushButton('Выход')

        self.entry_button.clicked.connect(self.handle_entry)
        self.exit_button.clicked.connect(self.handle_exit)
        self.guest_entry_button.clicked.connect(self.guest_handle_entry)
        self.guest_exit_button.clicked.connect(self.guest_handle_exit)
        self.guest_timer = QTimer(self)
        self.guest_timer.timeout.connect(self.check_guest_pass_expiry)

        layout = QVBoxLayout()
        layout.addWidget(self.sotrudnik)
        layout.addWidget(self.pass_number_edit)
        layout.addWidget(self.first_name_edit)
        layout.addWidget(self.last_name_edit)
        layout.addWidget(self.entry_button)
        layout.addWidget(self.exit_button)
        layout.addWidget(self.guest)
        layout.addWidget(self.guest_name_edit)
        layout.addWidget(self.guest_lastname_edit)
        layout.addWidget(self.guest_duration_edit)
        layout.addWidget(self.guest_entry_button)
        layout.addWidget(self.guest_exit_button)
        self.setLayout(layout)

        self.setWindowTitle('Терминал Охраны')
        self.show()

    def handle_entry(self):
        id_number = self.pass_number_edit.text()
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()

        if not self.employee_data['Фамилия'].str.strip().str.lower().eq(last_name.lower()).any():
            self.show_error('Сотрудник не найден.')
            return
        if not id_number.isdigit():
            self.show_error('Номер пропуска должен быть числом.')
            return
        if len(id_number) > 10:
            self.show_error('Номер пропуска не должен превышать 10 символов.')
            return

        if not all(map(str.isalpha, [first_name, last_name])):
            self.show_error('Имя и фамилия должны содержать только буквы.')
            return
        if not id_number or not first_name or not last_name:
            self.show_error('Все поля должны быть заполнены.')
            return

        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('INSERT INTO passes (id_number, first_name, last_name, entry_time) VALUES (?, ?, ?, ?)',
            (id_number, first_name, last_name, entry_time))
        conn.commit()

        self.show_message(' Вход выполнен.')

    def handle_exit(self):
        id_number = self.pass_number_edit.text()
        first_name = self.first_name_edit.text()
        last_name = self.last_name_edit.text()

        if not id_number.isdigit():
            self.show_error('Номер пропуска должен быть числом.')
            return
        if len(id_number) > 10:
            self.show_error('Номер пропуска не должен превышать 10 символов.')
            return

        if not all(map(str.isalpha, [first_name, last_name])):
            self.show_error('Имя и фамилия должны содержать только буквы.')
            return

        if not id_number or not first_name or not last_name:
            self.show_error('Все поля должны быть заполнены.')
            return

        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute('UPDATE passes SET exit_time = ? WHERE pass_number = ? AND exit_time IS NULL',
                       (id_number, exit_time))
        conn.commit()

        self.show_message('Выход успешно зарегистрирован.')

    def guest_handle_entry(self):
        guest_name = self.guest_name_edit.text()
        guest_lastname = self.guest_lastname_edit.text()
        guest_duration = self.guest_duration_edit.text()
        durate_time = int(self.guest_duration_edit.text())
        check_time = self.guest_duration_edit.text()

        if not check_time.isdigit():
            self.show_error('Время должно быть числом.')
            return

        if not guest_name or not guest_lastname or not guest_duration:
            self.show_error('Все поля должны быть заполнены.')
            return

        entry_time_1 = datetime.now()
        cursor_guest.execute(
            'INSERT INTO guest_passes (guest_name, guest_lastname, guest_duration, entry_time_1) VALUES (?, ?, ?, ?)',
            (guest_name, guest_lastname, guest_duration, entry_time_1))
        conn_guest.commit()

        self.show_message('Вход выполнен.')
        self.guest_timer.start(1000 * 60 * durate_time)

    def guest_handle_exit(self):
        guest_name = self.guest_name_edit.text()
        guest_lastname = self.guest_lastname_edit.text()
        guest_duration = self.guest_duration_edit.text()
        check_time = self.guest_duration_edit.text()

        if not check_time.isdigit():
            self.show_error('Время должно быть числом.')
            return

        if not all(map(str.isalpha, [guest_name, guest_lastname])):
            self.show_error('Имя и фамилия должны содержать только буквы.')
            return

        if not guest_name or not guest_lastname or not guest_duration:
            self.show_error('Все поля должны быть заполнены.')
            return

        exit_time_1 = datetime.now()

        cursor_guest.execute(
            'UPDATE guest_passes SET exit_time_1 = ? WHERE guest_name = ? AND guest_lastname = ? AND exit_time_1 IS NULL',
            (exit_time_1, guest_name, guest_lastname))
        conn_guest.commit()

        self.show_message('Выход выполнен.')
        self.guest_timer.stop()

    def check_guest_pass_expiry(self):
        current_time = datetime.now()
        cursor_guest.execute(
            'SELECT * FROM guest_passes WHERE exit_time_1 IS NULL AND strftime("%s", ?) > strftime("%s", entry_time_1) + guest_duration',
            (current_time,))
        expired_guests = cursor_guest.fetchall()

        if expired_guests:
            message = 'Время вашего пребывания истекло. Обратитесь к сотруднику охраны.'
            self.show_error(message)

    def show_error(self, message):
        error_box = QMessageBox()
        error_box.setIcon(QMessageBox.Icon.Critical)
        error_box.setText(message)
        error_box.setWindowTitle('Ошибка')
        error_box.exec()

    def show_message(self, message):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Information)
        message_box.setText(message)
        message_box.setWindowTitle('Успех')
        message_box.exec()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SecurityApp()
    sys.exit(app.exec())