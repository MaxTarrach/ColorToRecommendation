import sys
from PyQt5.QtWidgets import QApplication, QMainWindow,QHBoxLayout, QTableWidget,QTableWidgetItem, QSlider, QLabel, QGridLayout, QWidget, QLineEdit, QPushButton, QListWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QColor
import RecommendationModel
import GetSpotify
import  utils
import VisualFeatureExtraction
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtCore import pyqtSlot, Qt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


cluster_centers = 4


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi =dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_ylim([0, 1])
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

        # sliders to canvase

        self.textSlider1 = QLabel('Laune ' + '(0)')
        self.slider1 = QSlider(Qt.Horizontal, self)
        self.slider1.setRange(0, 100)
        self.slider1.setPageStep(5)
        self.slider1.setFocusPolicy(Qt.NoFocus)
        self.slider1.valueChanged.connect(self.updateLabel1)

        self.textSlider2 = QLabel('Ruhe' + '(0)')
        self.slider2 = QSlider(Qt.Horizontal, self)
        self.slider2.setRange(0, 100)
        self.slider2.setPageStep(5)
        self.slider2.setFocusPolicy(Qt.NoFocus)
        self.slider2.valueChanged.connect(self.updateLabel2)

        self.textSlider3 = QLabel('Spannung' + '(0)')
        self.slider3 = QSlider(Qt.Horizontal, self)
        self.slider3.setRange(0, 100)
        self.slider3.setPageStep(5)
        self.slider3.setFocusPolicy(Qt.NoFocus)
        self.slider3.valueChanged.connect(self.updateLabel3)

        self.buttonSlider = QPushButton('Recalculate')

        self.sc = MplCanvas(self, width=4, height=4, dpi=50)

        self.listWidget = QListWidget()

        placeholder = 'Assets/placeholder.jpg'

        #  Image load and label creation
        self.im = QPixmap(placeholder).scaledToWidth(720)
        self.label = QLabel()
        self.label.setPixmap(self.im)

        # Grid creation
        self.grid = QGridLayout()

        # Add elements to grid
        self.grid.addWidget(self.textFileLoader, 0, 0, 1, 1)
        self.grid.addWidget(self.lineFileLoader, 0, 1, 1, 4)

        self.grid.addWidget(self.textSpotifyLoader, 1, 0, 1, 1)
        self.grid.addWidget(self.lineSpotifyLink, 1, 1, 1, 4)

        self.grid.addWidget(self.buttonFileLoader, 0, 5, 2, 1)

        self.grid.addWidget(self.label, 2, 0, 7, 4)

        # Add slider to grid
        self.grid.addWidget(self.textSlider1, 2, 4, 2, 1)
        self.grid.addWidget(self.slider1, 3, 4, 2, 1)

        self.grid.addWidget(self.textSlider2, 4, 4, 2, 1)
        self.grid.addWidget(self.slider2, 5, 4, 2, 1)

        self.grid.addWidget(self.textSlider3, 6, 4, 2, 1)
        self.grid.addWidget(self.slider3, 7, 4, 2, 1)

        self.grid.addWidget(self.buttonSlider, 8, 4, 2, 1)

        self.grid.addWidget(self.listWidget, 10, 0, 2, 4)

        self.grid.addWidget(self.sc, 10, 4, 1, 2)

        self.setLayout(self.grid)

        # Window initiation
        self.setGeometry(50,50,1280,820)
        self.setWindowTitle("Color to song recommendation")
        self.show()


    @pyqtSlot()
    def button_click(self, image, playlist):

        sortedlist = RecommendationModel.getSortedList(image, cluster_centers, playlist)
        weights = VisualFeatureExtraction.create_hist(VisualFeatureExtraction.create_cluster(image, cluster_centers))
        colors = VisualFeatureExtraction.create_cluster(image, cluster_centers).cluster_centers_

        #  Image load and label creation
        self.im = QPixmap(image).scaledToWidth(720)
        self.label = QLabel()
        self.label.setPixmap(self.im)

        self.listWidget = QListWidget()

        print(sortedlist)

        # Put sorted list into table

        self.tableWidget = QTableWidget()

        self.tableWidget.setRowCount(len(sortedlist))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setHorizontalHeaderLabels(('TITEL', 'MATCH'))

        for i in range(len(sortedlist)):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(GetSpotify.song_name_display(str(sortedlist[i][7]))))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(sortedlist[i][8])))

        self.tableWidget.itemClicked.connect(lambda: self.item_click(self.tableWidget.currentRow(), sortedlist))

        self.grid.addWidget(self.tableWidget, 10, 0, 2, 4)
        self.grid.addWidget(self.label, 2, 0, 7, 4)

        # Plot colors inside the gui:
        self.label_plot_1 = QLabel(str(round(weights[0], 3)*100) + '%', self)
        self.label_plot_2 = QLabel(str(round(weights[1], 3)*100) + '%', self)
        self.label_plot_3 = QLabel(str(round(weights[2], 3)*100) + '%', self)
        self.label_plot_4 = QLabel(str(round(weights[3], 3)*100) + '%', self)

        # 4 rgb values of color clustering
        colorValue1 = (colors[0][0], colors[0][1], colors[0][2])
        colorValue2 = (colors[1][0], colors[1][1], colors[1][2])
        colorValue3 = (colors[2][0], colors[2][1], colors[2][2])
        colorValue4 = (colors[3][0], colors[3][1], colors[3][2])

        self.label_plot_1.setStyleSheet('background-color:rgb' + str(colorValue1) + '; border: 1px solid black; color: rgb(78, 253, 84)')
        self.label_plot_2.setStyleSheet('background-color:rgb' + str(colorValue2) + '; border: 1px solid black; color: rgb(78, 253, 84)')
        self.label_plot_3.setStyleSheet('background-color:rgb' + str(colorValue3) + '; border: 1px solid black; color: rgb(78, 253, 84)')
        self.label_plot_4.setStyleSheet('background-color:rgb' + str(colorValue4) + '; border: 1px solid black; color: rgb(78, 253, 84)')

        self.grid.addWidget(self.label_plot_1, 9, 0, 1, 1)
        self.grid.addWidget(self.label_plot_2, 9, 1, 1, 1)
        self.grid.addWidget(self.label_plot_3, 9, 2, 1, 1)
        self.grid.addWidget(self.label_plot_4, 9, 3, 1, 1)

    def item_click(self, item_position, sortedList):

        self.sc = MplCanvas(self, width=4, height=4, dpi=50)
        self.sc.axes.plot(['Energy', 'Loudness', 'Valence', 'Tempo'], [sortedList[item_position][0],
                                                                        sortedList[item_position][2],  sortedList[item_position][4] ,sortedList[item_position][5]])

        self.chroma_key = QLabel('Key: ' + GetSpotify.get_song_key(sortedList[item_position][6]))
        self.mode = QLabel('Mode: ' + GetSpotify.get_song_mode(sortedList[item_position][3]))

        self.grid.addWidget(self.sc, 10, 4, 1, 2)
        self.grid.addWidget(self.chroma_key, 11, 4, 1, 1)
        self.grid.addWidget(self.mode, 11, 5, 1, 1)

    def updateLabel1(self, value):

        self.textSlider1.setText('Laune ' + '(' + str(value) + ')')

    def updateLabel2(self, value):

        self.textSlider2.setText('Laune ' + '(' + str(value) + ')')

    def updateLabel3(self, value):
            self.textSlider3.setText('Laune ' + '(' + str(value) + ')')



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWIndow()

    sys.exit(app.exec_())