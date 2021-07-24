import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap
import cv2
from sklearn.cluster import KMeans
import numpy as np
import RecommendationModel
import GetSpotify
import  utils
import VisualFeatureExtraction
import matplotlib.pyplot as plt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter


cluster_centers = 4

image_file = '/Users/maximiliantarrach/Documents/Bilder/blade_runner.jpeg'

class MainWIndow(QWidget):

    def __init__(self):
        super().__init__()

        #  Image load and label creation
        self.im = QPixmap(image_file).scaledToWidth(720)
        self.label = QLabel()
        self.label.setPixmap(self.im)
        # Align center

        self.listWidget = QListWidget()

        for i in range(len(RecommendationModel.sorted_songs)):
            self.listWidget.insertItem(i, GetSpotify.song_name_display(
                str(RecommendationModel.sorted_songs[i][6])) + '    ' + str(RecommendationModel.sorted_songs[i][7]))

        print(RecommendationModel.sorted_songs)

        self.text1 = QLabel('Titel')
        self.text2 = QLabel('Interpret')
        self.text3 = QLabel('Match rating')



        # Load image file
        self.textFileLoader = QLabel('Select Image File')
        self.lineFileLoader = QLineEdit(self)
        self.buttonFileLoader = QPushButton('Open...')

        self.buttonFileLoader.clicked.connect(lambda: self.button_click(self.lineFileLoader.text()))


        # Grid creation
        self.grid = QGridLayout()

        # Add elements to grid
        self.grid.addWidget(self.textFileLoader, 1, 1)
        self.grid.addWidget(self.lineFileLoader, 1, 2)
        self.grid.addWidget(self.buttonFileLoader, 1, 3)
        self.grid.addWidget(self.label, 2, 2, 1, 3)
        self.grid.addWidget(self.text1, 4, 1)
        self.grid.addWidget(self.text2, 4, 2)
        self.grid.addWidget(self.text3, 4, 3)
        self.grid.addWidget(self.listWidget, 5, 1, 1, 3)

        self.setLayout(self.grid)

        # Window initiation
        self.setGeometry(50,50,1280,820)
        self.setWindowTitle("PyQT show image")
        self.show()

        bar = utils.plot_colors(VisualFeatureExtraction.create_hist(VisualFeatureExtraction.create_cluster(image_file,
                                                                                                           cluster_centers)), VisualFeatureExtraction.create_cluster(image_file, cluster_centers).cluster_centers_)

        # show our color bart
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    @pyqtSlot()
    def button_click(self, text):
        shost = text
        print(shost)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWIndow()

    sys.exit(app.exec_())