from Observer import Observer
from EventListener import Observable
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk, Listbox, Label, Canvas, Frame, Entry, Tk
import youtubesearchpython
from youtubesearchpython import ResultMode


class window():
    

    def checkplaylist(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        isFolder = os.path.isdir(desktop + "\\" + self.getEntryVal())
        return isFolder

    def createfolder(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        desktop = os.path.join(desktop, self.getEntryVal())
        os.mkdir(desktop)

    def enter(self,search):
        self.topResultList = youtubesearchpython.VideosSearch(search, limit=1)
        self.updatewindow("Searching song")
        self.result = self.topResultList.result(mode=ResultMode.dict)
        self.updatewindow('song found.')
        title = ((self.result["result"])[0])["title"]
        self.title = title
        url = ((self.result["result"])[0])["link"]
        self.url = url
        SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'
        print(title)
        YoutubeVideo = {
            "format": "best", "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",

            }],
            "outtmpl": '%USERPROFILE%\Desktop\\' + self.getEntryVal() + '\%(title)s-%(id)s.%(ext)s',

        }
        # path + "/%(title)s.mp3
        self.update()
        self.updatewindow("Downloading song. ")
        self.updatewindow("Song title: " + self.title)
        self.entercountid =+ 1
        entity = Observer(self.entercountid,"song",YoutubeVideo,self.url)
        print("Count run:" + str(self.entercountid))
        self.observerlist.attach(entity)


    def loadFile(self):
        try:
            if self.checkplaylist():
                messagebox.showerror(title="Error", message="Songlist name has already existed!!!!!!")
                return

            filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                                  filetypes=(("text files", "*.txt"),
                                                             ("all files", "*.*")))
            if filename == "":
                return
            self.createfolder()
            with open(filename, "r") as file:
                for line in file:
                    print("print song name: "+line)
                    songlist.append(line)
                    self.enter(line)
            self.observerlist.exec()
        except FileNotFoundError:
            print("exit window without action")
            messagebox.showinfo("Please input a file with at least 1 song")
        print("Finished downloads for playlist.")

    def getEntryVal(self):
        return self.entry.get()

    def update(self):
        self.root.update()

    def updatewindow(self,text):
        self.listbox.insert(self.linecount,text)
        self.linecount = self.linecount + 1
        self.update()

    def check(self,app):
        if app['status'] != 'finished':
            self.update()
        else:
            return

    def __init__(self, root):
        self.root = root
        self.root.title("Youtube songs downloader")
        self.root.resizable(width=False, height=False)
        self.canvas = Canvas(self.root, height=600, width=600, bg="#2c2f33")
        self.canvas.pack()
        self.entercountid = 0
        self.linecount = 0
        self.observerlist = Observable()
        self.topFrame = Frame(self.root, bg="#7289da")
        self.topFrame.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.1)    
        self.label = Label(self.topFrame, text="Enter the song list name:", bg="#7289da")
        self.label.place(relx=0.36, rely=0.16)
        self.entry = Entry(self.topFrame, text="Example playlist Name")
        self.entry.insert(0, "SongList")
        self.entry.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.25, )
        combobox = ttk.Combobox(self.topFrame, state="readonly")
        self.combobox = combobox
        self.combobox['values'] = ("Download songs from local .txt",
                                   "Download from youtube online playlist")
        self.combobox.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.37)
        self.combobox.set("Download songs from local .txt")
        self.combobox.current(0)

        self.buttomFrame = Frame(self.root, bg="White")
        self.buttomFrame.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.51)

        self.listbox = Listbox(self.buttomFrame,bg="White")
        self.listbox.pack(side="left", fill= BOTH, expand=1)

        self.scrollbar = Scrollbar(self.buttomFrame)
        self.scrollbar.pack(side="right", fill=Y)

        self.listbox.config(yscrollcommand = self.scrollbar.set)
        self.scrollbar.config(command = self.listbox.yview)

        self.myButton = Button(self.topFrame, text="Click here to Download", padx=10, pady=0, fg="#2c2f33",
                               bg="#99aab5",
                               command=self.loadFile)
        self.myButton.place(relx=0.34, rely=0.5)



root = Tk()
songlist = []
window = window(root)
root.mainloop()

# if __name__ == "__main__":
#     main()
