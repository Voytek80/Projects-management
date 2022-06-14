import sys
import sqlite3;
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtWidgets import *
import data_management


start_date = 1
end_date = 2
project_nr = 6     # rowne 1 gdy przyklady usuniete
colors = ['yellow', 'white', 'blue', 'red', 'pink', 'purple']

Baza = data_management.Database('banana')



class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projects Management")
        self.setGeometry(150, 100, 900, 600)

        global tabs, tab1, tab2, left_panel, right_panel
        tabs = QTabWidget()
        tab1 = QTabWidget()
        tab2 = QTabWidget()
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        tabs.addTab(tab1, "Main")
        tabs.addTab(tab2, "Add Project")
        layout = QHBoxLayout()
        left_panel = QGridLayout()
        header = QLabel("Project name")
        font = QFont("Times New Roman", 15, QFont.Bold)
        header.setFont(font)
        left_panel.addWidget(header, 0, 1)
        left_panel.addWidget(QLabel("                                    "), 0, 1)
        right_panel = QGridLayout()
        right_panel.setSpacing(1)

        for i in range(1,19):
            left_panel.addWidget(QLabel(" "), i, 0)

        for rows in range(20):
            for columns in range(30):
                right_panel.setColumnStretch(columns, 2)
                right_panel.setRowStretch(rows, 1)
                right_panel.addWidget(QLabel(str(columns+1)), 0, columns)
                right_panel.addWidget(Color('grey'), rows+1, columns)

        left_panel.addWidget(QLabel("Jakiś tam projekt nr 1"), 1, 0)     #
        for i in range(10):                                              # do usuniecia, tylko przyklad
            right_panel.addWidget(Color('green'), 1, i)                  #

        left_panel.addWidget(QLabel("Projekt nr 2"), 2, 0)               #
        for i in range(5,15):                                            # do usuniecia, tylko przyklad
            right_panel.addWidget(Color('red'), 2, i)                    #

        left_panel.addWidget(QLabel("Projekt nr 3"), 4, 0)               #
        for i in range(3, 20):                                           # do usuniecia, tylko przyklad
            right_panel.addWidget(Color('blue'), 4, i)                   #

        left_panel.addWidget(QLabel("Projekt nr 4"), 5, 0)               #
        for i in range(4, 25):                                           # do usuniecia, tylko przyklad
            right_panel.addWidget(Color('purple'), 5, i)                 #

        layout.addLayout(left_panel)
        layout.addLayout(right_panel)

        tab1.setLayout(layout)

        lista_dni = []
        for i in range(1,31):
            lista_dni.append(str(i))

        self.combobox1 = QComboBox()
        self.combobox1.addItems(lista_dni)
        self.combobox2 = QComboBox()
        self.combobox2.addItems(lista_dni)
        self.button1 = QPushButton("Add Project")
        self.project_name = QLineEdit()


        layout2 = QGridLayout()
        layout2.addWidget(QLabel("Project name"), 0, 0)
        layout2.addWidget(QLabel("Start date"), 1, 0)
        layout2.addWidget(QLabel("End date"), 2, 0)
        layout2.addWidget(self.project_name, 0, 1)
        layout2.addWidget(self.combobox1, 1, 1)
        layout2.addWidget(self.combobox2, 2, 1)
        layout2.addWidget(self.button1, 1, 3)
        tab2.setLayout(layout2)

        self.button1.setCheckable(True)
        self.button1.clicked.connect(self.button_checked)
        self.combobox1.activated.connect(self.check_index1)
        self.combobox2.activated.connect(self.check_index2)
        self.setCentralWidget(tabs)




    def button_checked(self):
        if self.button1.isChecked():
            global start_date, end_date, project_name, tab1, layout1, project_nr
            display = self.project_name.text()
            left_panel.addWidget(QLabel(display), project_nr, 0)
            for i in range(start_date, end_date):
                right_panel.addWidget(Color(colors[project_nr-6]), project_nr, i)   # usunac -6 gdy przyklady projektow usuniete
            project_nr = project_nr + 1



    def check_index1(self, index):
        global start_date
        start_date = index

    def check_index2(self, index):
        global end_date
        end_date = index



app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()