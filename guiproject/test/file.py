import sys
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QObject, QRectF, Qt
from PySide2.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView
from PySide2.QtGui import QPixmap


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.file_Select_Btn = QtWidgets.QPushButton(self.centralWidget)
        self.file_Select_Btn.setGeometry(QtCore.QRect(1082, 80, 121, 28))
        self.file_Select_Btn.setObjectName("file_Select_Btn")
        self.file_Select_Btn.setText("Load Image")
        self.gridLayout.addWidget(self.file_Select_Btn)
        MainWindow.setCentralWidget(self.centralWidget)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        Ui_MainWindow.__init__(self)
        QMainWindow.__init__(self)

        # Initialize UI
        self.setupUi(self)
        self.file_Select_Btn.clicked.connect(self.showImage)

    def tr(self, text):
        return QObject.tr(self, text)

    def showImage(self):
        path_to_file = QFileDialog.getExistingDirectory(self, self.tr("Load folder"), self.tr("~/Desktop/"), QFileDialog.ShowDirsOnly
                                             | QFileDialog.DontResolveSymlinks)
        print(path_to_file)
        self.image_viewer = ImageViewer(path_to_file)
        self.image_viewer.show()


class ImageViewer(QWidget):
    def __init__(self, image_path):
        super().__init__()

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.load_image(image_path)

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        self.scene.addPixmap(pixmap)
        self.view.fitInView(QRectF(0, 0, pixmap.width(), pixmap.height()), Qt.KeepAspectRatio)
        self.scene.update()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())