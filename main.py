import tkinter as tk
import time
import threading
import random
import queue as q
import subsequence as sub
from tkinter import filedialog as fd
from tkinter import scrolledtext as sctxt

class GuiPart:
    def __init__(self, master, queue, endCommand):



        def handler():
            endCommand()

        master.protocol("WM_DELETE_WINDOW", handler)

        self.batch = 1000
        self.queue = queue
        self.poking = False

        # Set up the GUI

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


    def poke(self):
        self.poking = not self.poking
        return

    def isPoking(self):
        return self.poking

    def hasFile(self):
        return not self.path == ''

    def getFile(self):
        return self.path

    def openFile(self):
        self.path=fd.askopenfilename()

    def getPattern(self):
        return self.pattern.get().replace('\n','').strip()

    def processIncoming(self):
        i = 0
        while i <= self.batch and self.queue.qsize() and self.poking:
            try:
                self.print(self.queue.get(0))
            except q.Empty:
                pass

            i += 1


    def print(self, text):
        self.text.config(state=tk.NORMAL)
        self.text.insert(tk.INSERT, text)
        self.text.config(state=tk.DISABLED)


class ThreadedClient:
    def __init__(self, master):
        self.master = master
        self.FNAfile = 0

        self.callSpeed = 1000
        self.idle = 1
 
        # Create queue
        self.queue = q.Queue()

        # Set up GUI 
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        self.running = 1
        self.thread1 = threading.Thread(target=self.workerThread1)
        self.thread1.start()

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        self.periodicCall()

    def periodicCall(self):
        self.gui.processIncoming()
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(self.callSpeed, self.periodicCall)

    def workerThread1(self):
        while self.running:
            if self.FNAfile == 0 and self.gui.hasFile():
                self.FNAfile = open(self.gui.getFile(), 'r')

            elif self.gui.isPoking() and self.running:
                self.callSpeed = 100
                self.idle = 0
                if self.FNAfile != 0:
                    self.poke()
            else:
                self.callSpeed = 1000


    def poke(self):
        meta = ''
        sequence = ''
        match = ''
        line = ''
        count = 0

        search = sub.Subsequence(self.gui.getPattern())
        while True:
            if count >= 1000 or not self.gui.isPoking():
                break

            try:
                line = self.FNAfile.readline()
                match = search.perfectMatch(sequence)
                if(match != []):
                    count += 1
                    self.queue.put('Match type: PERFECT\n' + meta.rstrip()+'\n'+sequence.rstrip()+'\n'+'============\n')
                elif line[0] == '>':
                    count += 1
                    sequence = ''
                    meta = line
                else:
                    sequence += line.strip()

            except IndexError:
                self.idle = 1
                self.callSpeed = 1000
                return

            

    def endApplication(self):
        self.running = 0

rand = random.Random()
root = tk.Tk()

client = ThreadedClient(root)
root.mainloop()
