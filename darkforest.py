#!/usr/bin/env python3

import npyscreen
from database import Database
from page_list_display import PageListDisplay
class DarkForest(npyscreen.NPSAppManaged):
    def onStart(self):
        self.myDatabase = Database()
        self.myDatabase.populate_path_tables()
        self.myPageId = 0
        self.myCarrot = False
        self.addForm('MAIN', PageListDisplay)

if __name__ == '__main__':
    try:
        myApp = DarkForest()
        myApp.run()
    except npyscreen.wgwidget.NotEnoughSpaceForWidget:
        print("Please increase the size of your terminal and reconnect!")
        print("Press any key to close the connection")
        input()
    except KeyboardInterrupt:
        print('til next time!')
