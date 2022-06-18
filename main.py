import sys
from PySide6.QtGui import QPalette, QColor, QFont
from PySide6.QtCore import Qt
from PySide6.QtSql import *
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import *
from datetime import datetime
import plotly.figure_factory as ff
import numpy


def sql_query(query):
    q = QSqlQuery()
    q.exec(query)


def sql_fetch(query):
    q = QSqlQuery()
    q.exec(query)
    data = []
    while q.next():
        data_line = [q.record().value("name"), q.record().value("start_date"), q.record().value("finish_date"),
                     q.record().value("status")]
        data.append(data_line)
    return data


def sql_fetch_one(table_name, attribute_name):
    q = QSqlQuery()
    q.exec(f'SELECT {attribute_name} FROM {table_name}')
    data = []
    while q.next():
        data.append(q.record().value(attribute_name))
    return data


def create_connection():
    con = QSqlDatabase.addDatabase("QSQLITE")
    con.setDatabaseName("database.sqlite")
    if not con.open():
        QMessageBox.critical(
            None,
            "QTableView Example - Error!",
            "Database Error: %s" % con.lastError().databaseText(),
        )
        return False
    return True


def setup_database():
    sql_query("""        
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                description VARCHAR(500),
                start_date VARCHAR(50),
                finish_date VARCHAR(40),
                project_leader_id INTEGER,
                FOREIGN KEY (project_leader_id) 
                    REFERENCES employees (id)        
            )
            """)

    sql_query("""        
            CREATE TABLE employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40),
                surname VARCHAR(40), 
                hire_date VARCHAR(50),
                tasks INTEGER
            )
            """)

    sql_query("""        
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                description VARCHAR(500),
                start_date VARCHAR(40),
                finish_date VARCHAR(40),
                status VARCHAR(20),
                employee_id INTEGER,
                project_id INTEGER,
                FOREIGN KEY (project_id) 
                    REFERENCES projects (id),
                FOREIGN KEY (employee_id) 
                    REFERENCES employees (id)

            )
            """)


class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class Label(QLabel):
    def __init__(self, text, alignment):
        super(Label, self).__init__()
        self.setText(text)
        self.setAlignment(alignment)


class PlotBrowser(QWidget):
    def __init__(self):
        super(PlotBrowser, self).__init__()
        self.browser = QWebEngineView(self)
        self.button_refresh = QPushButton('Refresh')
        self.button_refresh.clicked.connect(lambda: self.refresh())
        self.combobox = QComboBox()
        self.combobox.currentIndexChanged.connect(lambda: self.refresh())
        vlayout = QVBoxLayout(self)
        vlayout.addWidget(self.combobox)
        vlayout.addWidget(self.browser)
        vlayout.addWidget(self.button_refresh)
        fetch_projects = sql_fetch_one('projects', 'name')
        for project_name in fetch_projects:
            self.combobox.addItem(project_name)
        self.refresh()

    def refresh(self):
        df = []
        fetch_data = sql_fetch(f"SELECT name, start_date, finish_date, status FROM tasks WHERE project_id = {self.combobox.currentIndex()};")
        if fetch_data:
            for name, start, finish, status in fetch_data:
                if finish == '': finish = datetime.now()
                df.append(dict(Task=name, Start=start, Finish=finish, Resource=status))

            colors = {'Not Started': 'rgb(220, 0, 0)',
                      'Incomplete': (1, 0.9, 0.16),
                      'Complete': 'rgb(0, 255, 100)'}

            fig = ff.create_gantt(df, colors=colors, index_col='Resource', show_colorbar=True,
                                  group_tasks=True)

            self.browser.setHtml(fig.to_html(include_plotlyjs='cdn'))


class TableView(QTableView):
    def __init__(self, table_name, collumn_names):
        super(TableView, self).__init__()
        self.table_name = table_name
        self.column_names = collumn_names
        self.model = QSqlTableModel(self)
        self.setup_model(self.table_name, self.column_names)
        self.setModel(self.model)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def setup_model(self, table_name, attributes):
        self.model.setTable(table_name)
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)
        for i in range(len(attributes)):
            self.model.setHeaderData(i, Qt.Horizontal, attributes[i])
        self.model.select()

    def submit(self):
        self.model.submitAll()

    def refresh(self):
        self.model.select()


class TableViewProject(TableView):
    def add(self, data):
        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """
            INSERT INTO projects (
                name,
                description,
                start_date,
                finish_date,
                project_leader_id
            )
            VALUES (?, ?, ?, ?, ?)
            """
        )
        for i in range(len(data)):
            insertDataQuery.addBindValue(data[i])
        print(insertDataQuery.exec())
        self.model.select()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def delete(self, id):
        row = id.row()
        index = self.model.data(self.model.index(row, 0))
        sql_query(f"DELETE FROM projects WHERE id = {index};")
        self.model.select()
        # self.model.setQuery(QSqlQuery("SELECT name FROM projects;"))
        self.model.selectRow(row + 1)


class TableViewEmployees(TableView):
    def add(self, data):
        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """
            INSERT INTO employees (
                name,
                surname,
                hire_date,
                tasks
            )
            VALUES (?, ?, ?, ?)
            """
        )
        print(data)
        for i in data:
            insertDataQuery.addBindValue(i)
        insertDataQuery.exec()
        self.model.select()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def delete(self, id):
        row = id.row()
        index = self.model.data(self.model.index(row, 0))
        sql_query(f"DELETE FROM employees WHERE id = {index};")
        self.model.select()
        self.model.selectRow(row + 1)


class TableViewTasks(TableView):
    def add(self, data):
        insertDataQuery = QSqlQuery()
        insertDataQuery.prepare(
            """
            INSERT INTO tasks (
                name,
                description,
                start_date,
                finish_date,
                status,
                employee_id,
                project_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
        )
        for i in range(len(data)):
            insertDataQuery.addBindValue(data[i])
        insertDataQuery.exec()
        self.model.select()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def delete(self, id):
        row = id.row()
        index = self.model.data(self.model.index(row, 0))
        sql_query(f"DELETE FROM tasks WHERE id = {index};")
        self.model.select()
        self.model.selectRow(row + 1)


class TextField(QWidget):
    def __init__(self, text):
        super(TextField, self).__init__()
        self.label = Label(text, Qt.AlignCenter)
        self.field = QLineEdit()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.field)
        self.setLayout(self.layout)


class DataField(QWidget):
    def __init__(self, text):
        super(DataField, self).__init__()
        self.label = Label(text, Qt.AlignCenter)
        self.field = QDateEdit()
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.field)
        self.setLayout(self.layout)


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Projects Management")
        self.setGeometry(150, 100, 1000, 800)

        primary_widget = MainWidget()
        projects = QVBoxLayout()

        projects_left = QHBoxLayout()
        projects_right = QStackedLayout()

        project_layout = QVBoxLayout()
        project_layout.setAlignment(Qt.AlignHCenter)
        project_layout.addWidget(Label("PROJECTS MANAGEMENT", Qt.AlignCenter))
        project_table = TableViewProject('projects', ('ID', 'Name', 'Description', 'Start Date',
                                                      'Finish Date', 'Leader'))
        project_layout.addWidget(project_table)
        projects_layout_add = QHBoxLayout()
        add_name = TextField('Name: ')
        projects_layout_add.addWidget(add_name)
        add_description = TextField('Description: ')
        projects_layout_add.addWidget(add_description)
        add_leader = TextField('Leader: ')
        projects_layout_add.addWidget(add_leader)
        project_layout_bottom = QHBoxLayout()
        project_layout_bottom.setAlignment(Qt.AlignCenter)
        btn_add_project = QPushButton('Add')
        btn_add_project.clicked.connect(lambda: project_table.add((add_name.field.text(), add_description.field.text(),
                                                                   str(datetime.now()), ' ', 1)))
        btn_delete_project = QPushButton('Delete')
        btn_delete_project.clicked.connect(lambda: project_table.delete(project_table.currentIndex()))
        btn_save_project = QPushButton('Save')
        btn_save_project.clicked.connect(lambda: project_table.submit())
        btn_refresh_project = QPushButton('Refresh')
        btn_refresh_project.clicked.connect(lambda: project_table.refresh())

        project_layout_bottom.addWidget(btn_add_project)
        project_layout_bottom.addWidget(btn_delete_project)
        project_layout_bottom.addWidget(btn_save_project)
        project_layout_bottom.addWidget(btn_refresh_project)

        pla = QWidget()
        pla.setLayout(projects_layout_add)
        plb = QWidget()
        plb.setLayout(project_layout_bottom)
        project_layout.addWidget(pla)
        project_layout.addWidget(plb)

        employees_layout = QVBoxLayout()
        employees_layout.setAlignment(Qt.AlignCenter)

        employees_table = TableViewEmployees('employees', ('ID', 'Name', "Surname", 'Hired Date', 'Tasks'))
        employees_layout.addWidget(Label("EMPLOYEES MANAGEMENT", Qt.AlignCenter))
        employees_layout.addWidget(employees_table)

        employees_layout_add = QHBoxLayout()
        add_employee_name = TextField('Name: ')
        employees_layout_add.addWidget(add_employee_name)
        add_employee_surname = TextField('Surname: ')
        employees_layout_add.addWidget(add_employee_surname)
        add_hire_date = DataField('Hire Date: ')
        employees_layout_add.addWidget(add_hire_date)

        employees_layout_bottom = QHBoxLayout()
        employees_layout_bottom.setAlignment(Qt.AlignCenter)
        btn_add_employees = QPushButton('Add')
        btn_add_employees.clicked.connect(lambda: employees_table.add((add_employee_name.field.text(),
                                                                       add_employee_surname.field.text(),
                                                                       add_hire_date.field.text(), 0)))
        btn_delete_employees = QPushButton('Delete')
        btn_delete_employees.clicked.connect(lambda: employees_table.delete(employees_table.currentIndex()))
        btn_save_employees = QPushButton('Save')
        btn_save_employees.clicked.connect(lambda: employees_table.submit())
        btn_refresh_employees = QPushButton('Refresh')
        btn_refresh_employees.clicked.connect(lambda: employees_table.refresh())

        employees_layout_bottom.addWidget(btn_add_employees)
        employees_layout_bottom.addWidget(btn_delete_employees)
        employees_layout_bottom.addWidget(btn_save_employees)
        employees_layout_bottom.addWidget(btn_refresh_employees)
        ela = QWidget()
        ela.setLayout(employees_layout_add)
        elb = QWidget()
        elb.setLayout(employees_layout_bottom)
        employees_layout.addWidget(ela)
        employees_layout.addWidget(elb)

        tasks_layout = QVBoxLayout()
        tasks_layout.setAlignment(Qt.AlignHCenter)
        tasks_layout.addWidget(Label("TASKS MANAGEMENT", Qt.AlignCenter))
        tasks_table = TableViewTasks('tasks', ('ID', 'Name', 'Description', 'Start Date', 'Finish Date',
                                               'Status', 'Employee', 'Project'))
        tasks_layout.addWidget(tasks_table)
        tasks_layout_add = QHBoxLayout()
        add_task_name = TextField('Name: ')
        tasks_layout_add.addWidget(add_task_name)
        add_task_description = TextField('Description: ')
        tasks_layout_add.addWidget(add_task_description)
        add_task_status = TextField('Status: ')
        tasks_layout_add.addWidget(add_task_status)
        add_task_employee = TextField('Employee: ')
        tasks_layout_add.addWidget(add_task_employee)
        add_task_project = TextField('Project: ')
        tasks_layout_add.addWidget(add_task_project)
        tasks_layout_bottom = QHBoxLayout()
        tasks_layout_bottom.setAlignment(Qt.AlignCenter)
        btn_add_tasks = QPushButton('Add')
        btn_add_tasks.clicked.connect(lambda: tasks_table.add((add_task_name.field.text(),
                                                               add_task_description.field.text(),
                                                               str(datetime.now()), '',
                                                               add_task_status.field.text(),
                                                               2, 1)))
        btn_delete_tasks = QPushButton('Delete')
        btn_delete_tasks.clicked.connect(lambda: tasks_table.delete(tasks_table.currentIndex()))
        btn_save_tasks = QPushButton('Save')
        btn_save_tasks.clicked.connect(lambda: tasks_table.submit())
        btn_refresh_tasks = QPushButton('Refresh')
        btn_refresh_tasks.clicked.connect(lambda: tasks_table.refresh())

        tasks_layout_bottom.addWidget(btn_add_tasks)
        tasks_layout_bottom.addWidget(btn_delete_tasks)
        tasks_layout_bottom.addWidget(btn_save_tasks)
        tasks_layout_bottom.addWidget(btn_refresh_tasks)

        tla = QWidget()
        tla.setLayout(tasks_layout_add)
        tlb = QWidget()
        tlb.setLayout(tasks_layout_bottom)
        tasks_layout.addWidget(tla)
        tasks_layout.addWidget(tlb)

        project_widget = QWidget()
        employees_widget = QWidget()
        tasks_widget = QWidget()
        gantt_widget = PlotBrowser()

        project_widget.setLayout(project_layout)
        employees_widget.setLayout(employees_layout)
        tasks_widget.setLayout(tasks_layout)

        projects_right.addWidget(gantt_widget)
        projects_right.addWidget(project_widget)
        projects_right.addWidget(employees_widget)
        projects_right.addWidget(tasks_widget)

        btn_gantt = QPushButton('Gantt Chart')
        btn_gantt.clicked.connect(lambda: projects_right.setCurrentIndex(0))
        btn_projects = QPushButton('Project')
        btn_projects.clicked.connect(lambda: projects_right.setCurrentIndex(1))
        btn_employees = QPushButton('Employes')
        btn_employees.clicked.connect(lambda: projects_right.setCurrentIndex(2))
        btn_tasks = QPushButton('Tasks')
        btn_tasks.clicked.connect(lambda: projects_right.setCurrentIndex(3))

        projects.addLayout(projects_left)
        projects.addLayout(projects_right)
        primary_widget.setLayout(projects)

        projects_left.setAlignment(Qt.AlignCenter)
        projects_left.addWidget(btn_gantt)
        projects_left.addWidget(btn_projects)
        projects_left.addWidget(btn_employees)
        projects_left.addWidget(btn_tasks)

        self.setCentralWidget(primary_widget)


app = QApplication(sys.argv)

if not create_connection():
    sys.exit(1)

setup_database()

window = MainWindow()
window.show()
app.exec()
