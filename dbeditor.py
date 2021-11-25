import sqlite3
import os 

class EditDB():
    def __init__(self, filename="page.db"):
        self.dbfilename = os.path.abspath(filename)
        self.db = sqlite3.connect(self.dbfilename)
        c = self.db.cursor()
        c.execute(
        """CREATE TABLE IF NOT EXISTS pages( 
                pid             INTEGER PRIMARY KEY, 
                name            TEXT UNIQUE, 
                description     TEXT, 
                options         BLOB 
                );""")
        self.db.commit()
        
        c.close()
################
# ADDING 
################
    def addpage(self, pageid, pagetitle, pagedescription):
        c = self.db.cursor()
        c.execute(
                """INSERT INTO pages (pid, name, description, options) VALUES(?,?,?,0) """ % (pageid, pagetitle, pagedescription))
        self.db.commit()
        c.close()

    def addpath(self, pageid, pathid, pathname, pathdest):
        c = self.db.cursor()
        c.execute(
                """INSERT INTO paths_%s (path_id, name, source_id, dest_id) VALUES(?,?,?,?) """ % (pageid), (pathid, pathname, pageid, pathdest))
        self.db.commit()
        c.close()

    def create_path_table(self, pageid):
        c = self.db.cursor()
        c.execute(
                """CREATE TABLE IF NOT EXISTS path_%s (
                path_id             INTEGER PRIMARY KEY,
                name                TEXT,
                source_id           INTEGER,
                dest_id             INTEGER)""" % (pageid))
        self.db.commit()
        c.close()
    
    def gen_path_tables(self):
        c = self.db.cursor()
        pages = c.execute("SELECT pid FROM pages;")
        pages = pages.fetchall()
        for i in pages:
            self.create_path_table(i[0])
        c.close()

##############
# EDITING
##############

    def editpage(self, field, new_value, pageid):
        c = self.db.cursor()
        c.execute("""UPDATE pages
        SET %s = %s
        WHERE pid = ?""" % (field,new_value),(pageid))
        self.db.commit()
        c.close()

    def editpath(self, pageid, field, new_value, pathid):
        c = self.db.cursor()
        c.execute("""UPDATE paths_%s 
        SET %s = %s
        WHERE pathid = ?""" % (pageid, field, new_value), (pathid))

##############
# DISPLAY
##############


    def display(self,table):
        c = self.db.cursor()
        entries = c.execute("SELECT * FROM %s;" % (table))
        entries = entries.fetchall()
        c.close()
        print('\n'.join([str(i) for i in entries]))
edit = EditDB()
