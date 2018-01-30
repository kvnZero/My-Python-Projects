from main import QtWidgets, Ui_MainWindows
from datetime import datetime


if __name__=="__main__":
    import sys
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QMainWindow()
    ui=Ui_MainWindows()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
