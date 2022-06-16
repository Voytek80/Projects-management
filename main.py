import sys
import sqlite3;
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtWidgets import *
import data_management
from datetime import datetime


start_date = 1
end_date = 2
project_nr = 6     # rowne 1 gdy przyklady usuniete
colors = ['yellow', 'white', 'blue', 'red', 'pink', 'purple']

baza = data_management.Database('database')
baza.drop_table('projects')
baza.drop_table('employees')
baza.drop_table('tasks')

baza.create_table("employees(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, department text, position text, tasks int)")
baza.create_table("projects(id INTEGER PRIMARY KEY AUTOINCREMENT, title text, description text, startDate text, finishDate text, urgency int, allTasks int, doneTasks int)")
baza.create_table("tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, projectId int, employe int, title text, description text, urgency int, status int, startDate text, finishDate text, creationDate text)")




class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class Button(QPushButton):
    def __init__(self, text):
        super(Button, self).__init__()
        self.setText(text)
    def Clicked(self):
        MainWindow.printTable(str(self.text()))


class MainWindow(QMainWindow):
    lista = []
    rows = []
    def add_project(self):
        baza.addProject(('Project1', 'Project one long description', datetime.now(), '', 1, 0, 0))
        self.printTable('projects') 

    def delete_project(self):
        baza.addProject(('Project1', 'Project one long description', datetime.now(), '', 1, 0, 0))
        self.printTable('projects') 
    
    def add_task(self):
        baza.addTask(('Task1', 'Task description', datetime.now(), '', 1, 0, 0))
    
    def add_employe(self):
        baza.addEmploye(('Jan', 'Kowalski', 'IT', 'Dev'))
    
    def printTable(self, tableName):
        self.rows = baza.selectTable(tableName)  
        self.refreshList(self.rows)      
        

    def refreshList(self, rows):
        self.lista.clear()
        for row in rows:
            self.lista.addItem(QListWidgetItem(str(row)))
        self.lista.repaint()
    
        
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Projects Management")
        self.setGeometry(150, 100, 900, 600)

        global tabs, tab1, tab2, left_panel, right_panel
        tabs = QTabWidget()
        tab1 = QTabWidget() #Progress Tab
        tab1_2 = QTabWidget() #Progress Tab Single Project
        tab2 = QTabWidget() #Project Management tab
        tab2_2 = QTabWidget() #Project Management tab
        tab3 = QTabWidget() #Employes tab
        
           
        
        tabs.setTabPosition(QTabWidget.North)
        tabs.setMovable(True)
        tabs.addTab(tab1, "Main")
        tabs.addTab(tab1_2, "Main2")
        tabs.addTab(tab2, "Add Project")
        tabs.addTab(tab2_2, "Add Project2")
        tabs.addTab(tab3, "Użytkownicy")
        
        
        projects = QHBoxLayout()
        projectsLeft = QVBoxLayout()
        projectsRight = QStackedLayout() 
        

        projectLayout = QVBoxLayout()
        projectLayout.setAlignment(Qt.AlignHCenter)
        projectLayout.addWidget(QLabel("PROJECTS MANAGEMENT"))
        projectLayout.addWidget(QPushButton('Press Me'))

        employesLayout = QVBoxLayout()
        employesLayout.setAlignment(Qt.AlignCenter)
        employesLayout.addWidget(QLabel("EMPLOYES MANAGEMENT"))
        employesLayout.addWidget(QPushButton("some button"))

        tasksLayout = QVBoxLayout()     
        tasksLayout.setAlignment(Qt.AlignCenter)
        tasksLayout.addWidget(QLabel("TASKS MANAGEMENT"))
        for x in range(5):
            tasksLayout.addWidget(QLabel("Task"+ str(x)))

        projectWidget = QWidget()
        employesWidget = QWidget()
        tasksWidget = QWidget()

        projectWidget.setLayout(projectLayout)
        employesWidget.setLayout(employesLayout)
        tasksWidget.setLayout(tasksLayout)
                
        projectsRight.addWidget(projectWidget)
        projectsRight.addWidget(employesWidget)
        projectsRight.addWidget(tasksWidget)
        
        buttonProject = QPushButton('Project')
        buttonProject.clicked.connect(lambda: projectsRight.setCurrentIndex(0))
        buttonEmployes = QPushButton('Employes')
        buttonEmployes.clicked.connect(lambda: projectsRight.setCurrentIndex(1))
        buttonTasks = QPushButton('Tasks')
        buttonTasks.clicked.connect(lambda: projectsRight.setCurrentIndex(2))
        


        projectsLeft.setAlignment(Qt.AlignLeft)
        projectsLeft.addWidget(buttonProject)
        projectsLeft.addWidget(buttonEmployes)
        projectsLeft.addWidget(buttonTasks)
 

        buttonAddProject = QPushButton('Add Project')
        buttonAddProject.clicked.connect(lambda: self.add_project())

        buttonAddEmploye = QPushButton('Add Employe')
        buttonAddEmploye.clicked.connect(lambda: self.printTable('projects'))

        buttonProjects = Button('projects')
        buttonProjects.clicked.connect(buttonProjects.Clicked)
        

        buttonAddTask = QPushButton('Add Task')
        buttonAddTask.clicked.connect(lambda: self.add_task())

        projects.addLayout(projectsLeft)
        projects.addLayout(projectsRight)
        tab2_2.setLayout(projects)     
        tempLayout = QHBoxLayout()
        self.lista = QListWidget() 
        tempLayout.addWidget(self.lista)
        tempLayout.addWidget(buttonAddProject)
        tempLayout.addWidget(buttonAddEmploye)
        tempLayout.addWidget(buttonProjects)
        tab1_2.setLayout(tempLayout)
        
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