#used python 2.7
# made by Glaster, 31.12.2020
from PyQt5 import uic, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from playsound import playsound
import speech_recognition as sr
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

Form, _ = uic.loadUiType("design2.ui")
filelist = []
outputpath = ""
list_of_files = []
langcodes=["ar-XA","bn-IN","yue-HK","cs-CZ","da-DK","nl-NL","en-AU","en-US","en-IN","en-GB","fil-PH","fi-FI","fr-CA","fr-FR","de-DE","el-GR","gu-IN","hi-IN","hu-HU","id-ID","it-IT","ja-JP","kn-IN","ko-KR","ml-IN","cmn-CN","nb-NO","pl-PL","pt-BR","pt-PT","ru-RU","sk-SK","es-ES","sv-SE","te-IN","th-TH","tr-TR","uk-UA","vi-VN"]


class Ui(QtWidgets.QDialog, Form):

    def __init__(self):

        super(Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.browseFilesPressed)
        self.pushButton_4.clicked.connect(self.deleteFilesPressed)
        self.pushButton_2.clicked.connect(self.browseOutputFolder)
        self.pushButton_3.clicked.connect(self.recognizeAllCrap)
        self.comboBox.addItems(langcodes)

    def deleteFilesPressed(self):
        listItems = self.table.selectedItems()
        if not listItems: return
        for item in listItems:
            del filelist[self.table.row(item)]
            self.table.takeItem(self.table.row(item))


    def browseFilesPressed(self):
        self.open_dialog_box()

    def open_dialog_box(self):
        filename = QFileDialog.getOpenFileName()
        path = filename[0]
        line = str(path)
        if (".wav" in line or ".mp3" in line or ".ogg" in line) and len(line)>0:
            list_of_files.append(line)
            self.table.addItem(str(path))
            filelist.append(str(path))
        elif len(path) == 0:
           print("Glaster was here")
        else:
            playsound("erro.wav.mp3")

    def browseOutputFolder(self):
        outputpath = str(QFileDialog.getExistingDirectory(None, "Select Directory"))
        self.textEdit.setText(outputpath)

    def recognizeAllCrap(self):
       num=0
       print(str(len(list_of_files)))
       if len(list_of_files)>0 and len(self.textEdit.toPlainText()) >0:

           for x in list_of_files:
               r = sr.Recognizer()
               with sr.AudioFile(x) as source:
                   audio = r.record(source)
                   rec_m = r.recognize_google(audio,language=str(self.comboBox.currentText()))
                   if self.radioButton.isChecked():
                        filename= self.textEdit.toPlainText()+"/output.txt"
                        f=open(filename,'a')
                        f.write(str(rec_m))
                        f.write('\n')
                        f.write('====================')
                        f.write('\n')
                        f.close()
                   else:
                       filename=self.textEdit.toPlainText()+"/output_number"+str(num)+".txt"
                       print(filename)
                       f=open(filename,'w')
                       f.write(str(rec_m))
                       f.close()
                       num=num+1
           playsound("owfw311.wav")





       else:
           playsound("erro.wav.mp3")

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Ui()
    w.show()
    sys.exit(app.exec_())