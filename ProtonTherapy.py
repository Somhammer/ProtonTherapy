import os, sys
import datetime

from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

from src.variables import *

sys.path.append(BASE_PATH)

from src.data import *
from src.mainwindow import MainWindow

if __name__ == '__main__':
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)

    ex = MainWindow()
    sys.exit(app.exec())
