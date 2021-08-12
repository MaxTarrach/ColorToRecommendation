import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QColor
import RecommendationModel
import GetSpotify
import  utils
import VisualFeatureExtraction
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtCore import pyqtSlot

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


cluster_centers = 4


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi =dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


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

        # GUI Spotify User ID?

        # GUI submit button
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

        self.listWidget = QListWidget()

        sortedlist = RecommendationModel.getSortedList(image, 4, playlist)

        print(sortedlist)

        for i in range(len(sortedlist)):
            self.listWidget.insertItem(i, GetSpotify.song_name_display(
                str(sortedlist[i][6])) + '    ' + str(sortedlist[i][7]))

        self.listWidget.itemClicked.connect(lambda: self.item_click(self.listWidget.currentRow(), sortedlist))

        # Add List and Image to grid
        self.grid.addWidget(self.listWidget, 6, 1, 1, 3)
        self.grid.addWidget(self.label, 3, 2, 1, 3)

        weights = VisualFeatureExtraction.create_hist(VisualFeatureExtraction.create_cluster(image,cluster_centers))
        colors = VisualFeatureExtraction.create_cluster(image, cluster_centers).cluster_centers_

        # Plot colors inside the gui:
        self.label_plot_1 = QLabel(str(round(weights[0], 2)), self)
        self.label_plot_2 = QLabel(str(round(weights[1], 2)), self)
        self.label_plot_3 = QLabel(str(round(weights[2], 2)), self)
        self.label_plot_4 = QLabel(str(round(weights[3], 2)), self)

        # 4 rgb values of color clustering
        colorValue1 = (colors[0][0], colors[0][1], colors[0][2])
        colorValue2 = (colors[1][0], colors[1][1], colors[1][2])
        colorValue3 = (colors[2][0], colors[2][1], colors[2][2])
        colorValue4 = (colors[3][0], colors[3][1], colors[3][2])

        self.label_plot_1.setStyleSheet('background-color:rgb' + str(colorValue1) + '; border: 1px solid black;')
        self.label_plot_2.setStyleSheet('background-color:rgb' + str(colorValue2) + '; border: 1px solid black;')
        self.label_plot_3.setStyleSheet('background-color:rgb' + str(colorValue3) + '; border: 1px solid black;')
        self.label_plot_4.setStyleSheet('background-color:rgb' + str(colorValue4) + '; border: 1px solid black;')

        self.grid.addWidget(self.label_plot_1, 4, 1)
        self.grid.addWidget(self.label_plot_2, 4, 2)
        self.grid.addWidget(self.label_plot_3, 4, 3)
        self.grid.addWidget(self.label_plot_4, 4, 4)

    def item_click(self, item_position, sortedList):

        self.sc = MplCanvas(self, width=4, height=4, dpi=50)
        self.sc.axes.plot(['Energy', 'Key', 'Loudness', 'Mode', 'Valence', 'Tempo'], [sortedList[item_position][0], sortedList[item_position][1],
                                                                        sortedList[item_position][2], sortedList[item_position][3], sortedList[item_position][4] ,sortedList[item_position][5]])

        self.grid.addWidget(self.sc, 6, 4)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWIndow()

    sys.exit(app.exec_())