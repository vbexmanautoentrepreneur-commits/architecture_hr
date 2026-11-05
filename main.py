import sys

from PyQt6.QtWidgets import QApplication
from ui.dashboard import Dashboard

app = QApplication(sys.argv)

window = Dashboard()

window.show()

sys.exit(app.exec())