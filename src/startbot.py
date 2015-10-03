import groupy, time, sys
from groupy import Bot, Group

import stats, twitch, randomevents, dota, utils

g_thisGroup = None
g_thisBot = None
g_admins = ['Christopher', 'Patrick']

def main(groupName):
    refreshGroup(groupName)
    refreshBot()

    cur = g_thisGroup.messages()
    start_messages = g_thisGroup.message_count
    alreadyParsed = True
    
    thisTwitch = twitch.emotes()
    while True:
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
                    if command[0] == '!stats':
                        stats.stats(g_thisBot, g_thisGroup)
                    elif command[0].lower() == '!kappa':
                        thisTwitch.kappa(g_thisBot)
                    elif command[0].lower() == '!elegiggle':
                        thisTwitch.elegiggle(g_thisBot)                        
                    elif command[0].lower() == '!biblethump':
                        thisTwitch.biblethump(g_thisBot)
                    elif command[0].lower() == '!dansgame':
                        thisTwitch.dansgame(g_thisBot)
                    elif command[0].lower() == '!kreygasm':
                        thisTwitch.kreygasm(g_thisBot)
                    elif command[0].lower() == '!4head':
                        thisTwitch.fourhead(g_thisBot)
                    elif command[0] == '!roll':
                        try:
                            range = int(command[1])
                            randomevents.roll(g_thisBot, requester, range=range+1)
                        except:
                            randomevents.roll(g_thisBot, requester)
                    elif command[0] == '!flip':
                        randomevents.flip(g_thisBot, requester)
                    elif command[0] == '!lastmatch':
                        if '-u' in message.text:
                            try:
                                dota.lastMatch(g_thisBot, command[2])
                            except:
                                g_thisBot.post("Couldn't understand command:{0} {1} {2}, please see !commands for usage".format(command[0], command[1], command[2]))
                        else:
                            dota.lastMatch(g_thisBot, requester)
                    elif command[0] == '!register':
                        try:
                            dota.registerId(command[1], command[2], g_thisBot)
                        except:
                            g_thisBot.post('Couldn\'t understand !register command, use !commands for usages')
                    elif command[0] == '!commands':
                        utils.commands(g_thisBot)
                    elif command[0] == '!stop':
                        sys.exit(0) if requester in g_admins else None
                elif 'thanks brobot' in message.text.lower() or \
                    'thanks, brobot' in message.text.lower() or \
                    'thanks bro bot' in message.text.lower() or \
                    'thanks, bro bot' in message.text.lower():
                    utils.thanks(g_thisBot, requester)
					
        alreadyParsed = True
        print('sleeping for 3')
        time.sleep(3)
        try:
            refreshGroup(groupName)
            new_messages = g_thisGroup.message_count
            print('started with {0} messages, now see {1}'.format(start_messages, new_messages))
            if (new_messages - start_messages) > 0:
                cur = cur.newer()
                start_messages = new_messages
                print('retrieved {0} new messages'.format(len(cur)))
                alreadyParsed = False
        except Exception as e:
            print(e)

def refreshGroup(groupName):
    groups = groupy.Group.list()
    for group in groups:
        if group.name == groupName:
            global g_thisGroup
            g_thisGroup = group
            break

    if g_thisGroup is None:
        print("Cannot find group {0} \n".format(groupName))
        sys.exit(0)

def refreshBot():
    bots = Bot.list()
    for bot in bots:
        if g_thisGroup.id == bot.gorup_id:
            global g_thisBot
            g_thisBot = bot
            break

    if g_thisBot is None:
        print("Cannot find bot for group {0} \n".format(groupName))
        sys.exit(0)

if __name__ == '__main__':
    main(sys.argv[1])
    #main("Test")