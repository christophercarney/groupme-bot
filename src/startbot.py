import groupy, time, sys, os
from groupy import Bot, Group

import stats, twitch, randomevents, dota, utils, timer, markov

SLEEP_INTERVAL = 3          #time to sleep in seconds

class startBot():
    m_groupName = ''
    m_thisGroup = None
    m_thisBot = None
    m_admins = ['Christopher', 'Patrick']
    m_thisTwitch = None
    m_thisAlarm = None
    m_thisMarkov = None

    def __init__(self, groupName):
        self.m_groupName = groupName
        self.refreshGroup()
        self.refreshBot()
        self.m_thisTwitch = twitch.emotes()
        self.m_thisAlarm = timer.alarm()
        self.m_thisMarkov = markov.markov(self.m_thisGroup, self.m_groupName, self.m_thisBot)

    def runBot(self):
        cur = self.m_thisGroup.messages()
        start_messages = self.m_thisGroup.message_count
        messageAlreadyParsed = True
    
        while True:                   
            anyAlarms = self.m_thisAlarm.checkAlarms()
            if anyAlarms:
                self.m_thisBot.post(anyAlarms)          
            if messageAlreadyParsed == False:
                for message in cur:
                    if message.name == self.m_thisBot.name:
                        continue
                    requester = message.name.split(' ')[0]
                    if not message.text:
                        utils.showOutput('recived image ({0}) from {1}'.format(message.created_at, requester))
                        continue
                    else:
                        utils.showOutput('recieved message {0} ({1}) from {2}'.format(message.text.encode('utf-8'), message.created_at, requester), verbosity=utils.INFO_LEVEL_Useful)
                        
                    if message.text[0] == '!':
                        self.checkAndEvaluateCommand(message, requester)             #getting a little unwieldy, we'll hook in through this method now
                    else:    
                        self.checkAndEvaluateMessage(message, requester)            #same thing but for misc. events happening only from test
            
            messageAlreadyParsed = True
            utils.showOutput('sleeping for {0}s '.format(SLEEP_INTERVAL), end='')
            time.sleep(SLEEP_INTERVAL)
            try:
                self.refreshGroup()
                new_messages = self.m_thisGroup.message_count
                utils.showOutput('started with {0} messages, now see {1}'.format(start_messages, new_messages))
                if (new_messages - start_messages) > 0:
                    cur = cur.newer()
                    start_messages = new_messages
                    utils.showOutput('retrieved {0} new messages'.format(len(cur)))
                    messageAlreadyParsed = False
            except Exception as e:
                utils.showOutput(e)

    def checkAndEvaluateCommand(self, message, requester):
        command = message.text.split(' ')
        if command[0].lower() == '!kappa':
            self.m_thisTwitch.kappa(self.m_thisBot)
        elif command[0].lower() == '!elegiggle':
            self.m_thisTwitch.elegiggle(self.m_thisBot)                        
        elif command[0].lower() == '!biblethump':
            self.m_thisTwitch.biblethump(self.m_thisBot)
        elif command[0].lower() == '!dansgame':
            self.m_thisTwitch.dansgame(self.m_thisBot)
        elif command[0].lower() == '!kreygasm':
           self.m_thisTwitch.kreygasm(self.m_thisBot)
        elif command[0].lower() == '!4head':
           self.m_thisTwitch.fourhead(self.m_thisBot)
        elif command[0].lower() == '!pogchamp':
           self.m_thisTwitch.pogchamp(self.m_thisBot)     
        elif command[0].lower() == '!notlikethis':
            self.m_thisTwitch.notlikethis(self.m_thisBot)   
        elif command[0] == '!roll':
            try:
                range = int(command[1])
                randomevents.roll(self.m_thisBot, requester, range=range+1)
            except:
                randomevents.roll(self.m_thisBot, requester)
        elif command[0] == '!flip':
            randomevents.flip(self.m_thisBot, requester)
        elif command[0] == '!lastmatch':
            if '-u' in message.text:
                try:
                    dota.lastMatch(self.m_thisBot, command[2])
                except:
                    self.m_thisBot.post("Couldn't understand command:{0} {1} {2}, please see !commands for usage".format(command[0], command[1], command[2]))
            else:
                dota.lastMatch(self.m_thisBot, requester)
        elif command[0] == '!register':
            try:
                dota.registerId(command[1], command[2], self.m_thisBot)
            except:
                self.m_thisBot.post('Couldn\'t understand !register command, use !commands for usages')
        elif command[0] == '!commands':
            utils.commands(self.m_thisBot)
        elif command[0] == '!stop':
            if requester in self.m_admins:
                return              
        elif command[0] == '!clearcache':
            if requester in self.m_admins:
                utils.clearCache()
        elif command[0] == '!alarm':
            self.m_thisAlarm.setAlarm(message.text, self.m_thisBot)

    def checkAndEvaluateMessage(self, message, requester):
        if 'thanks {0}'.format(self.m_thisBot.name.lower()) in message.text.lower() or \
            'thanks, {0}'.format(self.m_thisBot.name.lower()) in message.text.lower():
            utils.thanks(self.m_thisBot, requester)
        elif '{0},'.format(self.m_thisBot.name.lower()) in message.text.lower() or \
              ', {0}'.format(self.m_thisBot.name.lower()) in message.text.lower():
            self.m_thisMarkov.talk(message.text, self.m_thisBot, self.m_groupName)

    def refreshGroup(self):
        groups = groupy.Group.list()
        for group in groups:
            if group.name == self.m_groupName:
                self.m_thisGroup = group
                break
        if self.m_thisGroup is None:
            utils.showOutput("Cannot find group {0}".format(groupName), verbosity=utils.INFO_LEVEL_Important)
            sys.exit(0)

    def refreshBot(self):
        bots = Bot.list()
        for bot in bots:
            if self.m_thisGroup.id == bot.gorup_id:
                self.m_thisBot = bot
                break
        if self.m_thisBot is None:
            utils.showOutput("Cannot find bot for group {0}".format(groupName), verbosity=utils.INFO_LEVEL_Important)
            sys.exit(0)

def main(groupName):
    myBot = startBot(groupName)
    myBot.runBot()
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1])
