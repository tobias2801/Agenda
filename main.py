# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QApplication
from ui_agenda import AgendaMainWindow

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    ventana = AgendaMainWindow()
    ventana.show()

    sys.exit(app.exec_())