from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from RARJPEG_Detector_MainWindow import Ui_MainWindow
import sys, os, shutil
import RARJPEG_Detector_Icon as icon

class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.icon_data = icon.Get_icon(icon.icon_str)
        self.setWindowIcon(self.icon_data)
        self.setMinimumWidth(self.width() + 25)
        self.setGeometry(800, 400, self.width(), self.height())
        m = self.menuBar().addMenu("Меню")
        a = m.addAction("О программе")
        a.triggered.connect(self.aboutClicked)
        self.ui.lineEdit.setReadOnly(True)
        self.ui.checkBox.setVisible(False)
        self.ui.pushButton_2.setEnabled(False)
        self.ui.pushButton.clicked.connect(self.SelectFolderButtonClicked)
        self.ui.pushButton_2.clicked.connect(self.FindRARJPEGButtonClicked)
        self.PictureSignatures = ['FF D8 FF DB', 'FF D8 FF E0', '4A 46 49 46 00 01', 'FF D8 FF E1', '45 78 69 66 00 00',    #jpg, jpeg, ...
                                  '89 50 4E 47 0D 0A 1A 0A',                                                                #png
                                  '42 4D',                                                                                  #bmp
                                  '47 49 46 38 37 61', '47 49 46 38 39 61',                                                 #gif
                                  '25 50 44 46']                                                                            #pdf
        self.ArchiveSignatures = ['50 4B 03 04', '50 4B 05 06', '50 4B 07 08',          #zip
                                  '52 61 72 21 1A 07 00', '52 61 72 21 1A 07 01 00',    #rar
                                  '37 7A BC AF 27 1C']                                  #7z

    def FindRARJPEGButtonClicked(self):
        self.FindRARJPEG() if not self.ui.checkBox.isChecked() else self.FindRARJPEGSubDirs()
        # if not self.ui.checkBox.isChecked():
        #     self.FindRARJPEG()
        # else:
        #     self.FindRARJPEGSubDirs()

    def FindRARJPEG(self):
        s = QMessageBox()
        s.setWindowIcon(self.icon_data)
        s1 = QMessageBox()
        s1.setWindowIcon(self.icon_data)
        s1.setText("Пожалуйста, подождите")
        s1.setModal(False)
        s1.setWindowTitle("RARJPEG Detector")
        s1.open()
        FilePath = self.ui.lineEdit.text()
        ListDir = os.listdir(FilePath)
        Files = []
        CountRJ, CountNewRJ, CountNotRJ = 0, 0, 0
        for File_i in ListDir:
            if not os.path.isdir(File_i):
                File_i_FullName = '/'.join([FilePath, File_i])
                Files.append(File_i_FullName)
        for File_i in Files:
            with open(File_i, "rb") as CurFile:
                CurFileContent = CurFile.read()
            CurFile.close()
            CurFileContentBytes = ' '.join(['{:02X}'.format(byte) for byte in CurFileContent])
            if (CurFileContentBytes[:11] == self.PictureSignatures[0]
                or (CurFileContentBytes[:11] == self.PictureSignatures[1] and CurFileContentBytes[18:35] == self.PictureSignatures[2])
                or (CurFileContentBytes[:11] == self.PictureSignatures[3] and CurFileContentBytes[18:35] == self.PictureSignatures[4])
                or CurFileContentBytes[:23] == self.PictureSignatures[5]
                or CurFileContentBytes[:5] == self.PictureSignatures[6]
                or CurFileContentBytes[:17] == self.PictureSignatures[7]
                or CurFileContentBytes[:17] == self.PictureSignatures[8]
                or CurFileContentBytes[:11] == self.PictureSignatures[9]) \
                    and (self.ArchiveSignatures[0] in CurFileContentBytes
                         or self.ArchiveSignatures[1] in CurFileContentBytes
                         or self.ArchiveSignatures[2] in CurFileContentBytes
                         or self.ArchiveSignatures[3] in CurFileContentBytes
                         or self.ArchiveSignatures[4] in CurFileContentBytes
                         or self.ArchiveSignatures[5] in CurFileContentBytes):
                    CountRJ += 1
                    ShortFileName = File_i.split('/')[-1]
                    if ShortFileName[:10] != "[RARJPEG]_":
                        CountNewRJ += 1
                        NewShortFileName = ''.join(["[RARJPEG]_", ShortFileName])
                        NewFileName = '/'.join([FilePath, NewShortFileName])
                        #shutil.move(File_i, NewFileName)
                        os.rename(File_i, NewFileName)
            else:
                ShortFileName = File_i.split('/')[-1]
                if ShortFileName[:10] == "[RARJPEG]_":
                    CountNotRJ += 1
                    NewShortFileName = ShortFileName[10:]
                    NewFileName = '/'.join([FilePath, NewShortFileName])
                    shutil.move(File_i, NewFileName)
        s1.close()
        QMessageBox.information(s, "RARJPEG Detector", f'Папка {FilePath} успешно проверена!\nВсего обнаружено {CountRJ} RARJPEG-ов, среди них {CountNewRJ} новых.\nИсправлены названия {CountNotRJ} файлов, не являющихся RARJPEG-ами\nОбнаруженные RARJPEG-и имеют пометку "[RARJPEG]" в названии', QMessageBox.Ok)

    def FindRARJPEGSubDirs(self):
        FilePath = self.ui.lineEdit.text()
        print(FilePath)

    def SelectFolderButtonClicked(self):
        d = QFileDialog()
        #d.setFileMode(QFileDialog.Directory)
        #d.setNameFilter("*.jpg")
        #d.setViewMode(QFileDialog.Detail)
        FolderToCheckName = d.getExistingDirectory(self, "Выбрать папку", "/home")
        self.ui.lineEdit.setText(FolderToCheckName)
        self.ui.pushButton_2.setEnabled(self.ui.lineEdit.text() != "")
        # if self.ui.lineEdit.text() != "":
        #     self.ui.pushButton_2.setEnabled(True)
        # else:
        #     self.ui.pushButton_2.setEnabled(False)

    def aboutClicked(self):
        q = QMessageBox()
        q.setWindowIcon(self.icon_data)
        q.setStyleSheet('QMessageBox {background-color: white; font-family: Consolas; font-size: 13px;}')
        # q.setStyleSheet('QMessageBox {background-color: white; font-family: Consolas;}')
        QMessageBox.about(q, "О программе", '''RARJPEG Detector 1.2\n
Автор программы:\n
   ____             _             _ _     ____  _  _
  / __ \  __ _ _ __| |_ _ __ ___ (_) |__ |___ \| || |
 / / _` |/ _` | '__| __| '_ ` _ \| | '_ \  __) | || |_
| | (_| | (_| | |  | |_| | | | | | | | | |/ __/|__   _|
 \ \__,_|\__,_|_|   \__|_| |_| |_|_|_| |_|_____|  |_|
  \____/''')


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = mywindow()
    application.show()

    sys.exit(app.exec())