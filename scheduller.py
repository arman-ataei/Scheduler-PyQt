# main.py
import sys
from PyQt5.QtWidgets import QApplication
from model import DatabaseModel
from view import MainView
from controller import MainController

def main():
    app = QApplication(sys.argv)
    model = DatabaseModel()
    view = MainView()
    controller = MainController(model, view)
    view.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
