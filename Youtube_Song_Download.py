import asyncio
import os
from tkinter import *
from tkinter import filedialog, messagebox
import youtube_dl
import youtubesearchpython
from youtubesearchpython.__future__ import VideosSearch
from youtubesearchpython.internal.constants import ResultMode

songlist = []


def checkplaylist():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    isFolder = os.path.isdir(desktop + "\\" + getEntryVal())
    return isFolder


def createfolder():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    desktop = os.path.join(desktop, getEntryVal())
    os.mkdir(desktop)


def enter(search):
    topResultList = youtubesearchpython.VideosSearch(search, limit=1)
    updatewindow("Searching song")
    result = topResultList.result(mode=ResultMode.dict)
    updatewindow('song found.')
    title = ((result["result"])[0])["title"]
    url = ((result["result"])[0])["link"]
    SAVE_PATH = '/'.join(os.getcwd().split('/')[:3]) + '/Downloads'

    YoutubeVideo = {
        "format": "best", "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",

        }],
        "outtmpl": '%USERPROFILE%\Desktop\\' + getEntryVal() + '\%(title)s-%(id)s.%(ext)s',

    }
    # path + "/%(title)s.mp3
    update()
    with youtube_dl.YoutubeDL(YoutubeVideo) as ydl:
        updatewindow("Downloading song. ")
        updatewindow("Song title: " + title)
        ydl.download([url])


def loadFile():
    try:
        if checkplaylist():
            messagebox.showerror(title="Error", message="Songlist name has already existed!!!!!!")
            return

        filename = filedialog.askopenfilename(initialdir="/", title="Select File", filetypes=(("text files", "*.txt"),
                                                                                              ("all files", "*.*")))
        if filename is "":
            return
        createfolder()
        with open(filename, "r") as file:
            for line in file:
                print(line)
                songlist.append(line)
                enter(line)
    except FileNotFoundError:
        print("exit window without action")
        messagebox.showinfo("Please input a file with at least 1 song")
    print("Finished downloads for playlist.")


def getEntryVal():
    return entry.get()


def update():
    root.update()


def updatewindow(text):
    new_output = Label(buttomFrame, text=text, bg="white", anchor="w")
    new_output.pack(fill="both")
    update()


def check(app):
    if app['status'] != 'finished':
        update()
    else:
        return


root = Tk()
root.title("Youtube songs downloader")
root.resizable(width=False, height=False)
canvas = Canvas(root, height=600, width=600, bg="#2c2f33")
canvas.pack()
topFrame = Frame(root, bg="#7289da")
topFrame.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.1)
label = Label(topFrame, text="Enter the song list name:", bg="#7289da")
label.place(relx=0.36, rely=0.16)
entry = Entry(topFrame, text="Example playlist Name")
entry.insert(0, "SongList")
entry.place(relwidth=0.5, relheight=0.1, relx=0.25, rely=0.25, )
buttomFrame = Frame(root, bg="White")
buttomFrame.place(relwidth=0.8, relheight=0.4, relx=0.1, rely=0.51)
scrollbar = Scrollbar(buttomFrame)
scrollbar.pack(side="right", fill=Y)

myButton = Button(topFrame, text="Click here to Download", padx=10, pady=0, fg="#2c2f33", bg="#99aab5",
                  command=loadFile)
myButton.place(relx=0.34, rely=0.5)
# myLabel1 = Label(canvas, text="I hate you")
# myLabel2 = Label(canvas, text="I hate you too.")
# myLabel1.grid(row=0, column=0)
# myLabel2.grid(row=1, column=0)

root.mainloop()

# if __name__ == "__main__":
#     main()
