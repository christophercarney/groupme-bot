import groupy
from groupy import Bot, Group

#whenever you add a command please add it and and short description to this list, one per line
g_commandsList = {'!lastmatch': 'retrieves the last match of the current user',
                  '!lastmatch -u [USER]': 'retrieves the last match of the specified user (must be registered with !register first)',
                  '!register [NAME] [STEAM_ID]': 'registers the user to the bots steam list, STEAM_ID is the user\'s unique steam number',
                  '!roll [HIGHEST]': 'rolls a virutal dice between 1-HIGHEST, if highest is not specified, 6 is assumed',
                  '!flip': 'flips a virtual coin',
                  '![TWITCH_EMOTICON]': 'various twitch emoticons are available to use',
                  '!stats': 'prints a lot of statistics about this chat history (please use sparingly)',
                  '!commands': 'prints this list'
                  }

def commands(bot):
    character_count = 0
    message = ''

    for key in g_commandsList:
        line = '{0}: {1} \n'.format(key, g_commandsList[key])
        if len(line) + character_count > 999:
            bot.post(message)
            message = line
        else:
            message = message + line

    bot.post(message)

def thanks(bot, requester):
    bot.post('You\'re welcome, {0}.'.format(requester))