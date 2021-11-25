import npyscreen
import curses
import textwrap
from ascii_art import get_asciiart

class Image(npyscreen.Textfield):
    def __init__(self, *args, **keywords):
        super(Image, self).__init__(*args, **keywords)
        self.syntax_highlighting = True
    def display_value(self, value):
        return value

class ImagePager(npyscreen.Pager):
    _contained_widgets = Image
    def display_value(self, value):
        lines = textwrap.wrap(value, self.width - 4)
        return  lines

class Page(npyscreen.Textfield):
    def __init__(self, *args, **keywords):
        super(Page, self).__init__(*args, **keywords)
        self.syntax_highlighting = True
    def display_value(self, value):
        return value


class PagePager(npyscreen.Pager):
    _contained_widgets = Page
    def display_value(self, value):
        lines = textwrap.wrap(value, self.width - 4)
        return  lines

class PageList(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(PageList, self).__init__(*args, **keywords)

        self.handlers.update({
            curses.KEY_RIGHT: self.h_act_on_highlighted,
            })
    def display_value(self, value):
        return "%s" % (value[1])

    def actionHighlighted(self, value, keypress):
        if self.parent.parentApp.myPageId == 5 and int(value[3]) == 6:
            self.parent.parentApp.myCarrot = True
        if self.parent.parentApp.myPageId == 11:
            self.parent.parentApp.myCarrot = False
        self.parent.parentApp.myPageId = int(value[3])
        self.parent.parentApp.switchForm('MAIN')


class PageListDisplay(npyscreen.FormMuttActiveWithMenus):
    MAIN_WIDGET_CLASS = PageList
    MAIN_WIDGET_CLASS_START_LINE = 30
    BLANK_LINES_BASE = 0
    def create(self, *args, **keywords):
        MAXY = self.lines
        #self.wDesc = self.add(npyscreen.Textfield, value = 0, 
        #                        rely=self.__class__.MAIN_WIDGET_CLASS_START_LINE -2 ,
        #                        height = self.__class__.MAIN_WIDGET_CLASS_START_LINE -1,
        #                        relx = self.__class__.STATUS_WIDGET_X_OFFSET,
        #                        editable = False)
        #self.wImage = self.add(ImagePager, values = 'test',
        #                        rely=3,
        #                        relx=self.__class__.STATUS_WIDGET_X_OFFSET,
        #                        editable = False)
        self.wImage = self.add(ImagePager,
                                rely=3,
                                relx=self.__class__.STATUS_WIDGET_X_OFFSET,
                                editable = False)
        self.wDesc = self.add(PagePager, values = ['test','test2'], 
                                height = 0,
                                rely=0,
                                relx = self.__class__.STATUS_WIDGET_X_OFFSET,
                                editable = False)
        self.wStatus1 = self.add(self.__class__.STATUS_WIDGET_CLASS,
                                rely=0,
                                relx=self.__class__.STATUS_WIDGET_X_OFFSET,
                                editable=False)
        self.wStatus2 = self.add(self.__class__.STATUS_WIDGET_CLASS,
                                rely = 10,#self.__class__.MAIN_WIDGET_CLASS_START_LINE -1,
                                relx = self.__class__.STATUS_WIDGET_X_OFFSET,
                                editable = False)
        self.wMain = self.add(self.__class__.MAIN_WIDGET_CLASS,
                                rely = self.__class__.MAIN_WIDGET_CLASS_START_LINE,
                                relx = 0, max_height = -2, allow_filtering = False)
        self.wCommand = self.add(self.__class__.COMMAND_WIDGET_CLASS, name = self.__class__.COMMAND_WIDGET_NAME,
                                rely= MAXY-1 - self.BLANK_LINES_BASE, 
                                relx =0, begin_entry_at = True, allow_override_begin_entry_at = True)
        self.wStatus1.important = True
        self.wStatus2.important = True
        self.nextrely = 2
        self.keypress_timeout = 20
        


    def beforeEditing(self):
        self.wStatus2.value = ''
        self.wStatus1.value = self.parentApp.myDatabase.get_title(self.parentApp.myPageId)[0][0] 
        self.update_image()
    def update_list(self): # perhaps this should be updating options 
        self.wMain.rely = self.wDesc.rely + self.wDesc.height + 2
        if self.parentApp.myCarrot == False and self.parentApp.myPageId == 10:
            self.wMain.values = self.parentApp.myDatabase.get_paths(self.parentApp.myPageId)[1:]
        else:
            self.wMain.values = self.parentApp.myDatabase.get_paths(self.parentApp.myPageId)
        self.wMain.display()

    def update_desc(self): 
        self.wDesc.values = textwrap.wrap(self.parentApp.myDatabase.get_desc(self.parentApp.myPageId)[0][0], 100)
        self.wDesc.rely = self.wImage.height + 4 
        self.wDesc.height = len(self.wDesc.values)
        self.wDesc.display()
        try: 
            self.update_list() # should update with options according to the current page id 
        except curses.error:
            pass

    def get_image(self,pageid):
        image = get_asciiart(pageid)[0]
        # handle some terms not supporting unicode 

        return image.splitlines()




    def update_image(self):
        image = self.get_image(self.parentApp.myPageId)
        # pad the image
        pad = int((self.columns-len(max(image, key = len)))/4) # this padding method is unoriginal, i didn't write it
        if pad < 0:
            pad = 0
        for i in range(0, len(image)):
            image[i] = " "*pad + image[i]
        self.wImage.values = image
        self.wImage.height = len(image)
        #self.wImage.values = textwrap.wrap(get_asciiart(self.parentApp.myPageId)[0],get_asciiart(self.parentApp.myPageId)[1],replace_whitespace = False)
        self.wImage.display()
        self.update_desc()
