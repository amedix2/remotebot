import keyboard
import random
import sys
import os
import threading
import time
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QMainWindow, QLabel


'''
author: amedix2
'''

bot = Bot(token='5937626790:AAGLqO3_UbPa9I144s7sBp28Ddi7ymcG4NI')
dp = Dispatcher(bot)

REG_FLAG = True
USER_ID = 0
USER_NAME = None
SELFOBJ = None


def GUI():
    app = QApplication(sys.argv)
    ex = main_window()
    ex.show()
    sys.exit(app.exec())


class main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(150, 150, 300, 300)
        self.setWindowTitle('Slider')

        self.btn1 = QPushButton('Подключить\nустройство', self)
        self.btn1.setFont(QFont("Times", 20, QFont.Bold))
        self.btn1.resize(220, 100)
        self.btn1.move(40, 60)

        self.btn2 = QPushButton('QR-код', self)
        self.btn2.resize(100, 40)
        self.btn2.move(40, 180)

        self.btn3 = QPushButton('Обратная связь', self)
        self.btn3.resize(100, 40)
        self.btn3.move(160, 180)

        self.btn1.clicked.connect(self.con)
        self.btn2.clicked.connect(self.qr)
        self.btn3.clicked.connect(self.fb)

    def con(self):
        self.win1 = connection(self)
        self.win1.show()

    def qr(self):
        os.system('start qr-code.png')

    def fb(self):
        self.win3 = feedback(self)
        self.win3.show()

    def closeEvent(self, event):
        return 0


class connection(QWidget):
    global room, REG_FLAG, USER_ID, USER_NAME, SELFOBJ

    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        global SELFOBJ
        self.setGeometry(470, 150, 600, 300)
        self.setWindowTitle('Connection')

        self.rl = QLabel(self)
        self.rl.setFont(QFont("Times", 60, QFont.Bold))
        self.rl.setText(room)
        self.rl.resize(300, 100)
        self.rl.move(150, 30)
        self.rl.setAlignment(Qt.AlignCenter)

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 20, QFont.Bold))
        self.us.setText(f'Подключенный пользователь\n{USER_NAME}')
        self.us.resize(600, 100)
        self.us.move(0, 120)
        self.us.setAlignment(Qt.AlignCenter)

        self.ab = QLabel(self)
        self.ab.setFont(QFont("Times", 8, QFont.Cursive))
        self.ab.setText('Отсканируйсте QR-код с помощью камеры на вашем смартфоне\n или самостоятельно найдите @remoteamedixbot в Telegram.\n\n'
                        'Далее, отправте боту код, который вы видите на экране.')
        self.ab.resize(600, 100)
        self.ab.move(0, 190)
        self.ab.setAlignment(Qt.AlignCenter)

        SELFOBJ = self

    def update(self):
        self.us.setText(f'Подключенный пользователь\n{USER_NAME}')
        self.ab.setText('Теперь вы можете свернуть приложение и открыть PowerPoint\n'
                                'Для остановки сессии закройте это окно\n\nПриятного использования!')
        
    def closeEvent(self, event):
        global USER_ID, USER_NAME, REG_FLAG, room
        room = room_id()
        print(room)
        USER_ID = 0
        USER_NAME = None
        REG_FLAG = True
        self.rl.setText(room)
        self.us.setText(f'Подключенный пользователь\n{USER_NAME}')


class feedback(QWidget):
    def __init__(self, *a):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(1090, 150, 530, 300)
        self.setWindowTitle('Feedback')

        self.us = QLabel(self)
        self.us.setFont(QFont("Times", 30, QFont.Bold))
        self.us.setText(f'amedix2@gmail.com\nt.me/amedix2\nvk.com/amedix')
        self.us.resize(530, 300)
        self.us.move(0, 0)
        self.us.setAlignment(Qt.AlignCenter)


def room_id():
    return f'{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}{chr(random.randint(65, 90))}'


def main_bot(dp):
    @dp.message_handler(commands=['start'])
    async def process_start_command(message: types.Message):
        await bot.send_message(message.from_user.id,
                               "Привет!\nЭтот бот управляет пк\n\nВведи код с экрана для "
                               "того, чтобы подключится к пк")

    @dp.message_handler(content_types=['text'])
    async def main(message: types.Message):
        global USER_ID, USER_NAME, REG_FLAG, room, SELFOBJ

        btn_l = KeyboardButton('<<<')
        btn_r = KeyboardButton('>>>')

        keybd = ReplyKeyboardMarkup()
        keybd.add(btn_l, btn_r)

        if REG_FLAG:

            if message.text.upper() == room:
                await bot.send_message(message.from_user.id, "Авторизация прошла успешно!\n\n"
                                                             "Нажмите >>> для того, чтобы переключится на следущий "
                                                             "слайд.\n"
                                                             "Нажмите <<< для того, чтобы переключится на предыдуший "
                                                             "слайд.",
                                       reply_markup=keybd)

                USER_ID = message.from_user.id
                USER_NAME = message.from_user.username
                REG_FLAG = False
                
                connection.update(SELFOBJ)
            else:
                await bot.send_message(message.from_user.id, "Ошибка авторизации")
        else:
            if message.from_user.id == USER_ID:
                if message.text == '>>>':
                    keyboard.send('right')
                    await bot.send_message(message.from_user.id, "Включаем следущий слайд...")
                elif message.text == '<<<':
                    keyboard.send('left')
                    await bot.send_message(message.from_user.id, "Включаем предыдущий слайд...")
                else:
                    await bot.send_message(message.from_user.id, "Такой команды нет")
            else:
                await bot.send_message(message.from_user.id, f"Бот уже используется пользователем @{USER_NAME}")


if __name__ == '__main__':
    room = room_id()
    print(room)

    th1 = threading.Thread(target=GUI, daemon=True)
    th2 = threading.Thread(target=main_bot, args=(dp,), daemon=True)
    th1.start()
    th2.start()

    executor.start_polling(dp, skip_updates=True)
