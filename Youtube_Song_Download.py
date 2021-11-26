import asyncio
import os
from tkinter import *
from tkinter import filedialog, messagebox, ttk
import youtube_dl
import youtubesearchpython
from youtubesearchpython.__future__ import VideosSearch
from youtubesearchpython.internal.constants import ResultMode


class main():

    def checkplaylist(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        isFolder = os.path.isdir(desktop + "\\" + self.getEntryVal())
        return isFolder

    def createfolder(self):
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        desktop = os.path.join(desktop, self.getEntryVal())
        os.mkdir(desktop)

    def enter(self,search):
        topResultList = youtubesearchpython.VideosSearch(search, limit=1)
        search.updatewindow("Searching song")
        result = topResultList.result(mode=ResultMode.dict)
        search.updatewindow('song found.')
        title = ((result["result"])[0])["title"]
        url = ((result["result"])[0])["link"]
        SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'

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
        with youtube_dl.YoutubeDL(YoutubeVideo) as ydl:
            self.updatewindow("Downloading song. ")
            self.updatewindow("Song title: " + title)
            ydl.download([url])

    def loadFile(self):
        try:
            if self.checkplaylist():
                messagebox.showerror(title="Error", message="Songlist name has already existed!!!!!!")
                return

            filename = filedialog.askopenfilename(initialdir="/", title="Select File",
                                                  filetypes=(("text files", "*.txt"),
                                                             ("all files", "*.*")))
            if filename is "":
                return
            self.createfolder()
            with open(filename, "r") as file:
                for line in file:
                    print(line)
                    songlist.append(line)
                    self.enter(line)
        except FileNotFoundError:
            print("exit window without action")
            messagebox.showinfo("Please input a file with at least 1 song")
        print("Finished downloads for playlist.")

    def getEntryVal(self):
        return self.entry.get()

    def update(self):
        self.root.update()

    def updatewindow(self,text):
        new_output = Label(self.buttomFrame, text=text, bg="white", anchor="w")
        new_output.pack(fill="both")
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
        self.topFrame = Frame(self.root, bg="#7289da")
        self.topFrame.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.1)
        self.label = Label(self.topFrame, text="Enter the song list name:", bg="#7289da")
        self.label.place(relx=0.36, rely=0.16)
        self.entry = Entry(self.topFrame, text="Example playlist Name")
        self.entry.insert(0, "SongList")
        self.entry.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.25, )
        current_var = StringVar()
        self.combobox = ttk.Combobox(self.topFrame, textvariable=current_var)
        self.combobox["values"] = ("Download songs from local .txt",
                                   "Download from youtube online playlist",)
        self.combobox.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.37, )
        self.combobox.current(0)
        self.buttomFrame = Frame(self.root, bg="White")
        self.buttomFrame.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.51)
        self.scrollbar = Scrollbar(self.buttomFrame)
        self.scrollbar.pack(side="right", fill=Y)

        self.myButton = Button(self.topFrame, text="Click here to Download", padx=10, pady=0, fg="#2c2f33",
                               bg="#99aab5",
                               command=self.loadFile)
        self.myButton.place(relx=0.34, rely=0.5)


root = Tk()
songlist = []
window = main(root)
root.mainloop()

# if __name__ == "__main__":
#     main()
