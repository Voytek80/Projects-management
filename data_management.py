import sqlite3

class Database(object):
    def __init__(self, name):
        con = sqlite3.connect(name + '.db')
