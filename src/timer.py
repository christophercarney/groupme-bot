import os, time, fileinput, re

import utils

class alarm():

    def __init__(self):
        self.messageDictionary = {}
        self.cacheLocation = '..' + os.path.sep + 'cache' + os.path.sep + 'alarm.cache'
    
        if not utils.cacheExists("alarm.cache"):
            open(self.cacheLocation,'w')
        else:
            with open(self.cacheLocation) as f:
                for line in f:
                    self.messageDictionary[line.split(",")[0]] = line.split(",")[1]
                    timeUntilAlarm = float(line.split(",")[0]) - time.time()
                    print("Alarm found. Will go off in {0:.2f} minutes".format(timeUntilAlarm/60))
        
    def setAlarm(self,text,bot):
        try:
            text = text.replace('!alarm ','')
            
            allFlags = re.findall('-\w \d+',text)
            
            hours = 0; minutes = 0; seconds = 0
            
            for currentFlag in allFlags:
                text = text.replace(currentFlag,'')
                if "-h" in currentFlag:
                    hours = int(currentFlag[2:])
                if "-m" in currentFlag:
                    minutes = int(currentFlag[2:])
                if "-s" in currentFlag:
                    seconds = int(currentFlag[2:])
                    
            message = text.strip()
            
            alarmTime = time.time() + int(hours) * 3600 + int(minutes) * 60 + int(seconds)
            
            self.messageDictionary[alarmTime] = message
            
            cache = open(self.cacheLocation,'a')
            cache.write("{0},\"{1}\"\n".format(alarmTime, message))
            cache.close()
            
            bot.post("In {0} hour(s), {1} minute(s), and {2} second(s), I will remind you: {3}".format(hours,minutes,seconds,message))
        except:
            bot.post("You screwed that up... Try again.")
        
    def checkAlarms(self):
        for alarm in self.messageDictionary:
            if time.time() > float(alarm):
                for line in fileinput.input(self.cacheLocation, inplace=1):
                    line = re.sub(r'{}.*'.format(alarm), r'', line.rstrip())
                message = self.messageDictionary[alarm]
                self.messageDictionary.pop(alarm,0)
                return message
        
                
    