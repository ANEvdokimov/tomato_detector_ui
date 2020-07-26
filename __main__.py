from PyQt5 import QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QCameraInfo
import main_window
import sys
import cv2
import numpy as np
import json
import tomato_detector
from settings import Settings
from settings_encoder import SettingsEncoder


class MainWindow(QtWidgets.QMainWindow, main_window.Ui_MainWindow):
    source_image_bgr = None
    vc = None

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setFixedSize(847, 749)

        self.rbtn_input_group = QtWidgets.QButtonGroup()
        self.rbtn_input_group.addButton(self.rbtn_camera)
        self.rbtn_input_group.addButton(self.rbtn_image)

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
        self.btn_saveSettings.clicked.connect(self.btn_save_settings_handler)

        self.rbtn_camera.clicked.connect(self.rbtn_input_handler)
        self.rbtn_image.clicked.connect(self.rbtn_input_handler)

        self.btn_catch.clicked.connect(self.btn_catch_handler)
        self.btn_continue.clicked.connect(self.btn_continue_handler)

        self.rbtn_input_handler()
        cameras = QCameraInfo.availableCameras()
        for camera in cameras:
            self.cmbx_cameras.addItem(camera.description())
        self.camera_id = 0

        self.cmbx_cameras.currentIndexChanged.connect(self.cmbx_cameras_handler)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_frame)

        self.load_settings()

    def open_camera(self):
        self.vc = cv2.VideoCapture(self.camera_id)

        if not self.vc.isOpened():
            msgBox = QtWidgets.QMessageBox()
            msgBox.setText("Ошибка при открытии камеры.")
            msgBox.exec_()
            return

        self.timer.start(int(1000. / 24))

    def stop_camera(self):
        if self.vc is not None:
            self.timer.stop()
            self.vc.release()

    def next_frame(self):
        rval, frame = self.vc.read()
        self.source_image_bgr = frame
        frame_resized = self.resize_image_for_frame(frame, self.lbl_image.width(), self.lbl_image.height())
        self.lbl_image.setPixmap(
            QPixmap.fromImage(QImage(frame_resized.data, frame_resized.shape[1], frame_resized.shape[0],
                                     frame_resized.strides[0], QImage.Format_BGR888)))

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

    def btn_save_settings_handler(self):
        self.save_settings()

    def save_settings(self):
        settings = Settings(
            self.sbx_minH.value(),
            self.sbx_minS.value(),
            self.sbx_minV.value(),
            self.sbx_maxH.value(),
            self.sbx_maxS.value(),
            self.sbx_maxV.value(),
            self.chbx_whiteBalance.isChecked(),
            self.chbx_contrast.isChecked(),
            self.chbx_circularity.isChecked(),
            self.sld_minCircularity.value() / 20,
            self.sld_maxCircularity.value() / 20,
            self.chbx_convexity.isChecked(),
            self.sld_minConvexity.value() / 20,
            self.sld_maxConvexity.value() / 20,
            self.chbx_inertia.isChecked(),
            self.sld_minInertia.value() / 20,
            self.sld_maxInertia.value() / 20,
            self.chbx_area.isChecked(),
            self.sbx_minArea.value(),
            self.sbx_maxArea.value(),
            self.chbx_splitFruit.isChecked()
        )

        with open("settings.json", "w") as file:
            file.write(SettingsEncoder().encode(settings))

        message_box = QtWidgets.QMessageBox()
        message_box.setText("Настройки успешно сохранены")
        message_box.setWindowTitle("Статус сохранения")
        message_box.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message_box.exec()

    def load_settings(self):
        try:
            with open("settings.json", "r") as file:
                settings = Settings(**json.load(file))

                self.sbx_minH.setValue(settings.minH)
                self.sbx_minS.setValue(settings.minS)
                self.sbx_minV.setValue(settings.minV)
                self.sbx_maxH.setValue(settings.maxH)
                self.sbx_maxS.setValue(settings.maxS)
                self.sbx_maxV.setValue(settings.maxV)
                self.chbx_whiteBalance.setChecked(settings.whiteBalance)
                self.chbx_contrast.setChecked(settings.contrast)
                self.chbx_circularity.setChecked(settings.filterByCircularity)
                self.sld_minCircularity.setValue(int(settings.minCircularity * 20))
                self.sld_maxCircularity.setValue(int(settings.maxCircularity * 20))
                self.chbx_convexity.setChecked(settings.filterByConvexity)
                self.sld_minConvexity.setValue(int(settings.minConvexity * 20))
                self.sld_maxConvexity.setValue(int(settings.maxConvexity * 20))
                self.chbx_inertia.setChecked(settings.filterByInertia)
                self.sld_minInertia.setValue(int(settings.minInertia * 20))
                self.sld_maxInertia.setValue(int(settings.maxInertia * 20))
                self.chbx_area.setChecked(settings.filterByArea)
                self.sbx_minArea.setValue(settings.minArea)
                self.sbx_maxArea.setValue(settings.maxArea)
                self.chbx_splitFruit.setChecked(settings.splitFruit)

                self.chbx_circularity_handler()
                self.chbx_convexity_handler()
                self.chbx_inertia_handler()
                self.chbx_area_handler()

        except FileNotFoundError:
            pass

    def rbtn_input_handler(self):
        if self.rbtn_image.isChecked():
            self.cmbx_cameras.setEnabled(False)
            self.btn_catch.setEnabled(False)
            self.btn_continue.setEnabled(False)
            self.lbl_fileName.setEnabled(True)
            self.btn_open.setEnabled(True)
            self.stop_camera()
        elif self.rbtn_camera.isChecked():
            self.cmbx_cameras.setEnabled(True)
            self.btn_catch.setEnabled(True)
            self.btn_continue.setEnabled(True)
            self.lbl_fileName.setEnabled(False)
            self.btn_open.setEnabled(False)
            self.open_camera()

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

    def btn_catch_handler(self):
        self.stop_camera()
        self.redraw_image()

    def btn_continue_handler(self):
        if not self.vc.isOpened():
            self.open_camera()
            self.source_image_bgr = None

    def cmbx_cameras_handler(self):
        self.camera_id = self.cmbx_cameras.currentIndex()
        self.stop_camera()
        self.open_camera()

    def redraw_image(self):
        if self.source_image_bgr is not None and not self.vc.isOpened():

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

            self.output_keypoints_text(keypoints["fruit"])

    def output_keypoints_text(self, keypoints):
        self.pte_output.clear()
        self.pte_output.appendPlainText("Количество найденных объектов: " + str(len(keypoints)))

        index = 0
        for fruit in keypoints:
            self.pte_output.appendPlainText("")
            self.pte_output.appendPlainText("Index: " + str(index))
            self.pte_output.appendPlainText(
                "Расположение на изображении: " + str(round(fruit.pt[0])) + ":" + str(round(fruit.pt[1])))
            index += 1

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
