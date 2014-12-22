from tkinter import *
from tkinter import filedialog

class UI:

    def __init__(self, master):
        self.path = ''
        frame = Frame(master)
        frame.pack()

        self.fileButton = Button(frame, text='Choose file', command=self.openFile)
        self.fileButton.pack(side=LEFT)

        self.quitButton = Button(frame, text='Quit', command=frame.quit)
        self.quitButton.pack(side=LEFT)



    def openFile(self):
        self.path=filedialog.askopenfilename()


root = Tk()
ui = UI(root)
root.mainloop()
