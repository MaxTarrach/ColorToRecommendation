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


class Example(QWidget):

    def __init__(self):
        super().__init__()


        image = VisualFeatureExtraction.read_and_convert_to_rgb(image_file)

        VisualFeatureExtraction.convert_rgb_to_grayscale(image)

        image = VisualFeatureExtraction.reshape_imgdata(image)



        #cluster the pixels
        clt = KMeans(n_clusters= cluster_centers)
        clt.fit(image)

        # build a histogram of clusters and then create a figure
        # representing the number of pixels labeled to each color
        hist = utils.centroid_histogram(clt)

        print(hist)
        print(clt.cluster_centers_)

        x = VisualFeatureExtraction.weighted_rgb_score(clt.cluster_centers_, hist)

        x = utils.transfrom_255_to_1(x)

        y = VisualFeatureExtraction.convert_rgb_to_hsv(x)

        print(x)

        print(y)

        #Image load and label creation
        self.im = QPixmap(image_file)
        self.label = QLabel()
        self.label.setPixmap(self.im)




        #Create Horizontal bar graph

        set0 = QBarSet('Color 1')
        set1 = QBarSet('Color 2')
        set2 = QBarSet('Color 3')
        set3 = QBarSet('Color 4')

        set0.append([4])
        set1.append([3])
        set2.append([2])
        set3.append([1])

        series = QHorizontalBarSeries()
        series.append(set0)
        series.append(set1)
        series.append(set2)
        series.append(set3)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Color Cluster Plot')



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
        self.grid.addWidget(self.label,2,1,1,3)
        self.grid.addWidget(self.text,3,1,1,4)

        self.setLayout(self.grid)

        #Window initiation
        self.setGeometry(50,50,1280,820)
        self.setWindowTitle("PyQT show image")
        self.show()

        bar = utils.plot_colors(hist, clt.cluster_centers_)

        # show our color bart
        plt.figure()
        plt.axis("off")
        plt.imshow(bar)
        plt.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()

    sys.exit(app.exec_())