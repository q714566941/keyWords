import sys
from PyQt5.QtWidgets import QApplication
from keyword_selector import KeywordSelector

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KeywordSelector()
    window.show()
    sys.exit(app.exec_())
