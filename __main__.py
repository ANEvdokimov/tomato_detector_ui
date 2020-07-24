from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
import main_window
import sys
import cv2
import numpy as np
import tomato_detector


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    source_image_bgr = []

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # self.setFixedSize(672, 645)

        self.sbx_minH.valueChanged.connect(self.sbx_colors_handler)
        self.sbx_minS.valueChanged.connect(self.sbx_colors_handler)
        self.sbx_minV.valueChanged.connect(self.sbx_colors_handler)
        self.sbx_maxH.valueChanged.connect(self.sbx_colors_handler)
        self.sbx_maxS.valueChanged.connect(self.sbx_colors_handler)
        self.sbx_maxV.valueChanged.connect(self.sbx_colors_handler)

        self.chbx_circularity.stateChanged.connect(self.chbx_circularity_handler)
        self.chbx_convexity.stateChanged.connect(self.chbx_convexity_handler)
        self.chbx_inertia.stateChanged.connect(self.chbx_inertia_handler)
        self.chbx_area.stateChanged.connect(self.chbx_area_handler)

        self.sld_minCircularity.valueChanged.connect(self.sld_min_circularity_handler)
        self.sld_maxCircularity.valueChanged.connect(self.sld_max_circularity_handler)
        self.sld_minConvexity.valueChanged.connect(self.sld_min_convexity_handler)
        self.sld_maxConvexity.valueChanged.connect(self.sld_max_convexity_handler)
        self.sld_minInertia.valueChanged.connect(self.sld_min_inertia_handler)
        self.sld_maxInertia.valueChanged.connect(self.sld_max_inertia_handler)
        self.sbx_minArea.valueChanged.connect(self.sbx_area_handler)
        self.sbx_maxArea.valueChanged.connect(self.sbx_area_handler)

        self.chbx_whiteBalance.stateChanged.connect(self.chbx_white_balance_handler)
        self.chbx_contrast.stateChanged.connect(self.chbx_contrast_handler)
        self.chbx_splitFruit.stateChanged.connect(self.chbx_splitFruit_handler)

        self.btn_open.clicked.connect(self.btn_open_handler)

    def btn_open_handler(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self, "Открыть")[0]
        if file_name:
            try:
                self.open_image(file_name)
                self.lbl_fileName.setText(file_name)
            except IOError as e:
                message_box = QtWidgets.QMessageBox()
                message_box.setText(str(e))
                message_box.setWindowTitle("IOError")
                message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
                message_box.exec()

    def open_image(self, file_name):
        opened_image = cv2.imread(file_name)
        if opened_image is None:
            raise IOError("Ошибка при открытии изображения.")
        self.source_image_bgr = opened_image
        self.redraw_image()

    def sbx_colors_handler(self):
        self.redraw_image()

    def chbx_white_balance_handler(self):
        self.redraw_image()

    def chbx_contrast_handler(self):
        self.redraw_image()

    def chbx_splitFruit_handler(self):
        self.redraw_image()

    def sld_min_circularity_handler(self):
        self.lbl_minCircularity.setText(str(self.sld_minCircularity.value() / 20))
        self.redraw_image()

    def sld_max_circularity_handler(self):
        self.lbl_maxCircularity.setText(str(self.sld_maxCircularity.value() / 20))
        self.redraw_image()

    def sld_min_convexity_handler(self):
        self.lbl_minConvexity.setText(str(self.sld_minConvexity.value() / 20))
        self.redraw_image()

    def sld_max_convexity_handler(self):
        self.lbl_maxConvexity.setText(str(self.sld_maxConvexity.value() / 20))
        self.redraw_image()

    def sld_min_inertia_handler(self):
        self.lbl_minInertia.setText(str(self.sld_minInertia.value() / 20))
        self.redraw_image()

    def sld_max_inertia_handler(self):
        self.lbl_maxInertia.setText(str(self.sld_maxInertia.value() / 20))
        self.redraw_image()

    def sbx_area_handler(self):
        self.redraw_image()

    def chbx_circularity_handler(self):
        if self.chbx_circularity.isChecked():
            is_enable = True
        else:
            is_enable = False
        self.lbl_minCircularity_name.setEnabled(is_enable)
        self.sld_minCircularity.setEnabled(is_enable)
        self.lbl_minCircularity.setEnabled(is_enable)
        self.lbl_maxCircularity_name.setEnabled(is_enable)
        self.sld_maxCircularity.setEnabled(is_enable)
        self.lbl_maxCircularity.setEnabled(is_enable)

        self.redraw_image()

    def chbx_convexity_handler(self):
        if self.chbx_convexity.isChecked():
            is_enable = True
        else:
            is_enable = False
        self.lbl_minConvexity_name.setEnabled(is_enable)
        self.sld_minConvexity.setEnabled(is_enable)
        self.lbl_minConvexity.setEnabled(is_enable)
        self.lbl_maxConvexity_name.setEnabled(is_enable)
        self.sld_maxConvexity.setEnabled(is_enable)
        self.lbl_maxConvexity.setEnabled(is_enable)

        self.redraw_image()

    def chbx_inertia_handler(self):
        if self.chbx_inertia.isChecked():
            is_enable = True
        else:
            is_enable = False
        self.lbl_minInertia_name.setEnabled(is_enable)
        self.sld_minInertia.setEnabled(is_enable)
        self.lbl_minInertia.setEnabled(is_enable)
        self.lbl_maxInertia_name.setEnabled(is_enable)
        self.sld_maxInertia.setEnabled(is_enable)
        self.lbl_maxInertia.setEnabled(is_enable)

        self.redraw_image()

    def chbx_area_handler(self):
        if self.chbx_area.isChecked():
            is_enable = True
        else:
            is_enable = False
        self.lbl_minArea_name.setEnabled(is_enable)
        self.sbx_minArea.setEnabled(is_enable)
        self.lbl_maxArea_name.setEnabled(is_enable)
        self.sbx_maxArea.setEnabled(is_enable)

        self.redraw_image()

    def redraw_image(self):
        if len(self.source_image_bgr) != 0:

            color_range = {"fruit": {
                "min": (self.sbx_minH.value(), self.sbx_minS.value(), self.sbx_minV.value()),
                "max": (self.sbx_maxH.value(), self.sbx_maxS.value(), self.sbx_maxV.value())}}

            sbd_params = cv2.SimpleBlobDetector_Params()
            sbd_params.filterByColor = False
            sbd_params.filterByCircularity = self.chbx_circularity.isChecked()
            if self.chbx_circularity.isChecked():
                sbd_params.maxCircularity = self.sld_maxCircularity.value() / 20
                sbd_params.minCircularity = self.sld_minCircularity.value() / 20
            sbd_params.filterByConvexity = self.chbx_convexity.isChecked()
            if self.chbx_convexity.isChecked():
                sbd_params.minConvexity = self.sld_minConvexity.value() / 20
                sbd_params.maxConvexity = self.sld_maxConvexity.value() / 20
            sbd_params.filterByInertia = self.chbx_inertia.isChecked()
            if self.chbx_inertia.isChecked():
                sbd_params.minInertiaRatio = self.sld_minInertia.value() / 20
                sbd_params.maxInertiaRatio = self.sld_maxInertia.value() / 20
            sbd_params.filterByArea = self.chbx_area.isChecked()
            if self.chbx_area.isChecked():
                sbd_params.minArea = self.sbx_minArea.value()
                sbd_params.maxArea = self.sbx_maxArea.value()

            keypoints, mask = tomato_detector.detect_in_image(self.source_image_bgr,
                                                              color_range,
                                                              self.chbx_contrast.isChecked(),
                                                              self.chbx_whiteBalance.isChecked(),
                                                              self.chbx_splitFruit.isChecked(),
                                                              sbd_params)

            result_image_bgr = cv2.drawKeypoints(self.source_image_bgr, keypoints["fruit"], np.array([]), (255, 0, 0),
                                                 cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

            resized_image_bgr = self.resize_image_for_frame(result_image_bgr, self.lbl_image.width(),
                                                            self.lbl_image.height())
            self.lbl_image.setPixmap(QPixmap.fromImage(
                QImage(resized_image_bgr.data, resized_image_bgr.shape[1], resized_image_bgr.shape[0],
                       resized_image_bgr.strides[0], QImage.Format_BGR888)))

    @staticmethod
    def resize_image_for_frame(image, frame_width, frame_height):
        image_width = image.shape[1]
        image_height = image.shape[0]

        if image_height > frame_height or image_width > frame_width:
            width_diff = image_width / frame_width
            height_diff = image_height / frame_height
        else:
            width_diff = frame_width / image_width
            height_diff = frame_height / image_height

        if width_diff > height_diff:
            return cv2.resize(image, (round(image_width / width_diff), round(image_height / width_diff)))
        else:
            return cv2.resize(image, (round(image_width / height_diff), round(image_height / height_diff)))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
