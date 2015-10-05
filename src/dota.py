import json, groupy, urllib, time, os
from groupy import Bot, attachments
from PIL import Image, ImageDraw, ImageFont

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
        player_slot = 0
        itemsId = []
        itemsName = []
        stats_dict = {}
        stats_dict['match_id'] = match_id
        stats_dict['duration'] = getDurationString(jsonObj['result']['duration'])       
        stats_dict['steam_name'] = getSteamName(steam_api_key, steam_dict[requester])

        for player in jsonObj['result']['players']:
            if str(player['account_id']) == steam_dict[requester]:
                stats_dict['last_hits'] = player['last_hits']
                stats_dict['denies'] = player['denies']
                hero_id = player['hero_id']
                stats_dict['kills'] = player['kills']
                stats_dict['deaths'] = player['deaths']
                stats_dict['assists'] = player['assists']
                stats_dict['xpm'] = player['xp_per_min']
                stats_dict['gpm'] = player['gold_per_min']
                itemsId.append(player['item_0'])
                itemsId.append(player['item_1'])
                itemsId.append(player['item_2'])
                itemsId.append(player['item_3'])
                itemsId.append(player['item_4'])
                itemsId.append(player['item_5'])
                break
            player_slot = player_slot + 1

        if jsonObj['result']['radiant_win'] == True and player_slot <= 4:
            stats_dict['player_win'] = True  
        elif jsonObj['result']['radiant_win'] == False and player_slot > 4:
            stats_dict['player_win'] = True
        else: 
            stats_dict['player_win'] = False
        
        dotabuff_url = "http://www.dotabuff.com/matches/{0}".format(match_id)
        hero_loc, hero = getHeroNameFromId(hero_id)

        for id in itemsId:
            itemsName.append(getItemNameFromId(id).replace('item_', ''))

        imgPath = makeImage(itemsName, hero, stats_dict)
        matchImage = groupy.attachments.Image.file(open(imgPath,'rb'))
        if stats_dict['player_win'] is True:
            bot.post("Looks like {0} won! Great job bro!".format(requester), matchImage.url)
        else:
            bot.post("Rough game bro, can't win 'em all; Get back out there!".format(requester), matchImage.url)
                        
    except Exception as e:
        reportFailure(bot, requester, e)
        return

def getSteamName(apiKey, steamId32):
    steamId64 = int(steamId32) + 76561197960265728
    request_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={0}&steamids={1}'.format(apiKey, steamId64)
    print('Requesting: {0}'.format(request_url))
    time.sleep(1)
    response = urllib.request.urlopen(request_url)
    profile_data = response.read().decode('utf-8')
    jsonObj = json.loads(str(profile_data))

    try:
        return jsonObj['response']['players'][0]['personaname']
    except:
        return steamId32.__str__()

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
            return hero['localized_name'], hero['name']
    return 'Unknown Hero', 'unknown'

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

def ensureItemImageExists(itemName):
    if not os.path.exists('..{0}assets{0}items{0}'.format(os.path.sep)):
        os.mkdir('..{0}assets{0}items{0}'.format(os.path.sep))

    itemPath = '..{0}assets{0}items{0}{1}.png'.format(os.path.sep, itemName)
    print('Checking for {0} ...'.format(itemPath), end='')

    if not os.path.exists(itemPath):
        downloadUrl = 'http://cdn.dota2.com/apps/dota2/images/items/{0}_lg.png'.format(itemName)
        print('not found, downloading from {0}...'.format(downloadUrl), end='')
        urllib.request.urlretrieve(downloadUrl, itemPath)
    print('finished.')

def ensureHeroImageExists(heroName):
    if not os.path.exists('..{0}assets{0}heroes{0}'.format(os.path.sep)):
       os.mkdir('..{0}assets{0}heroes{0}'.format(os.path.sep))

    heroPath = '..{0}assets{0}heroes{0}{1}.png'.format(os.path.sep, heroName)
    print('Checking for {0} ...'.format(heroPath), end='')

    if not os.path.exists(heroPath):
        downloadUrl = 'http://cdn.dota2.com/apps/dota2/images/heroes/{0}_sb.png'.format(heroName)
        print('not found, downloading from {0}...'.format(downloadUrl), end='')
        urllib.request.urlretrieve(downloadUrl, heroPath)
    print('finished.')

def makeImage(items, hero, stats_dict):
    itemImages = []

    fullImage = Image.new('RGB', (300,200))

    #deal with the items
    for item in items:
        if item == 'unknown':
            continue
        ensureItemImageExists(item)
        cur = Image.open('..{0}assets{0}items{0}{1}.png'.format(os.path.sep, item))
        cur.thumbnail((59,33))
        itemImages.append(cur)

    #deal with the hero
    ensureHeroImageExists(hero)
    hero_im = Image.open('..{0}assets{0}heroes{0}{1}.png'.format(os.path.sep, hero))
    hero_im.thumbnail((59,33))
    fullImage.paste(hero_im, (75,60))
  
    #add items to the image
    loc_x, loc_y = 75, 100
    for im in itemImages:
        fullImage.paste(im, (loc_x, loc_y))
        loc_x = loc_x + 50
        if loc_x >= 225:
            loc_x = 75
            loc_y = loc_y + 40

    #now we add the text
    fnt = ImageFont.truetype('..{0}assets{0}{1}'.format(os.path.sep, 'arial.ttf'))
    fntBold = ImageFont.truetype('..{0}assets{0}{1}'.format(os.path.sep, 'arialbd.ttf'))
    drawing = ImageDraw.Draw(fullImage)

    drawing.text((77,15), stats_dict['steam_name'], font = fntBold, fill=(255,255,255,255))
    if stats_dict['player_win'] is True:
        drawing.text((75,30), 'Won', font=fntBold, fill=(0,255,0,255))
    else:
        drawing.text((75,30), 'Lost', font=fntBold, fill=(255,0,0,255))
    drawing.text((100,30), stats_dict['duration'], font=fnt, fill=(255,255,255,255))
    drawing.text((75,45), 'Match ID: {0}'.format(stats_dict['match_id']), font=fnt, fill=(255,255,255,255))
    drawing.text((140,60), '{0}/{1}/{2} K/D/A'.format(stats_dict['kills'], stats_dict['deaths'], stats_dict['assists']), font=fnt, fill=(255,255,255,255))
    drawing.text((140,72), '{0} LH / {1} DN'.format(stats_dict['last_hits'], stats_dict['denies']), font=fnt, fill=(255,255,255,255))
    drawing.text((140,84), '{0} GPM, {1} XPM'.format(stats_dict['gpm'], stats_dict['xpm']), font=fnt, fill=(255,255,255,255))
    
    imgPath = '..{0}cache{0}dota2_{1}.png'.format(os.path.sep, time.time())
    fullImage.save(imgPath)
    fullImage.close()
    return imgPath
    
    