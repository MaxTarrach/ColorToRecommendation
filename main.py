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

        self.text1 = QLabel('Titel')
        self.text2 = QLabel('Interpret')
        self.text3 = QLabel('Match rating')

        # GUI elements image file
        self.textFileLoader = QLabel('Image File')
        self.lineFileLoader = QLineEdit(self)
        self.lineFileLoader.setPlaceholderText('Example: /Users/maximiliantarrach/Documents/Bilder/blade_runner.jpeg')

        # GUI elements spotify playlist
        self.textSpotifyLoader = QLabel('Spotify Playlist Link')
        self.lineSpotifyLink = QLineEdit(self)
        self.lineSpotifyLink.setPlaceholderText('Example: https://open.spotify.com/playlist/0cubuWEaRYj2CUCOSkfrIq?si=11af689f2d724676')

        self.buttonFileLoader = QPushButton('Compute')

        self.buttonFileLoader.clicked.connect(lambda: self.button_click(self.lineFileLoader.text(), self.lineSpotifyLink.text()))


        # Grid creation
        self.grid = QGridLayout()

        # Add elements to grid
        self.grid.addWidget(self.textFileLoader, 1, 1)
        self.grid.addWidget(self.lineFileLoader, 1, 2)

        self.grid.addWidget(self.textSpotifyLoader, 2, 1)
        self.grid.addWidget(self.lineSpotifyLink, 2, 2)

        self.grid.addWidget(self.buttonFileLoader, 1, 3, 2, 1)
        self.grid.addWidget(self.text1, 5, 1)
        self.grid.addWidget(self.text2, 5, 2)
        self.grid.addWidget(self.text3, 5, 3)

        self.setLayout(self.grid)

        # Window initiation
        self.setGeometry(50,50,1280,820)
        self.setWindowTitle("Color to song recommendation")
        self.show()


    @pyqtSlot()
    def button_click(self, image, playlist):
        #  Image load and label creation
        self.im = QPixmap(image).scaledToWidth(720)
        self.label = QLabel()
        self.label.setPixmap(self.im)
        # Align center

        self.listWidget = QListWidget()

        for i in range(len(RecommendationModel.sorted_songs)):
            self.listWidget.insertItem(i, GetSpotify.song_name_display(
                str(RecommendationModel.sorted_songs[i][6])) + '    ' + str(RecommendationModel.sorted_songs[i][7]))

        self.grid.addWidget(self.listWidget, 6, 1, 1, 3)
        self.grid.addWidget(self.label, 3, 2, 1, 3)

        bar = utils.plot_colors(VisualFeatureExtraction.create_hist(VisualFeatureExtraction.create_cluster(image,
                                                                                                           cluster_centers)),
                                VisualFeatureExtraction.create_cluster(image, cluster_centers).cluster_centers_)

        # show our color bart
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWIndow()

    sys.exit(app.exec_())