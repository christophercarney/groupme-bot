import groupy, time, sys
from groupy import Bot, Group

import stats, kappa

g_thisGroup = None
g_thisBot = None

def main(groupName):
    refreshGroup(groupName)
    refreshBot()

    cur = g_thisGroup.messages()
    start_messages = g_thisGroup.message_count
    alreadyParsed = True
    while True:
        if alreadyParsed == False:
            for message in cur:
                print('recieved message {0} ({1})\n'.format(message.text, message.created_at))
                if message.text[0] == '!':
                    command = message.text.split(' ')
                    if command[0] == '!stats':
                        stats.stats(g_thisBot, g_thisGroup)
                    elif command[0] == '!kappa':
                        kappa.kappa(g_thisBot)
        alreadyParsed = True
        print('sleeping for 5 \n')
        time.sleep(5)
        try:
            refreshGroup(groupName)
            new_messages = g_thisGroup.message_count
            print('started with {0} messages, now see {1}'.format(start_messages, new_messages))
            if (new_messages - start_messages) > 0:
                cur = cur.newer()
                start_messages = new_messages
                print('retrieved {0} new messages \n'.format(len(cur)))
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
    main('Brothers')