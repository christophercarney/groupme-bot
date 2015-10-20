import groupy, time, sys, os
from groupy import Bot, Group

import stats, twitch, randomevents, dota, utils, timer, markov

if os.name == 'posix':
    import resource

class startBot():
    m_groupName = ''
    m_thisGroup = None
    m_thisBot = None
    m_admins = ['Christopher', 'Patrick']

    def __init__(self, groupName):
        self.m_groupName = groupName
        self.refreshGroup()
        self.refreshBot()

    def runBot(self):
        cur = self.m_thisGroup.messages()
        start_messages = self.m_thisGroup.message_count
        alreadyParsed = True
    
        thisTwitch = twitch.emotes()
        thisAlarm = timer.alarm()
        thisMarkov = markov.markov(self.m_thisGroup, self.m_groupName)
        while True:                   
            anyAlarms = thisAlarm.checkAlarms()
            if anyAlarms:
                self.m_thisBot.post(anyAlarms)
            
            if alreadyParsed == False:
                for message in cur:
                    requester = message.name.split(' ')[0]
                    if not message.text:
                        print('recived image ({0}) from {1}'.format(message.created_at, requester))
                        continue
                    else:
                        print('recieved message {0} ({1}) from {2}'.format(message.text.encode('utf-8'), message.created_at, requester))
                    if message.text[0] == '!':
                        command = message.text.split(' ')
                        try:
                            resource.getrusage(resource.RUSAGE_SELF)
                        except:
                            pass
                        if command[0] == '!stats':
                            stats.stats(self.m_thisBot, self.m_thisGroup)
                        elif command[0].lower() == '!kappa':
                            thisTwitch.kappa(self.m_thisBot)
                        elif command[0].lower() == '!elegiggle':
                            thisTwitch.elegiggle(self.m_thisBot)                        
                        elif command[0].lower() == '!biblethump':
                            thisTwitch.biblethump(self.m_thisBot)
                        elif command[0].lower() == '!dansgame':
                            thisTwitch.dansgame(self.m_thisBot)
                        elif command[0].lower() == '!kreygasm':
                            thisTwitch.kreygasm(self.m_thisBot)
                        elif command[0].lower() == '!4head':
                            thisTwitch.fourhead(self.m_thisBot)
                        elif command[0].lower() == '!pogchamp':
                            thisTwitch.pogchamp(self.m_thisBot)     
                        elif command[0].lower() == '!notlikethis':
                            thisTwitch.notlikethis(self.m_thisBot)   
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
                            thisAlarm.setAlarm(message.text, self.m_thisBot)
                    elif 'thanks brobot' in message.text.lower() or \
                        'thanks, brobot' in message.text.lower():
                        utils.thanks(self.m_thisBot, requester)
                    elif 'brobot' in message.text.lower().rstrip():
                        thisMarkov.talk(message.text, self.m_thisBot, self.m_groupName)

            alreadyParsed = True
            print('sleeping for 3s ', end='')
            time.sleep(3)
            try:
                self.refreshGroup()
                new_messages = self.m_thisGroup.message_count
                print('started with {0} messages, now see {1}'.format(start_messages, new_messages))
                if (new_messages - start_messages) > 0:
                    cur = cur.newer()
                    start_messages = new_messages
                    print('retrieved {0} new messages'.format(len(cur)))
                    alreadyParsed = False
            except Exception as e:
                print(e)

    def refreshGroup(self):
        groups = groupy.Group.list()
        for group in groups:
            if group.name == self.m_groupName:
                self.m_thisGroup = group
                break
        if self.m_thisGroup is None:
            print("Cannot find group {0} \n".format(groupName))
            sys.exit(0)

    def refreshBot(self):
        bots = Bot.list()
        for bot in bots:
            if self.m_thisGroup.id == bot.gorup_id:
                self.m_thisBot = bot
                break
        if self.m_thisBot is None:
            print("Cannot find bot for group {0} \n".format(groupName))
            sys.exit(0)

def main(groupName):
    myBot = startBot(groupName)
    myBot.runBot()
    sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1])