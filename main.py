from PyQt6.QtWidgets import *
from main_window import Main
import sys

def main():
    APP = QApplication(sys.argv)
    widget = QStackedWidget()
    main = Main()
    # widget.addWidget(main)
    try:
        sys.exit(APP.exec())
    except:
        print("Exiting")

if __name__ == '__main__':
    main()