from PyQt5 import QtWidgets # import PyQt5 widgets
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget
import sys
import cv2
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import UI

### Variables ###
# Image file to analyze
file = '/Users/maximiliantarrach/Documents/Bilder/test.jpeg'

cluster_centers = 4


class Example(QWidget):
    # Create the application object
    app = QtWidgets.QApplication(sys.argv)

    # Create the form object
    first_window = QtWidgets.QWidget()

    first_window.text = QLabel('Hallo')

    first_window.Grid = QGridLayout

    first_window.grid.addWidget(first_window.text, 2, 1)


    # Set window size
    first_window.resize(UI.x_Window_Size, UI.y_Window_Size)

    # Set the form title
    first_window.setWindowTitle("Color to music recommendation system")

    # Show form
    first_window.show()

    # Run the program
    sys.exit(app.exec())