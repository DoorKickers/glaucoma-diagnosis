# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'v0.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QMessageBox, QFileDialog
from database import Database
from image_file_manage import ImageFileManage
from PyQt5.QtGui import QPixmap, QPainter, QImage, qRgb, QColor
from PyQt5.QtCore import Qt, QRectF
import os
from datetime import datetime
import cv2
from model import ResNet50
import torch, random, numpy
import torchvision.transforms as transforms
from torchvision.transforms import Compose, Resize, ToTensor, Normalize
from PIL import Image
import torch.nn.functional as F

class ImageViewer(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        self.image_item = None
        self.scale_factor = 1.0

    def set_image(self, pixmap):
        self.scene.clear()
        self.image_item = self.scene.addPixmap(pixmap)
        self.scale_factor = 1.0
        self.resetTransform()
        rect = QRectF(pixmap.rect())
        self.setSceneRect(rect)
        self.fitInView(self.image_item, Qt.KeepAspectRatio)

    def wheelEvent(self, event):
        delta = event.angleDelta().y() / 120
        factor = 1.1 ** delta
        self.scale(factor, factor)
        self.scale_factor *= factor

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_R:
            self.reset_image()

    def reset_image(self):
        if self.image_item is not None:
            self.resetTransform()
            # self.fitInView(self.image_item, Qt.KeepAspectRatio)
            self.scale_factor = 1.0

class Ui_MainWindow(object):
    PATIENT = 0
    IMAGE = 1
    HISTORY = 2
    def __init__(self, database: Database):
        self.db = database
        self.patients = None
        self.image_path_list = None
        self.historys = None
        self.work_number = 0
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.cnnmodel = ResNet50(2).to(self.device)
        self.cnnmodel.load_state_dict(torch.load('/home/naitnal/Code/DL/remember_download_first_try/v0/ResNet50-glacuoma_modelweight.pth'))
        seed = 29
        torch.manual_seed(seed)
        random.seed(seed)
        numpy.random.seed(seed)
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1386, 966)
        self.MainWindow = MainWindow
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 60, 1341, 851))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.pushButton = QtWidgets.QPushButton(self.page)
        self.pushButton.setGeometry(QtCore.QRect(110, 410, 80, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.page)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 370, 80, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.stackedWidget.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(160, 40, 61, 31))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit.setGeometry(QtCore.QRect(160, 70, 51, 23))
        self.lineEdit.setObjectName("lineEdit")
        self.listWidget_2 = QtWidgets.QListWidget(self.page_2)
        self.listWidget_2.setGeometry(QtCore.QRect(10, 540, 131, 271))
        self.listWidget_2.setObjectName("listWidget_2")
        self.listWidget_2.clicked.connect(self.select_image)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 70, 51, 23))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        self.label_2.setGeometry(QtCore.QRect(220, 40, 61, 31))
        self.label_2.setObjectName("label_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_3.setGeometry(QtCore.QRect(280, 70, 51, 23))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.page_2)
        self.label_3.setGeometry(QtCore.QRect(280, 40, 61, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.page_2)
        self.label_4.setGeometry(QtCore.QRect(160, 140, 91, 31))
        self.label_4.setObjectName("label_4")
        self.graphicsView = ImageViewer(self.page_2)
        self.graphicsView.setGeometry(QtCore.QRect(390, 40, 761, 611))
        self.graphicsView.setObjectName("graphicsView")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(160, 120, 211, 21))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setGeometry(QtCore.QRect(160, 100, 57, 15))
        self.label_5.setObjectName("label_5")
        self.pushButton_3 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_3.setGeometry(QtCore.QRect(280, 750, 80, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.modify_patient_information)
        self.pushButton_4 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 750, 80, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.reset_patient_information)
        self.pushButton_5 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_5.setGeometry(QtCore.QRect(180, 790, 80, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.last_undiaged_patient)
        self.pushButton_6 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_6.setGeometry(QtCore.QRect(280, 790, 80, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.next_undiaged_patient)

        self.pushButton_7 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QtCore.QRect(160, 10, 90, 23))
        self.pushButton_7.clicked.connect(self.import_excel_data)

        self.pushButton_11 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_11.setObjectName(u"pushButton_11")
        self.pushButton_11.setGeometry(QtCore.QRect(270, 10, 90, 23))
        self.pushButton_11.clicked.connect(self.export_excel_data)
        
        self.label_6 = QtWidgets.QLabel(self.page_2)
        self.label_6.setGeometry(QtCore.QRect(160, 520, 191, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.page_2)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.page_2)
        self.label_8.setGeometry(QtCore.QRect(10, 520, 131, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self.page_2)
        self.label_9.setGeometry(QtCore.QRect(390, 670, 57, 15))
        self.label_9.setObjectName("label_9")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_7.setGeometry(QtCore.QRect(530, 690, 113, 23))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_11.setGeometry(QtCore.QRect(530, 740, 111, 23))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_12.setGeometry(QtCore.QRect(530, 790, 111, 23))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.label_10 = QtWidgets.QLabel(self.page_2)
        self.label_10.setGeometry(QtCore.QRect(530, 670, 57, 15))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.page_2)
        self.label_11.setGeometry(QtCore.QRect(530, 770, 91, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.page_2)
        self.label_12.setGeometry(QtCore.QRect(530, 720, 57, 15))
        self.label_12.setObjectName("label_12")
        self.textEdit = QtWidgets.QTextEdit(self.page_2)
        self.textEdit.setGeometry(QtCore.QRect(160, 170, 211, 331))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.page_2)
        self.textEdit_2.setGeometry(QtCore.QRect(160, 540, 211, 201))
        self.textEdit_2.setObjectName("textEdit_2")
        self.listWidget_4 = QtWidgets.QListWidget(self.page_2)
        self.listWidget_4.setGeometry(QtCore.QRect(390, 690, 121, 151))
        self.listWidget_4.setObjectName("listWidget_4")
        self.listWidget_4.clicked.connect(self.select_history)
        self.label_13 = QtWidgets.QLabel(self.page_2)
        self.label_13.setGeometry(QtCore.QRect(670, 670, 91, 16))
        self.label_13.setObjectName("label_13")
        self.textEdit_3 = QtWidgets.QTextEdit(self.page_2)
        self.textEdit_3.setGeometry(QtCore.QRect(670, 690, 121, 151))
        self.textEdit_3.setObjectName("textEdit_3")
        self.pushButton_8 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_8.setGeometry(QtCore.QRect(820, 690, 90, 23))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.clicked.connect(self.modify_history_information)
        self.checkBox = QtWidgets.QCheckBox(self.page_2)
        self.checkBox.setGeometry(QtCore.QRect(1180, 50, 85, 21))
        self.checkBox.setObjectName("checkBox")
        self.checkBox.stateChanged.connect(self.check_gray)
        self.checkBox_2 = QtWidgets.QCheckBox(self.page_2)
        self.checkBox_2.setGeometry(QtCore.QRect(1180, 80, 85, 21))
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkBox_2.stateChanged.connect(self.check_CLAHE)
        self.checkBox_3 = QtWidgets.QCheckBox(self.page_2)
        self.checkBox_3.setGeometry(QtCore.QRect(1180, 110, 101, 21))
        self.checkBox_3.setObjectName("checkBox_3")
        self.checkBox_3.stateChanged.connect(self.check_R_channel)
        self.checkBox_4 = QtWidgets.QCheckBox(self.page_2)
        self.checkBox_4.setGeometry(QtCore.QRect(1180, 140, 121, 21))
        self.checkBox_4.setObjectName("checkBox_4")
        self.checkBox_4.stateChanged.connect(self.check_G_channel)
        self.checkBox_5 = QtWidgets.QCheckBox(self.page_2)
        self.checkBox_5.setGeometry(QtCore.QRect(1180, 170, 121, 21))
        self.checkBox_5.setObjectName("checkBox_5")
        self.checkBox_5.stateChanged.connect(self.check_B_channel)
        self.label_14 = QtWidgets.QLabel(self.page_2)
        self.label_14.setGeometry(QtCore.QRect(1180, 30, 111, 16))
        self.label_14.setObjectName("label_14")
        self.pushButton_9 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_9.setGeometry(QtCore.QRect(1180, 200, 80, 23))
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.clicked.connect(self.deselect_image_param)
        self.checkBox_6 = QtWidgets.QCheckBox(self.page_2)
        self.checkBox_6.setGeometry(QtCore.QRect(820, 730, 85, 21))
        self.checkBox_6.setObjectName("checkBox_6")
        self.checkBox_6.stateChanged.connect(self.history_add_new)
        self.label_15 = QtWidgets.QLabel(self.page_2)
        self.label_15.setGeometry(QtCore.QRect(1190, 320, 81, 16))
        self.label_15.setObjectName("label_15")
        self.pushButton_10 = QtWidgets.QPushButton(self.page_2)
        self.pushButton_10.setGeometry(QtCore.QRect(1190, 340, 111, 23))
        self.pushButton_10.setObjectName("pushButton_10")
        self.pushButton_10.clicked.connect(self.auto_analyze)
        self.label_16 = QtWidgets.QLabel(self.page_2)
        self.label_16.setGeometry(QtCore.QRect(1170, 390, 81, 16))
        self.label_16.setObjectName("label_16")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_4.setGeometry(QtCore.QRect(1250, 390, 71, 23))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.label_17 = QtWidgets.QLabel(self.page_2)
        self.label_17.setGeometry(QtCore.QRect(1170, 430, 81, 16))
        self.label_17.setObjectName("label_17")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_6.setGeometry(QtCore.QRect(1250, 430, 71, 23))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.stackedWidget.addWidget(self.page_2)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 100, 131, 471))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.clicked.connect(self.select_patients)

        self.label_18 = QtWidgets.QLabel(self.page_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QtCore.QRect(940, 670, 90, 15))

        self.lineEdit_8 = QtWidgets.QLineEdit(self.page_2)
        self.lineEdit_8.setObjectName(u"lineEdit_8")
        self.lineEdit_8.setGeometry(QtCore.QRect(940, 690, 113, 23))
        self.lineEdit_8.setReadOnly(True)
        self.lineEdit_8.setText(str(self.work_number))
        self.lineEdit_8.setAlignment(Qt.AlignCenter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1386, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.load_patients()
        self.display(self.listWidget, 0)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Glaucoma Diagnosis"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.label.setText(_translate("MainWindow", "name"))
        self.label_2.setText(_translate("MainWindow", "age"))
        self.label_3.setText(_translate("MainWindow", "gender"))
        self.label_4.setText(_translate("MainWindow", "description"))
        self.label_5.setText(_translate("MainWindow", "ID"))
        self.pushButton_3.setText(_translate("MainWindow", "modify"))
        self.pushButton_4.setText(_translate("MainWindow", "reset"))
        self.pushButton_5.setText(_translate("MainWindow", "last"))
        self.pushButton_6.setText(_translate("MainWindow", "next"))
        self.pushButton_7.setText(_translate("MainWindow", "import data"))
        self.pushButton_11.setText(_translate("MainWindow", "export data"))
        self.label_6.setText(_translate("MainWindow", "additional cynical information"))
        self.label_7.setText(_translate("MainWindow", "patient list"))
        self.label_8.setText(_translate("MainWindow", "fundus image list"))
        self.label_9.setText(_translate("MainWindow", "history"))
        self.label_10.setText(_translate("MainWindow", "time"))
        self.label_11.setText(_translate("MainWindow", "final result"))
        self.label_12.setText(_translate("MainWindow", "AI result"))
        self.label_13.setText(_translate("MainWindow", "doctor note"))
        self.pushButton_8.setText(_translate("MainWindow", "modify/add"))
        self.checkBox.setText(_translate("MainWindow", "Grayscale"))
        self.checkBox_2.setText(_translate("MainWindow", "CLAHE"))
        self.checkBox_3.setText(_translate("MainWindow", "Red Channel"))
        self.checkBox_4.setText(_translate("MainWindow", "Green Channel"))
        self.checkBox_5.setText(_translate("MainWindow", "Blue Channel"))
        self.label_14.setText(_translate("MainWindow", "Image processing"))
        self.pushButton_9.setText(_translate("MainWindow", "deselect"))
        self.checkBox_6.setText(_translate("MainWindow", "add new"))
        self.label_15.setText(_translate("MainWindow", "AI module"))
        self.pushButton_10.setText(_translate("MainWindow", "Auto analyze"))
        self.label_16.setText(_translate("MainWindow", "Blur degree"))
        self.label_17.setText(_translate("MainWindow", "illness prob"))
        self.label_18.setText(_translate("MainWindow", "Work Count"))
    
    def load_patients(self) -> None:
        self.patients = self.db.get_patients()
    
    def load_historys(self, patient_id):
        self.historys = self.db.get_historys(patient_id)

    def select_history(self):
        index = self.listWidget_4.currentRow()
        if index >= 0 and index < len(self.patients):       
            history = self.historys[index]
            self.lineEdit_7.setText(str(history["time"]))
            self.lineEdit_11.setText(str(history["ai_diagnosis"]))
            self.lineEdit_12.setText(str(history["final_diagnosis"]))
            self.textEdit_3.setText(str(history["doctor_note"]))
        else:
            self.clear_history_information()
            
    def import_excel_data(self):
        file_path, _ = QFileDialog.getOpenFileName(self.MainWindow, "Open Excel File", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.db.import_data_from_excel(file_path)

    def export_excel_data(self):
        save_path, _ = QFileDialog.getSaveFileName(self.MainWindow, "Save Excel File", "", "Excel Files (*.xlsx)")
        if save_path:
            self.db.export_data_to_excel(save_path)
    
    def select_patients(self):
        self.clear_auto_analyze_result()
        index = self.listWidget.currentRow()
        if index >= 0 and index < len(self.patients):
            patient = self.patients[index]
            id = patient["id"]
            self.lineEdit.setText(str(patient["name"]))
            self.lineEdit_2.setText(str(patient["age"]))
            self.lineEdit_3.setText(str(patient["gender"]))
            self.lineEdit_5.setText(str(patient["id_number"]))
            self.textEdit.setText(str(patient["description"]))
            self.textEdit_2.setText(str(patient["additional_information"]))
            currentPath = os.path.abspath(__file__)
            currentDir = os.path.dirname(currentPath)
            image_dir = os.path.join(currentDir, "img")
            image_path_list = ImageFileManage.get_image_path_list_by_patient_id(image_dir, id)
            self.image_path_list = image_path_list
            self.display(self.listWidget_2, 1)
            self.graphicsView.scene.clear()
            self.load_historys(id)
            self.display(self.listWidget_4, 2)
            self.select_history()

    def display(self, list_widget: QtWidgets.QListWidget, info_type: int) -> None:
        list_widget.clear()
        if info_type == 0:
            for patient in self.patients:
                patient_info = f"{patient['id']}-{patient['name']}"
                list_widget.addItem(patient_info)

        elif info_type == 1:
            for path in self.image_path_list:
                image_name = os.path.basename(path)
                list_widget.addItem(image_name)

        elif info_type == 2:
            for history in self.historys:
                history_info = f"{history['time']}"
                list_widget.addItem(history_info)

        else:
            return
    @staticmethod
    def extract_channel(cv_image, channel):
        channel_image = cv_image[:, :, channel]
        bgr_image = cv2.merge([channel_image, channel_image, channel_image])
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        return gray_image

    @staticmethod
    def apply_clahe_gray(cv_image):
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_image = clahe.apply(cv_image)
        return enhanced_image

    @staticmethod
    def apply_clahe_RGB_color(cv_image):
        lab_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2LAB)

        l_channel, a_channel, b_channel = cv2.split(lab_image)

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced_l_channel = clahe.apply(l_channel)

        enhanced_lab_image = cv2.merge((enhanced_l_channel, a_channel, b_channel))

        enhanced_image = cv2.cvtColor(enhanced_lab_image, cv2.COLOR_LAB2BGR)
        return enhanced_image

    @staticmethod
    def cv_to_qimage_bgr(cv_image):
        height, width, channels = cv_image.shape
        bytes_per_line = channels * width
        q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
        return q_image.copy()

    @staticmethod
    def cv_to_qimage_gray(cv_image):
        height, width = cv_image.shape
        bytes_per_line = width
        q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        return q_image.copy()

    @staticmethod 
    def compute_blur_score_lap(image):
        # print(image.shape)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return blur_score

    @staticmethod
    def compute_blur_score_sobel(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

        gradient_magnitude = cv2.magnitude(sobel_x, sobel_y)

        mean_gradient = cv2.mean(gradient_magnitude)[0]

        return mean_gradient

    def set_result_text(self, probability, blur_score):
        if blur_score > 100:
            self.lineEdit_6.setText(f"{probability}% ill")
        else:
            self.lineEdit_6.setText("Image too blur!")
        self.lineEdit_4.setText(str(blur_score))
        if self.checkBox_6.isChecked() == True:
            self.lineEdit_11.setText(f"{probability}% ill")

    def auto_analyze(self):
        index = self.listWidget_2.currentRow()
        if index == -1:
            return
        image_abs_path = self.image_path_list[index]

        # generate image_text_abs_path by replace the suffix of image_abs_path after '.'
        image_text_abs_path = image_abs_path[:image_abs_path.rfind('.')] + '.txt'
        if os.path.exists(image_text_abs_path):

            # read two float numbers from image_text_abs_path
            with open(image_text_abs_path, 'r') as f:
                blur_score = float(f.readline())
                probability = float(f.readline())
        else:
            transform = Compose([
                Resize((224, 224)),
                ToTensor(),
            ])
            image = Image.open(image_abs_path)
            blur_score = round(self.compute_blur_score_sobel(numpy.array(image)), 2)
            print(f"blur_score : {blur_score}")
            input_image = transform(image).unsqueeze(0).to(self.device)
            self.cnnmodel.eval()

            with torch.no_grad():
                output = self.cnnmodel(input_image)
                probabilities = F.softmax(output, dim=1)
                probability = round(probabilities[0][0].item() * 100, 2)
            
            # open image_text_abs_path and write two float numbers
            with open(image_text_abs_path, 'w') as f:
                f.write(str(blur_score) + '\n')
                f.write(str(probability) + '\n')

        self.set_result_text(probability, blur_score)
            
    def deselect_image_param(self):
        self.checkBox.setChecked(False)
        self.checkBox_2.setChecked(False)
        self.checkBox_3.setChecked(False)
        self.checkBox_4.setChecked(False)
        self.checkBox_5.setChecked(False)

    def check_CLAHE(self):
        self.select_image()
    
    def check_gray(self, state):
        if state == 2:
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
        self.select_image()

    def check_R_channel(self, state):
        if state == 2:
            self.checkBox.setChecked(False)
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
        self.select_image()
    
    def check_G_channel(self, state):
        if state == 2:
            self.checkBox.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_5.setChecked(False)
        self.select_image()

    def check_B_channel(self, state):
        if state == 2: 
            self.checkBox.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_4.setChecked(False)
        self.select_image()

    def process_image(self, image_path) -> QPixmap:
        # image = QImage(image_path)
        image = cv2.imread(image_path)
        gray = False
        if self.checkBox.isChecked() == True:
            gray = True
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            gray = True
            if self.checkBox_3.isChecked() == True:
                image = self.extract_channel(image, 2)
            elif self.checkBox_4.isChecked() == True:
                image = self.extract_channel(image, 1)
            elif self.checkBox_5.isChecked() == True:
                image = self.extract_channel(image, 0)
            else:
                gray = False
        
        if self.checkBox_2.isChecked() == True:
            if gray:
                image = self.apply_clahe_gray(image)
            else:
                image = self.apply_clahe_RGB_color(image)
            
        if gray:
            image = self.cv_to_qimage_gray(image)
        else:
            image = self.cv_to_qimage_bgr(image)

        return QPixmap.fromImage(image)
    
    def clear_auto_analyze_result(self):
        self.lineEdit_4.clear()
        self.lineEdit_6.clear()

    def select_image(self):
        self.clear_auto_analyze_result()
        index = self.listWidget_2.currentRow()
        if index >= 0 and index < len(self.image_path_list):
            image_abs_path = self.image_path_list[index]
            # image_pixmap = QPixmap(image_abs_path)
            image_pixmap = self.process_image(image_abs_path)
            self.graphicsView.set_image(image_pixmap)
            # check whether the image has been processed
            image_text_abs_path = image_abs_path[:image_abs_path.rfind('.')] + '.txt'
            if os.path.exists(image_text_abs_path):
                with open(image_text_abs_path, 'r') as f:
                    blur_score = float(f.readline())
                    probability = float(f.readline())
                    self.set_result_text(probability, blur_score)


    def reset_patient_information(self):
        self.select_patients()

    def modify_patient_information(self):
        index = self.listWidget.currentRow()
        if index == -1:
            return
        patient = self.patients[index]
        patient_id = patient["id"]
        name = self.lineEdit.text()
        age = int(self.lineEdit_2.text())
        gender = self.lineEdit_3.text()
        id_number = self.lineEdit_5.text()
        description = self.textEdit.toPlainText()
        addtional_information = self.textEdit_2.toPlainText()
        self.db.update_patient(patient_id, name, age, gender, id_number, description, addtional_information)
        self.patients[index]["name"] = name
        self.patients[index]["age"] = age
        self.patients[index]["gender"] = gender
        self.patients[index]["id_number"] = id_number
        self.patients[index]["description"] = description
        self.patients[index]["additional_information"] = addtional_information
        patient = self.patients[index]
        self.select_patients()
        item = self.listWidget.item(index)
        if item is not None:
            item.setText(f"{patient['id']}-{patient['name']}")
        # self.display(self.listWidget, 0)
    
    def modify_history_information(self):
        if self.checkBox_6.isChecked() == True:
            time = self.lineEdit_7.text()
            ai_diag = self.lineEdit_11.text()
            final_diag = self.lineEdit_12.text()
            doctor_note = self.textEdit_3.toPlainText()
            patient_index = self.listWidget.currentRow()
            patient_id = self.patients[patient_index]["id"]
            if time and ai_diag and final_diag and doctor_note:
                self.db.add_history(patient_id, time, ai_diag, final_diag, doctor_note)
                self.work_number = self.work_number + 1
                print(f"Work number++, current work number is : {self.work_number}")
                self.lineEdit_8.setText(str(self.work_number))
                self.lineEdit_8.setAlignment(Qt.AlignCenter)
                self.select_patients()
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Add history failed, somewhere is empty!")
                msg.setWindowTitle("Warning")
                msg.exec_()
        else:
            index = self.listWidget_4.currentRow()
            if index == -1:
                return
            history = self.historys[index]
            history_id = history["id"]
            time = self.lineEdit_7.text()
            ai_diag = self.lineEdit_11.text()
            final_diag = self.lineEdit_12.text()
            doctor_note = self.textEdit_3.toPlainText()
            self.db.update_history(history_id, time, ai_diag, final_diag, doctor_note)
            self.historys[index]["time"] = time
            self.historys[index]["ai_diagnosis"] = ai_diag
            self.historys[index]["final_diagnosis"] = final_diag
            self.historys[index]["doctor_note"] = doctor_note
            history = self.historys[index]
            self.select_history()
            item = self.listWidget_4.item(index)
            if item is not None:
                item.setText(f"{history['time']}")

    def clear_history_information(self):
        self.lineEdit_7.clear()
        self.lineEdit_11.clear()
        self.lineEdit_12.clear()
        self.textEdit_3.clear()
        if self.checkBox_6.isChecked():
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            self.lineEdit_7.setText(formatted_time)

    def next_undiaged_patient(self):
        index = self.listWidget.currentRow()
        if index == -1: index = 0
        for i in range(0, len(self.patients)):
            if self.patients[i]["diaged"] == False:
                self.listWidget.setCurrentRow(i)
                break
        self.select_patients()

    def last_undiaged_patient(self):
        index = self.listWidget.currentRow()
        if index == -1: index = len(self.patients) - 1
        for i in range(index, -1, -1):
            if self.patients[i]["diaged"] == False:
                self.listWidget.setCurrentRow(i)
                break
        self.select_patients()
    
    def history_add_new(self, state):
        self.clear_history_information()
        if state == 2:
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
            self.select_patients() # in order to dis-select history
            self.lineEdit_7.setText(formatted_time)



class MainWindow(QMainWindow):
    def __init__(self, database: Database):
        super().__init__()
        self.ui = Ui_MainWindow(database)
        self.ui.setupUi(self)

app = QApplication(sys.argv)
window = MainWindow(Database('/home/naitnal/Code/DL/remember_download_first_try/v0/demo.db'))
window.show()
sys.exit(app.exec_())