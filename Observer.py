import threading
import youtube_dl

exitFlag = 0

class Observer(threading.Thread):
    def __init__(self,threadid,songname,ydls,url):
        threading.Thread.__init__(self)
        self.threadid = threadid
        self.songname = songname
        self.url = url
        self.ydls = ydls


    def run(self):
        with youtube_dl.YoutubeDL(self.ydls) as ydl:
            print("Starting thread")
            print(threading.current_thread().ident)
            # ydl.download([self.url])
            print("Exiting thread")
            
        # print("thread ID:"+str(self.threadid))

    