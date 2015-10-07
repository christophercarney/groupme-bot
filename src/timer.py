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
            hours = 0; minutes = 0; seconds = 0
            if "-h" in text:
                hours = text[(text.find("-h")):].split()[1]
            if "-m" in text:
                minutes = text[(text.find("-m")):].split()[1]
            if "-s" in text:
                seconds = text[(text.find("-m")):].split()[1]                
            message = text.split("\"")[1]
            
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
        
                
    