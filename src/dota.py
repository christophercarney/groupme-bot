import json, groupy, urllib, time, os
from groupy import Bot, attachments
from PIL import Image

def lastMatch(bot, requester):
    try:
        steam_dict = populateSteamIds()

        steam_api_key = getAPIKey()
        request_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={0}&account_id={1}&matches_requested=1".format(steam_api_key, steam_dict[requester])
        print('Requesting: {0}'.format(request_url))
        response = urllib.request.urlopen(request_url)
        last_match_info = response.read().decode('utf-8')

        jsonObj = json.loads(str(last_match_info))

        if jsonObj['result']['status'] == 15:
            reportFailure(bot, requester, jsonObj['result']['statusDetail'])
            return
        else:
            match_id = jsonObj['result']['matches'][0]['match_id']

        time.sleep(1)
        request_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key={0}&match_id={1}".format(steam_api_key, match_id)
        print('Requesting: {0}'.format(request_url))
        response2 = urllib.request.urlopen(request_url)
        last_match = response2.read().decode('utf-8')

        jsonObj = json.loads(str(last_match))
        player_win = jsonObj['result']['radiant_win']
        duration = getDurationString(jsonObj['result']['duration'])
        player_slot = 0
        itemsId = []
        itemsName = []

        for player in jsonObj['result']['players']:
            if str(player['account_id']) == steam_dict[requester]:
                last_hits = player['last_hits']
                denies = player['denies']
                hero_id = player['hero_id']
                kills = player['kills']
                deaths = player['deaths']
                assists = player['assists']
                xpm = player['xp_per_min']
                gpm = player['gold_per_min']
                itemsId.append(player['item_0'])
                itemsId.append(player['item_1'])
                itemsId.append(player['item_2'])
                itemsId.append(player['item_3'])
                itemsId.append(player['item_4'])
                itemsId.append(player['item_5'])
                break
            player_slot = player_slot + 1

        if jsonObj['result']['radiant_win'] == True and player_slot <= 4:
            player_win = True  
        elif jsonObj['result']['radiant_win'] == False and player_slot > 4:
            player_win = True
        else: 
            player_win = False
        
        dotabuff_url = "http://www.dotabuff.com/matches/{0}".format(match_id)
        hero = getHeroNameFromId(hero_id)

        for id in itemsId:
            itemsName.append(getItemNameFromId(id).replace('item_', ''))

        imgPath = makeImage(itemsName)
        itemsImage = groupy.attachments.Image.file(open(imgPath,'rb'))

        bot.post("{0} {11} a game as {1} in {2} minutes, went {3}/{4}/{5} K/D/A with {6}LH/{7}DN. XPM: {8}, GPM: {9}. {10}".format(
                 requester, hero, duration, kills, deaths, assists, last_hits, denies, xpm, gpm, dotabuff_url, 'won' if player_win == True else 'lost'))
        time.sleep(1)
        bot.post(itemsImage.url)
                        
    except Exception as e:
        reportFailure(bot, requester, e)
        return

def reportFailure(bot, requester, exception):
    bot.post("Sorry, I couldn't retrieve {0}'s last match (unrecognized user, game mode, bad request, or steam api down). [{1}]".format(requester, exception))

def getDurationString(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def getHeroNameFromId(id):
    f = open('../assets/heroes.json', 'r')
    jsonObj = json.load(f)

    for hero in jsonObj['heroes']:
        if hero['id'] == id:
            return hero['localized_name']
    return 'Unknown Hero'

def getItemNameFromId(id):
    f = open('../assets/items.json', 'r')
    jsonObj = json.load(f)

    for item in jsonObj['result']['items']:
        if item['id'] == id:
            return item['name']
    return 'unknown'

def getAPIKey():
    f = open('../.steam.key', 'r')
    return f.readline().rstrip()

def populateSteamIds():
    f = open('../assets/steamids.txt', 'r')
    input = f.readline().split(' ')
    dict = {}

    for i in range(len(input) - 1):
        dict[input[i].rstrip()] = input[i+1].rstrip()

    return dict

def registerId(name, steamid, bot):
    f = open('../assets/steamids.txt', 'a')
    f.write(' {0} {1}'.format(name, steamid))
    f.close()

    bot.post("Steam ID {0} has been successfully registered as {1}".format(steamid, name))

def ensureImageExists(itemName):
    if not os.path.exists('..{0}assets{0}items{0}'.format(os.path.sep)):
        os.mkdir('..{0}assets{0}items{0}'.format(os.path.sep))

    itemPath = '..{0}assets{0}items{0}{1}.png'.format(os.path.sep, itemName)
    print('Checking for {0} ...'.format(itemPath), end='')

    if not os.path.exists(itemPath):
        downloadUrl = 'http://cdn.dota2.com/apps/dota2/images/items/{0}_lg.png'.format(itemName)
        print('not found, downloading from {0}...'.format(downloadUrl), end='')
        urllib.request.urlretrieve(downloadUrl, itemPath)
    print('finished.')

def makeImage(items):
    itemImages = []
    fullImage = Image.new('RGB', (600,300))
    for item in items:
        ensureImageExists(item)
        cur = Image.open('..{0}assets{0}items{0}{1}.png'.format(os.path.sep, item))
        cur.thumbnail((100,75))
        itemImages.append(cur)
    
    loc_x = 150
    loc_y = 100
    for im in itemImages:
        fullImage.paste(im, (loc_x, loc_y))

        loc_x = loc_x + 100
        if loc_x >= 450:
            loc_x = 150
            loc_y = loc_y + 75

    imgPath = '..{0}cache{0}dota2_{1}.png'.format(os.path.sep, time.time())
    fullImage.save(imgPath)
    fullImage.close()
    return imgPath
    
    