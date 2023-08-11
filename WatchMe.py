from os import listdir
from os.path import isfile, join
import pymsteams
import threading
import time


class WatchMe:
    
    contentBeforeScan = []
    contentAfterScan = []
    section = None
    myTeamsMessage = None

    def startWatch(self):
        self.thread.start()

    def watch(self):
        while True:
            
            actionTaken = False
            self.contentAfterScan = [f for f in listdir(self.path) if isfile(join(self.path, f))]
            newfiles = []
            
            if (self.contentBeforeScan != self.contentAfterScan):
                for file in self.contentAfterScan:
                    if (self.checkIfElementIsNew(self.contentBeforeScan, file)):
                        newfiles.append(file)

            numberOfFiles = len(newfiles)

            if (not actionTaken and numberOfFiles == 0):
                actionTaken = True

            if (not actionTaken and numberOfFiles > 10):
                self.createMessage()
                actionTaken = True
                
                section = pymsteams.cardsection()
                section.title(self.path)
                section.text("Im Ordner sind sehr viele Dateien gelandet." )
                self.myTeamsMessage.addSection(section)

                newfiles.clear()
                #self.myTeamsMessage.printme()
                self.myTeamsMessage.send()

            if (not actionTaken and numberOfFiles > 0):
                self.createMessage()
                actionTaken = True
                for file in newfiles:
                    section = pymsteams.cardsection()
                    section.title("Ort: " + self.path)
                    section.text("Dateiname: **" + file + "**")
                    self.myTeamsMessage.addSection(section)
                newfiles.clear()
                self.myTeamsMessage.summary("Bitte die Dateien erneut prüfen.")
                #self.myTeamsMessage.printme()
                self.myTeamsMessage.send()
                self.contentBeforeScan = self.contentAfterScan
                time.sleep(self.interval)

    def toString(self):
        return f'Path: {self.path}\nInterval: {self.interval}\nWebhook: {self.webhook}\nInitialContent: {self.contentBeforeScan}'

    def initialScan(self):
        self.contentBeforeScan = [f for f in listdir(self.path) if isfile(join(self.path, f))] 

    def createMessage(self):
        self.myTeamsMessage = pymsteams.connectorcard(self.webhook)
        self.myTeamsMessage.color(self.cardcolor)
        self.myTeamsMessage.title("Neue Datei(en)")
        self.myTeamsMessage.text("*Wenn erledigt, bitte mit 👍 reagieren.*") 

    @staticmethod
    def checkIfElementIsNew(list, element):
        if element in list:
            return False
        else:
            return(element)
    
    def __init__(self, path: str, interval: int, webhook: str, cardcolor: str):
        """ path -> folderlocation \n
            interval -> seconds to rescan \n
            webhook ->teams webhook \n
            cardcolor -> hex"""
        self.path = path
        self.interval = interval
        self.webhook = webhook
        self.cardcolor = cardcolor
        self.initialScan()
        self.thread = threading.Thread(target=self.watch)

