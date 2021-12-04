
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QDialog, QMainWindow, QMessageBox)
# from _zaloapi import final_path_mp3
import sys
import requests
import os
import random
import re
import time
import nltk
from urllib.parse import quote


class text2voice:

    def zalo_api(payload, voidid, speed):
        url = "https://zalo.ai/api/demo/v1/tts/synthesize"
        f = open("output.txt", "w")
        links = []
        for p in payload:
            text = quote(str(p))

            # text.encode('utf-8')  # Totally fine.
            payload = "input="+text+"&speaker_id=" + \
                voidid+"&speed="+speed+"&dict_id=0"
            headers = {
                "content-type": "application/x-www-form-urlencoded; charset=utf-8",
                "origin": "https://zalo.ai",
                "referer": "https://zalo.ai/experiments/text-to-audio-converter",

                "cookie": "zpsid=eMKnVbo-PZEvNHqtDTKIOgHQ7p4nrWzalI47O4wZJssuT3bRV_irVuyWFcWShorgrNnyH1sN7H_cHL08DySx4jayN3Kgv2SblZf95sovCHgQRaSg; zai_did=8k9uAj3FNiTevcSSryzXoYYo64d0o6V3AB4PHJ8q; zpsidleg=eMKnVbo-PZEvNHqtDTKIOgHQ7p4nrWzalI47O4wZJssuT3bRV_irVuyWFcWShorgrNnyH1sN7H_cHL08DySx4jayN3Kgv2SblZf95sovCHgQRaSg; zai_sid=lf2zTzCfGqIZbxznrofUGhhifo2eNnvBlxcP6va7P5c8xPue-bDyJDAnt0JxQqmvuOZmID4xQZJUyVnrp1Xs0xdtwLUAHM0ydQFdQl1IIGRigkzd; __zi=3000.SSZzejyD0jydXQcYsa00d3xBfxgP71AM8Tdbg8yB7SWftQxdY0aRp2gIh-QFHXF2BvMWxp0mDW.1; fpsend=149569; _zlang=vn"
            }

            response = requests.request(
                "POST", url, data=payload.encode('utf-8'), headers=headers)
            f.write(response.text+"\n")
            time.sleep(5)

        out = open('output.txt', 'r').read()

        links = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}.m3u8)', out)
        f.close()
        return links

    def split_text(payload):
        text = []
        long_sentence = []
        if len(payload) <= 200:
            text.append(payload)
            return text
        elif len(payload) > 200:
            sentences = nltk.sent_tokenize(payload)
            sub_para = ''

            for sen in sentences:
                if sub_para == '':
                    sub_para = sen

                elif sub_para != '':
                    if len(sub_para)+len(sen) <= 200 and sen != sentences[-1]:
                        sub_para = sub_para + " " + sen

                    elif len(sub_para)+len(sen) <= 200 and sen == sentences[-1]:
                        sub_para = sub_para + " " + sen
                        long_sentence.append(sub_para)

                    elif len(sub_para)+len(sen) > 200:
                        long_sentence.append(sub_para)
                        sub_para = ''
                        sub_para = sen

                    elif sen == sentences[-1]:
                        long_sentence.append(sub_para)

        return long_sentence

    def connect_audio(links):
        id = 1
        path = str(os.getcwd())
        full = path + '/tmp_audio/'
        command = 'cd '+full+' && rm -rf *'
        os.system(command)
        f = open('list_name.txt', 'w')
        for i in links:
            url = i
            des_fol = str(os.getcwd())+"/tmp_audio/"
            namefile = str(id)+".mp3"
            command = 'ffmpeg  -i '+url+' -ab 256k ' + des_fol + namefile + ' -y'
            id = id + 1
            os.system(command)
            f.write("file '"+full+namefile+"'\n")
        f.close()
        print("done")

    def get_links():
        out = open('output.txt', 'r').read()
        links = re.findall(
            r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}.m3u8)', out)
        return links

    def mer_audio(id):
        path_list = str(os.getcwd()) + "/list_name.txt"
        path = str(os.getcwd())+"/final_audio/"

        mp3_path = path+id+".mp3"
        command = 'ffmpeg -f concat -safe 0 -i ' + \
            path_list + ' -c copy '+mp3_path + ' -y'
        os.system(command)

        mp3_path = mp3_path.replace(os.getcwd(), '.')

        return mp3_path


class final_path_mp3():
    def get_path_mp3(id, payload, voiceid, speed):
        path = str(os.getcwd())+"/tmp_audio"
        if os.path.exists(path) == False:
            os.system("mkdir tmp_audio")
        path = str(os.getcwd()) + "/final_audio"
        if os.path.exists(path) == False:
            os.system("mkdir final_audio")
        data = text2voice.split_text(payload)
        text2voice.zalo_api(data, voiceid, speed)
        links = text2voice.get_links()
        text2voice.connect_audio(links)
        path = text2voice.mer_audio(id)

        return path


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("T2SBT")
        MainWindow.resize(647, 412)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.gridLayout.addWidget(self.plainTextEdit, 0, 1, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)
        self.comboBox.setFont(font)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(21)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(
            self.centralwidget, clicked=lambda: self.do_it())
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(19)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 2, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 647, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuBart_Tran = QtWidgets.QMenu(self.menubar)
        self.menuBart_Tran.setObjectName("menuBart_Tran")
        MainWindow.setMenuBar(self.menubar)
        self.actionOpen_2 = QtWidgets.QAction(MainWindow)
        self.actionOpen_2.setCheckable(False)
        self.actionOpen_2.setChecked(False)
        self.actionOpen_2.setObjectName("actionOpen_2")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.menuFile.addAction(self.actionOpen_2)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuBart_Tran.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.plainTextEdit, self.comboBox)
        MainWindow.setTabOrder(self.comboBox, self.pushButton)

    def do_it(self):
        id = "Thank_to_you_for_using_this_program"
        payload = self.plainTextEdit.toPlainText()
        choice = self.comboBox.currentText()
        if choice == "Nữ - Miền Nam":
            voiceid = '1'
            filename = "Nữ_Miền_Nam" + \
                "_" + str(random.randint(1, 10000))
        elif choice == "Nam - Miền Nam":
            voiceid = '2'
            filename = "Nam_Miền_Nam" + \
                "_" + str(random.randint(1, 10000))
        elif choice == "Nữ - Miền Bắc":
            voiceid = '3'
            filename = "Nữ_Miền_Bắc" + \
                "_" + str(random.randint(1, 10000))
        elif choice == "Nam - Miền Bắc":
            voiceid = '4'
            filename = "Nam_Miền_Bắc" + \
                "_" + str(random.randint(1, 10000))
        else:
            filename = id
            voiceid = '1'
        filename = str(filename)
        
        path = final_path_mp3.get_path_mp3(
            id=filename, payload=payload, voiceid=voiceid, speed="1.0")
        print(path)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Text to Speech Bart Tran"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Chọn..."))
        self.comboBox.setItemText(1, _translate("MainWindow", "Nữ - Miền Nam"))
        self.comboBox.setItemText(
            2, _translate("MainWindow", "Nam - Miền Nam"))
        self.comboBox.setItemText(3, _translate("MainWindow", "Nữ - Miền Bắc"))
        self.comboBox.setItemText(
            4, _translate("MainWindow", "Nam - Miền Bắc"))
        self.label.setText(_translate("MainWindow", "Giọng đọc:"))
        self.label_2.setText(_translate("MainWindow", "Văn bản:"))
        self.pushButton.setText(_translate("MainWindow", "Tạo giọng nói"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuBart_Tran.setTitle(_translate("MainWindow", "Bart Tran"))
        self.actionOpen_2.setText(_translate("MainWindow", "Open..."))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
