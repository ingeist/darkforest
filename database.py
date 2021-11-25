import npyscreen
import sqlite3 
import os

class Database(object):
    def __init__(self, filename="page.db"):
        self.dbfilename = os.path.abspath(filename)
        self.db = sqlite3.connect(self.dbfilename)
        c = self.db.cursor()
        #c.execute("CREATE TABLE IF NOT EXISTS pages (pid INTEGER PRIMARY KEY, name TEXT UNIQUE, description TEXT,)")
        c.execute(
        """CREATE TABLE IF NOT EXISTS pages( 
                pid             INTEGER PRIMARY KEY, 
                name            TEXT UNIQUE, 
                description     TEXT, 
                options         BLOB 
                );""")
        self.db.commit()
        
        c.close()



    def get_paths(self, pageid):
        c = self.db.cursor()
        c.execute("SELECT * FROM paths_%s" % (pageid,))
        paths = c.fetchall()
        return paths

#    def get_pages(self):
#        c = db.cursor()
#        c.execute('SELECT pid, name, description, options FROM pages')
#        pages = c.fetchall()
#        for key, row in enumerate(pages): # get options from each page
#            c.execute("SELECT * FROM boards")
#            option = c.fetchall()
#            if len(option) == 0:
#                pages[key] = row + ("",)
#            else:
#                pages[key] = row + option[0]
#
#        c.close()
#        return pages

    def list_all_options(self,):
        c = self.db.cursor()
        c.execute('SELECT * from pages')
        options = c.fetchall()
        c.close()
        return options

    def get_title(self,pageid):
        c = self.db.cursor()
        #c.row_factory = sqlite3.Row
        c.execute("SELECT name FROM pages WHERE pid = %s" % (pageid,))
        title = c.fetchall()
        c.close()
        return title


    def get_desc(self, pageid):
        c = self.db.cursor()
        #c.row_factory = sqlite3.Row
        c.execute("SELECT description FROM pages WHERE pid = %s" % (pageid,))
        desc = c.fetchall()
        c.close()
        return desc


    def create_path_table(self, pageid):
        c = self.db.cursor()
        c.execute(
        """CREATE TABLE IF NOT EXISTS paths_%s (
            path_id             INTEGER PRIMARY KEY,
            name                TEXT,
            source_id           INTEGER,
            dest_id             INTEGER)""" % (pageid))
        self.db.commit()
        c.close()


    def populate_path_tables(self):
        c = self.db.cursor()
        pages = c.execute("SELECT pid FROM pages;")
        pages = pages.fetchall()
        for i in pages:
            self.create_path_table(i[0])
        c.close()






#     def add_record(self, last_name = '', other_names = '', email_address= ''):
#         db = sqlite3.connect(self.dbfilename)
#         c = db.cursor()
#         c.execute('INSERT INTO records(last_name, other_names, email_address) \
#                 VALUES(?,?,?)', (last_name,other_names, email_address))
#         db.commit()
#         c.close()
# 
#     def update_record(self, record_id, last_name ='', other_names='',email_address=''):
#         db.sqlite3.connect(self.dbfilename)
#         c = db.cursor()
#         c.execute('UPDATE records set last_name=?, other_names=?, email_address=? \
#                 WHERE record_internal_id = ?', (last_name, other_names, email_address, \
#                 record_id))
#         db.commit()
#         c.close()
# 
#     def delete_record(self, record_id):
#         db = sqlite3.connect(self.dbfilename)
#         c = db.cursor()
#         c.execute("DELETE FROM records where record_internal_id=?", (record_id))
#         db.commit()
#         c.close()
# 
#     def list_all_records(self, ):
#         db = sqlite3.connect(self.dbfilename)
#         c = db.cursor()
#         c.execute('SELECT * from records')
#         records = c.fetchall()
#         c.close()
#         return records
# 
#     def get_record(self, record_id):
#         db = sqlite3.connect(self.dbfilename)
#         c = db.cursor()
#         c.execute('SELECT * from records WHERE record_internal_id=?', (record_id,))
#         records = c.fetchall()
#         c.close()
#         return records[0]
# 
# 
# 
