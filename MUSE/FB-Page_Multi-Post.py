# -*- coding: utf-8 -*-
"""
@author: george chen(neural022)
"""

import sys
# import cv2 
import logging
from PyQt5 import QtWidgets, QtGui, QtCore

from utils.config import *
from utils.fbpy_graph_api import *
from utils import TextEditLogHandler
from utils import Ui_MainWindow, PostSettingDialog, PublishCheckDialog, GenerateLongLiveTokenForm



class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.APP_ID = ''
        self.APP_SECRET = ''
        self.USER_ACCESS_TOKEN = ''
        self.api_version =''

        self.load_api_version()
        self.long_live_token_form = GenerateLongLiveTokenForm(self)

        self.message = ""
        self.image = ""

        self.setAcceptDrops(True)
        self.long_live_token_button.clicked.connect(self.long_live_token)
        self.post_setting_button.clicked.connect(self.post_setting)
        self.upload_image_button.clicked.connect(self.upload_image_dialog)
        self.reset_button.clicked.connect(self.reset_ui)
        self.publish_post_button.clicked.connect(self.send_to_post)


        # Setting up logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        self.log_handler = TextEditLogHandler(self.execution_log_TextEdit)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(self.log_handler)
        self.logger.setLevel(logging.INFO)

    def load_api_version(self):
        config = Config("./config/config.json")
        self.api_version = config.load_config()['api_version']
        self.api_LineEdit.setText(self.api_version)

    def clear_image_preview(self):
        self.image_preview_label.clear()
        # self._movie.stop()

    def load_image_to_preview(self, image_path):
        self.image_preview_label.clear()
        # 檢查是否是 GIF
        if image_path.lower().endswith('.gif'):
            self._movie = QtGui.QMovie(image_path)  # 重新初始化 QMovie 對象
            self.image_preview_label.setMovie(self._movie)
            self._movie.start()
        else:
            image = QtGui.QPixmap(image_path)
            # 調整圖片大小以適應imagePreviewLabel，但保持圖片的寬高比
            image = image.scaled(self.image_preview_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.image_preview_label.setPixmap(image)


    def dragEnterEvent(self, event):
        # 只接受拖放的文件
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        # 獲取文件路徑
        file_path = event.mimeData().urls()[0].toLocalFile()
        # 預覽圖片
        self.load_image_to_preview(file_path)
        # 更新路徑文字框
        self.image_path_lineEdit.setText(file_path)


    def upload_image_dialog(self):
        image_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇圖片", "", "圖片檔案 (*.png *.jpg *.jpeg *.bmp *.gif);;所有文件 (*)")

        # 如果user選擇或了有效路徑，則將該路徑設置到imagePathLineEdit文本框上
        if image_path:
            self.image_path_lineEdit.setText(image_path)
            self.load_image_to_preview(image_path)
        # 如果user選擇或取消了有效路徑
        else:
            self.image_path_lineEdit.clear()
            self.clear_image_preview()


    def long_live_token(self):
        self.long_live_token_form.show()

    def post_setting(self):
        self.USER_ACCESS_TOKEN = self.token_textEdit.toPlainText().strip()
        self.api_version = self.api_LineEdit.text().strip()
        if self.USER_ACCESS_TOKEN:
            try:
                user_api = FacebookUserAPI(self.USER_ACCESS_TOKEN, api_version=self.api_version)
                self.pages_data = [ page_data for page_data in user_api.get_managed_pages() ]
                self.setting_dialog = PostSettingDialog(self)
                self.setting_dialog.populate_table(self.pages_data)
                self.setting_dialog.show()
            except FacebookError as e:
                self.logger.error(f"Error occurred while interacting with Facebook: {e}")
        else:
            self.logger.info(f"無存取權限，USER ACCESS TOKEN不能為空，請至設至設定TOKEN。")

    def send_to_post(self):
        self.USER_ACCESS_TOKEN = self.token_textEdit.toPlainText().strip()
        self.api_version = self.api_LineEdit.text().strip()
        if self.USER_ACCESS_TOKEN:
            if hasattr(self, 'setting_dialog') and len(self.setting_dialog.target_page_ids) > 0:
                    self.publish_check_dialog = PublishCheckDialog(
                        self.setting_dialog.target_page_ids, 
                        self.pages_data, self.post_plainText_edit.toPlainText(), 
                        self.image_path_lineEdit.text(),
                        self.logger,
                        self.api_version,
                        self
                    )
                    self.publish_check_dialog.show()
            else:
                self.logger.info(f"請先選擇發布對象")
        else:
            self.logger.info(f"無存取權限，USER ACCESS TOKEN不能為空，請至設至設定TOKEN。")

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyle('Fusion')
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())