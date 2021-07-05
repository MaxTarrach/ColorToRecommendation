import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap
import cv2
from sklearn.cluster import KMeans
import numpy as np
import  utils
import VisualFeatureExtraction
import matplotlib.pyplot as plt
from PyQt5.QtChart import QChart, QChartView, QHorizontalBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPainter


cluster_centers = 4

image_file = "/Users/maximiliantarrach/Documents/Bilder/test.jpeg"


class MainWIndow(QWidget):

    def __init__(self):
        super().__init__()

        # Image load and label creation
        self.im = QPixmap(image_file).scaledToWidth(720)
        self.label = QLabel()
        self.label.setPixmap(self.im)


        self.text = QLabel('Colorcodes')

        self.textFileLoader = QLabel('Select File')
        self.lineFileLoader = QLineEdit(image_file)
        self.buttonFileLoader = QPushButton('Open...')

        #Grid creation
        self.grid = QGridLayout()
        #Add elements to grid
        self.grid.addWidget(self.textFileLoader,1,1)
        self.grid.addWidget(self.lineFileLoader,1,2)
        self.grid.addWidget(self.buttonFileLoader,1,3)
        self.grid.addWidget(self.label,2,2,1,3)
        self.grid.addWidget(self.text,3,1,1,4)


        self.setLayout(self.grid)

        #Window initiation
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

class SecondaryWindow:
    def __init__(self, parent:None):
        super(SecondaryWindow, self).__init__(parent)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWIndow()

    sys.exit(app.exec_())