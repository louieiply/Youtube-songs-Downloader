from typing import List
from Observer import Observer
import youtube_dl

class Observable:

    def __init__(self):
        self.observers : List[Observer] = []
        self.id = 0
        
    def attach(self,observer:Observer):
        count = str(observer.threadid)
        print("this is observer"+count)
        self.observers.append(observer)

    def discard(self,observer:Observer):
        self.observers.remove(observer)

    def notify(self) -> None:
        pass

    def exec(self):
        i = 0
        for observer in self.observers:
            observer.start()
    
    def count(self):
        return self.observers.count()