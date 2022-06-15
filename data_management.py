import sqlite3

class Database(object):
    
    def __init__(self, name):
        self.con = sqlite3.connect(name + '.db')

    def create_table(self, sql):

        cursorObj = self.con.cursor()

        cursorObj.execute('CREATE TABLE if not exists ' + sql)

        self.con.commit()


    def drop_table(self, name):

        cursorObj = self.con.cursor()

        cursorObj.execute("drop table if exists " + name)

        self.con.commit()


    def addEmploye(self, entities):

        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO employees(name, department, position, tasks) VALUES(?, ?, ?, ?)', entities)
        
        self.con.commit()

    def addProject(self, entities):

        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO projects(title,description, startDate, finishDate, urgency, allTasks, doneTasks) VALUES(?, ?, ?, ?, ?, ?, ?)', entities)
        
        self.con.commit()

    def addTask(self, entities):

        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO tasks(projectId, employe, title, description, urgency, status, startDate, finishDate, creationDate) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', entities)
        
        self.con.commit()


    def selectEmploye(self, entities):

        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO employees(name, department, position) VALUES(?, ?, ?)', entities)
        
        self.con.commit()

    def selectProject(self, entities):

        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO projects(title,description, startDate, finishDate, urgency, allTasks, doneTasks) VALUES(?, ?, ?, ?, ?, ?, ?)', entities)
        
        self.con.commit()

    def selectTask(self, entities):

        cursorObj = self.con.cursor()
        cursorObj.execute('INSERT INTO tasks(projectId, employe, title, description, urgency, status, startDate, finishDate, creationDate) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', entities)
        
        self.con.commit()