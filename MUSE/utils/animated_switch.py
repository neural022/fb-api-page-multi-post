from PyQt5.QtCore import QPropertyAnimation, QPoint, pyqtSignal
from PyQt5.QtWidgets import QWidget, QPushButton

class AnimatedSwitch(QPushButton):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 20)  # 設置控件的大小
        self._circle = QPushButton(self)
        self._circle.setFixedSize(18, 18)  # 設置內部圓形按鈕的大小
        self._circle.setStyleSheet("background-color: white; border-radius: 9px;")
        self._circle.move(1, 1)  # 初始位置
        self._active = False
        self.setStyleSheet("background-color: lightgray; border-radius: 10px;")

        self._animation = QPropertyAnimation(self._circle, b'pos')
        self._animation.setDuration(100)  # 動畫持續時間

        self.clicked.connect(self.animate)

    def animate(self):
        self._active = not self._active
        end_x = 21 if self._active else 1  # 按鈕在開啟和關閉狀態下的位置
        self._animation.setStartValue(self._circle.pos())
        self._animation.setEndValue(QPoint(end_x, 1))
        self._animation.start()
        self.toggled.emit(self._active)
        self.updateStyle()

    def updateStyle(self):
        if self._active:
            self.setStyleSheet("background-color: rgb(200, 200, 255); border-radius: 10px;")  # 激活狀態下的背景顏色
        else:
            self.setStyleSheet("background-color: lightgray; border-radius: 10px;")  # 非激活狀態下的背景顏色
