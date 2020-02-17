import os
import sys
import webbrowser

import cv2 as cv
from PySide2.QtCore import QCoreApplication, QRectF, Qt, Slot
from PySide2.QtGui import QBrush, QFont, QImage, QPen, QPixmap
from PySide2.QtWidgets import (
    QAction,
    QApplication,
    QFileDialog,
    QGraphicsScene,
    QGraphicsSimpleTextItem,
    QGraphicsView,
    QMainWindow,
)

import extract
import generate
import logger
import predict


class MainWindow(QMainWindow):
    def __init__(self):
        self.elements = None
        QMainWindow.__init__(self)
        self.setWindowTitle("GUI")
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("File")
        self.open_action = QAction("Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_image)
        self.file_menu.addAction(self.open_action)

        self.predict_action = QAction("Predict", self)
        self.predict_action.setShortcut("Ctrl+P")
        self.predict_action.setEnabled(False)
        self.predict_action.triggered.connect(self.draw_predictions)
        self.file_menu.addAction(self.predict_action)

        self.generate_action = QAction("Generate", self)
        self.generate_action.setShortcut("Ctrl+G")
        self.generate_action.setEnabled(False)
        self.generate_action.triggered.connect(self.generate)
        self.file_menu.addAction(self.generate_action)

        self.graphics_scene = QGraphicsScene()
        self.graphics_view = QGraphicsView(self.graphics_scene)

        self.setCentralWidget(self.graphics_view)

    @Slot()
    def open_image(self):
        path_to_file = QFileDialog.getOpenFileName(
            self, self.tr("Load Image"), self.tr("~/"), self.tr("Images (*.jpg)"),
        )
        image, elements = extract.get_elements_from_path(path_to_file[0])
        self.elements = elements
        image = cv.cvtColor(image, cv.COLOR_GRAY2RGB)
        height, width, channel = image.shape
        bytes_per_line = channel * width
        q_img = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap(q_img)
        self.graphics_scene.addPixmap(pixmap)
        self.graphics_scene.update()
        self.graphics_view.fitInView(
            QRectF(0, 0, pixmap.width(), pixmap.height()), Qt.KeepAspectRatio
        )
        self.predict_action.setEnabled(True)

    @Slot()
    def draw_predictions(self):
        pen = QPen(Qt.green, 4)
        brush = QBrush(Qt.green)
        font = QFont()
        font.setPointSize(16)
        for ele in self.elements:
            QCoreApplication.processEvents()
            crop, bbox = ele
            category, prob = predict.get_prediction((crop, bbox))
            ele.append((category, prob))
            text = QGraphicsSimpleTextItem(f" {category.upper()}: {prob:.0%} ")
            text.setFont(font)
            text_bbox = text.boundingRect()
            text_bg = self.graphics_scene.addRect(text_bbox, pen=pen, brush=brush)
            text_bg.setPos(bbox[0], bbox[1] - text_bbox.height())
            text.setPos(bbox[0], bbox[1] - text_bbox.height())
            self.graphics_scene.addRect(*bbox, pen=pen)
            self.graphics_scene.addItem(text)
            self.graphics_scene.update()
        self.generate_action.setEnabled(True)

    @Slot()
    def generate(self):
        generate.align_elements(self.elements)
        html = generate.generate_html(self.elements)
        with open("output.html", "w+") as html_file:
            html_file.write(html)
        logger.log_info(f"Written HTML to 'output.html'")
        logger.log_info(f"Opening 'output.html' in browser", dim=True)
        webbrowser.open("file://" + os.path.realpath("output.html"))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()

    # Execute application
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
