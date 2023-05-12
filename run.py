from PyQt5.QtWidgets import QMainWindow,QApplication, QLabel, QTextEdit,QPushButton, QFileDialog
import PyQt5.QtWidgets
from PyQt5 import uic
from models.ESRGAN import image_enhancer as ie
from video_processing import img_to_vid as i2v
from video_processing import vid_to_img as v2i
import sys
import os
import cv2

class UI(QMainWindow):
    fps=None
    def __init__(self):
        super(UI, self).__init__()

        uic.loadUi("C:/Users/asus/Desktop/Video to image sequence/UI/Video_to_img_ui.ui", self)

        #Defining custom widgets for vriddhi (sv- select video, sf- seleect folder)
        self.button_sv = self.findChild(QPushButton,"pushButton")
        self.path_sv = self.findChild(QTextEdit,"textEdit")
        self.cancel_sv = self.findChild(QPushButton,"pushButton_2")
        self.button_sf = self.findChild(QPushButton,"pushButton_3")
        self.cwd = self.findChild(QPushButton,"pushButton_6")
        self.path_sf = self.findChild(QTextEdit,"textEdit_2")
        self.cancel_sf = self.findChild(QPushButton,"pushButton_4")
        self.execute = self.findChild(QPushButton,"pushButton_5")
        self.outputlabel = self.findChild(QLabel,"label_3")
        self.button_next = self.findChild(QPushButton,"pushButton_7")

        #Actions:
        self.button_sv.clicked.connect(self.video_get)#actions for both select video and path_sv are included
        self.cancel_sv.clicked.connect(self.path_sv_clear)

        self.button_sf.clicked.connect(self.folder_get)#actions for both select folder and path_sf are included
        self.cwd.clicked.connect(self.cwd_store)#path_sf is cwd
        self.cancel_sf.clicked.connect(self.path_sf_clear)

        self.execute.clicked.connect(self.run)#using both path saved, program is run
        
        self.button_next.clicked.connect(self.next_window)
        #show app
        self.show()

        #Functions:
    def video_get(self):
        self.outputlabel.setText("")
        file_path = QFileDialog.getOpenFileName(self, "Selected video will be converted into image sequence:","C:\\Users\\asus\\Desktop\\Video", "Video(*.mp4)")

        if file_path:
            self.path_sv.setText(file_path[0])
        global cv_file
        cv_file= self.path_sv.toPlainText()
    
    def path_sv_clear(self):
        self.path_sv.setText("")

    def folder_get(self):
        self.outputlabel.setText("")
        folder_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder_path:
            self.path_sf.setText(folder_path)
        global cv_folder 
        cv_folder= self.path_sf.toPlainText()

    def cwd_store(self):
        self.outputlabel.setText("")
        folder_path =os.getcwd()
        if folder_path:
            self.path_sf.setText(folder_path)
        global cv_folder
        cv_folder= self.path_sf.toPlainText()

    def path_sf_clear(self):
        self.path_sf.setText("")

    def next_window(self):
        global enhance_folder
        try:
            self.window= PyQt5.QtWidgets.QMainWindow()
            self.window = UI_2()
            self.window.textEdit.setText(cv_folder)
            enhance_folder=cv_folder
            self.window.show()
        except:
            self.window= PyQt5.QtWidgets.QMainWindow()
            self.window = UI_2()
            #self.window.textEdit.setText(cv_folder)
            self.window.show()

    def run(self):
        self.outputlabel.setText(f'Processing...')
        try:
            v2i.vid_to_img(cv_file, cv_folder)
            self.outputlabel.setText(f'Saved sucessfully!!!!')
        except:
            self.outputlabel.setText(f'Invalid selections')

#class for second window initiates
class UI_2(QMainWindow):
    def __init__(self):
        super(UI_2, self).__init__()

        uic.loadUi("C:/Users/asus/Desktop/Video to image sequence/UI/Image_Enhancer.ui",self)

        #Defining custom widgets for vriddhi window2 (snf - select new folder)
        self.cancel_snf= self.findChild(QPushButton,"pushButton_22")
        self.path_snf = self.findChild(QTextEdit,"textEdit")
        self.button_snf = self.findChild(QPushButton,"pushButton_33")

        self.enhance = self.findChild(QPushButton,"pushButton_55")
        self.outputlabel2 = self.findChild(QLabel,"label_33")

        self.convert = self.findChild(QPushButton,"pushButton_66")
        self.outputlabel3 = self.findChild(QLabel,"label_44")
        
        #Actions
        self.cancel_snf.clicked.connect(self.path_snf_clear)
        self.button_snf.clicked.connect(self.folder_new_get)

        self.enhance.clicked.connect(self.enhance_func)
        self.convert.clicked.connect(self.convert_func)

    def path_snf_clear(self):
        self.path_snf.setText("")
        self.outputlabel2.setText("Enhance kardo na...")

    def folder_new_get(self):
        folder_new_path = QFileDialog.getExistingDirectory(None, "Select Folder")
        if folder_new_path:
            self.path_snf.setText(folder_new_path)
        global enhance_folder
        enhance_folder=self.path_snf.toPlainText()
        print(enhance_folder)
    
    def enhance_func(self):
        #label outputlabel2
        self.outputlabel2.setText("Wait...Processing")
        try:
            model_path = 'models/ESRGAN/models/RRDB_ESRGAN_x4.pth'
            images_path = enhance_folder+"/*"
            ie.enhance_image(images_path, model_path)
            self.outputlabel2.setText("Enhanced Images saved")
        except:
            self.outputlabel2.setText("Invalid arguments")
    
    def convert_func(self):
        #label- outputlabel3
        self.outputlabel3.setText("converting to video wait...")
        try:
            i2v.img_to_vid(UI.fps)
            self.outputlabel3.setText(f'Enhancement Successful!!!!')
        except:
            self.outputlabel3.setText(f'Invalid arguments')

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
