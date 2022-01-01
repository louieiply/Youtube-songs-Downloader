import threading
import time

exitFlag = 0

class myThread (threading.Thread):
   def __init__(self, threadID, songname, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.songname = songname
      self.counter = counter
   def run(self):
      print ("Starting " + self.songname)
      print_time(self.songname, 5, self.counter)
      print ("Exiting " + self.songname)

def print_time(threadName, counter, delay):
   while counter:
      if exitFlag:
         threadName.exit()
      time.sleep(delay)
      print ("%s: %s" % (threadName, time.ctime(time.time())))
      counter -= 1




print("Exiting Main Thread")