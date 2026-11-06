import sys

from PyQt6.QtWidgets import QApplication

from database.init_db import initialize_database
from ui.dashboard import Dashboard


def main():

    initialize_database()
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()