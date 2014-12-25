# Python 3.4.2 64bit
import threading
import subsequence as sub
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import scrolledtext as sctxt

class UI:

    def __init__(self, master):


        # file path
        self.path = ''

        # main window
        master.wm_title('FNA_poke')
        fileFrame = tk.Frame(master)
        patternFrame = tk.Frame(master)
        pokeFrame = tk.Frame(master)
        resultFrame = tk.Frame(master)
        
        
        # search pattern
        self.pattern = tk.StringVar()
        self.patternLabel = tk.Label(patternFrame, text='Pattern') 
        self.patternEntry = tk.Entry(patternFrame, textvariable=self.pattern)
        self.pokeButton = tk.Button(
                pokeFrame,
                text='Poke',
                command=self.poke
        )


        # text output
        self.textLabel = tk.Label(resultFrame, text='Matches')
        self.text = sctxt.ScrolledText(
                master,
                wrap = tk.WORD,
                state=tk.DISABLED
        )

        # open file button
        self.fileButton = tk.Button(
                fileFrame, 
                text='Choose file', 
                command=self.openFile
        )

        # quit button, doesn't really make sense, does it?
#        self.quitButton = tk.Button(fileFrame, text='Quit', command=fileFrame.quit)




        # layout
        fileFrame.pack(anchor=tk.W, padx=5, pady=5)
        patternFrame.pack(fill=tk.X, padx=5, pady=5)
        pokeFrame.pack(anchor=tk.W, padx=5, pady=5)
        self.patternLabel.pack(side=tk.LEFT)
        self.patternEntry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.fileButton.pack()
        self.pokeButton.pack()
        resultFrame.pack(side=tk.BOTTOM)
        self.text.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    def openFile(self):
        # remember Except FileNotFoundError
        self.path=fd.askopenfilename()

    def fileHead(self):
        with open(self.path, 'r') as bla:
            for i in range(0,5):
                self.print(bla.readline())


    def print(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.INSERT, text)
        self.text.config(state=tk.DISABLED)


    def poke(self):
        search = sub.Subsequence(self.pattern.get())

        meta = ''
        sequence = ''
        match = ''

        try:
            with open(self.path, 'r') as fna:
                for line in fna:
                    match = search.match(sequence)
                    if match != []:
                        self.print(meta)
                        self.print(sequence)
                    elif line[0] == '>':
                        sequence = ''
                        meta = line
                    else:
                        sequence += line.strip()

        except FileNotFoundError as e:
            self.print(e)
            return




root = tk.Tk()
ui = UI(root)
root.mainloop()
