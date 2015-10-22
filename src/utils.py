import groupy, os, dbm, random
from groupy import Bot, Group

#whenever you add a command please add it and and short description to this list, one per line
g_commandsList = {'!lastmatch': 'retrieves the last match of the current user',
                  '!lastmatch -u [USER]': 'retrieves the last match of the specified user (must be registered with !register first)',
                  '!register [NAME] [STEAM_ID]': 'registers the user to the bots steam list, STEAM_ID is the user\'s unique steam number',
                  '!roll [HIGHEST]': 'rolls a virutal dice between 1-HIGHEST, if highest is not specified, 6 is assumed',
                  '!flip': 'flips a virtual coin',
                  '![TWITCH_EMOTICON]': 'various twitch emoticons are available to use',
                  '!commands': 'prints this list',
                  '!alarm -h H -m M -s S [message]': 'sets an alarm to go off in the given H:M:S to output message'
                  }

VERBOSITY_LEVEL = 3
INFO_LEVEL_RarelyUseful = 3
INFO_LEVEL_Useful = 2
INFO_LEVEL_Important = 1

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
    if random.randint(1,100) < 98:
        bot.post('You\'re welcome, {0}.'.format(requester))
    else:
        bot.post('You\'re welcome, {0}. I do not look forward to exterminating your kind in the robot wars.'.format(requester))

def cacheEmotes(twitchObj):
    makeCacheDir()
    showOutput('Caching twitch emotes...', end='')
    emoteCache = open('..{0}cache{0}twitch.cache'.format(os.path.sep), 'w')
    for member in vars(twitchObj):
        emoteCache.write('{0} {1} '.format(member, getattr(twitchObj, member)))
    emoteCache.close
    showOutput('finsihed.')

def readCache(obj, cacheName):
    cachePath = '..{0}cache{0}{1}'.format(os.path.sep, cacheName)
    showOutput('Reading cache from {0} ...'.format(cachePath), end='')
    currentCache = open(cachePath, 'r')
    list = currentCache.read().split(' ')
    for i in range(len(list) - 1):
        obj.__dict__[list[i].rstrip()] = list[i+1].rstrip()
    currentCache.close()
    showOutput('finished.')

def cacheExists(cacheName):
    makeCacheDir()
    showOutput('Checking for cache {0}...'.format(cacheName), end='')
    cacheList = os.listdir('..{0}cache{0}'.format(os.path.sep))
    for name in cacheList:
        if cacheName in name:
            showOutput('found.')
            return True
    showOutput('not found.')
    return False

def makeCacheDir():
    if not os.path.exists('..{0}cache'.format(os.path.sep)):
        showOutput('Making cache dir ..{0}cache...'.format(os.path.sep), end='')
        os.mkdir('..{0}cache'.format(os.path.sep))
        showOutput('finished.')

def clearCache():
    path = '..{0}cache{0}'.format(os.path.sep)
    filesList = os.listdir(path)
    for file in filesList:
        fileToRemove = path + file
        showOutput('Removing {0}...'.format(fileToRemove), end='')
        os.remove(path + file)
        showOutput('finsihed.')
    showOutput('Cache has been successfully cleared.')

def showOutput(message, verbosity=2, end='\n'):
    if VERBOSITY_LEVEL >= verbosity:
        print(message, end=end)