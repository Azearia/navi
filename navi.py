import keyboard
import os
import sys
import shutil

class Navi:

    class _fileobj:
        def __init__(self):
            self.abspath = ''
            self.name = ''
            self.suffix = ''
        def __call__(self, filepath):
            self.abspath = os.path.abspath(filepath)
            self.name = filepath.split('/')[-1]

            if '.' in filepath: self.suffix = filepath.split('.')[-1]

        def _clear(self):
            self.abspath = ''
            self.name = ''
            self.suffix = ''
        
        def drop(self, newpath):
            if self.abspath != '':
                if self.abspath != os.path.abspath(newpath+'/'+self.name):
                    shutil.move(self.abspath, newpath)
                    self._clear()
                else:
                    self._clear()


    def __init__(self):
        if sys.platform.startswith('linux'):
            self.osclear = 'clear'
            self.ops = 'linux'
        elif sys.platform.startswith('win32'):
            self.osclear = 'cls'
            self.ops = 'windows'
        else:
            self.osclear = ''
            self.ops = ''

        keyboard.add_hotkey('up', self.cursorup)
        keyboard.add_hotkey('down', self.cursordown)
        keyboard.add_hotkey('right', self.inpage)
        keyboard.add_hotkey('left', self.outpage)
        keyboard.add_hotkey('p', self.breakloop)
        keyboard.add_hotkey('h', self.holdfile)
        keyboard.add_hotkey('j', self.dropfile)

        self.naviActive = True
        self.currentdir = os.path.abspath('./')
        self.currentdirlist = os.listdir(self.currentdir)
        self.cursorpos = 0
        self.responsemsg = ''
        self.file = self._fileobj()
    
        self.refreshpage()

    def cursorup(self):
        if self.cursorpos == 0:
            self.cursorpos = len(self.currentdirlist)-1
        else:
            self.cursorpos -= 1

        self.refreshpage()

    def cursordown(self):
        if self.cursorpos == len(self.currentdirlist)-1:
            self.cursorpos = 0
        else:
            self.cursorpos += 1

        self.refreshpage()

    def refreshpage(self):
        print('-------------------')
        os.system(self.osclear)

        for ct, item in enumerate(self.currentdirlist):
            if os.path.abspath(f'./{item}') == self.file.abspath:
                item = item+' : (HOLDING)'

            if ct == self.cursorpos:
                print(item, '<', self.file.name)
            else:
                print(item)

        print('-------------------')
        print(self.responsemsg)
        print('\n\nh to hold/release file | arrows to move through directories | p to break loop | h pickup file | j drop file')
        self.responsemsg = ''
        
    def inpage(self):

        if os.path.isdir(self.currentdir + '/' + self.currentdirlist[self.cursorpos]):
            self.currentdir = self.currentdir + '/' + self.currentdirlist[self.cursorpos]

            self.refreshdir()

        else:
            self.responsemsg = 'Invalid directory'

            self.refreshpage()
        
    def outpage(self):

        if '/'.join(self.currentdir.split('/')[:-1]) != '':
            self.currentdir = '/'.join(self.currentdir.split('/')[:-1])

            self.refreshdir()
        else:
            self.responsemsg = 'Cannot go back any farther'

            self.refreshpage()

    def refreshdir(self, curspos = 0):
        self.currentdirlist = os.listdir(self.currentdir)
        self.cursorpos = curspos

        self.refreshpage()

    def holdfile(self):
        if not os.path.isdir(self.currentdir + '/' + self.currentdirlist[self.cursorpos]):
            self.file(self.currentdir + '/' + self.currentdirlist[self.cursorpos])
        else:
            self.responsemsg = 'Cannot move directories'
        
        self.refreshpage()
    
    def dropfile(self):
        self.file.drop(self.currentdir)

        self.refreshdir(self.cursorpos)



    def breakloop(self):
        self.naviActive = False

    def start(self):
        while self.naviActive:
            pass


if __name__=='__main__':
    Navi().start()