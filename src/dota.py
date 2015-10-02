import json, groupy, urllib, time
from groupy import Bot

steam_dict = {'Patrick': '23384658', 'Christopher': '84083298', 'Kevin': '72842908', 'Joshua': '133364520'}

def lastMatch(bot, requester):
    try:
        steam_api_key = getAPIKey()
        request_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchHistory/V001/?key={0}&account_id={1}&matches_requested=1".format(steam_api_key, steam_dict[requester])
        with urllib.request.urlopen(request_url) as f:
            response = f.read().decode('utf-8')

        jsonObj = json.loads(str(response))

        match_id = jsonObj['result']['matches'][0]['match_id']

        time.sleep(1)
        request_url = "https://api.steampowered.com/IDOTA2Match_570/GetMatchDetails/V001/?key={0}&match_id={1}".format(steam_api_key, match_id)
        with urllib.request.urlopen(request_url) as f:
            response = f.read().decode('utf-8')

        jsonObj = json.loads(str(response))
        player_win = jsonObj['result']['radiant_win']
        duration = getDurationString(jsonObj['result']['duration'])
        player_slot = 0

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

        bot.post("{0} {11} a game as {1} in {2} minutes, went {3}/{4}/{5} with {6}LH/{7}DN. XPM: {8}, GPM: {9}. More details at {10}".format(
                 requester, hero, duration, kills, deaths, assists, last_hits, denies, xpm, gpm, dotabuff_url, 'won' if player_win == True else 'lost'))
                        
    except Exception as e:
        reportFailure(bot, requester, e)
        return

def reportFailure(bot, requester, exception):
    bot.post("Sorry {0}, I couldn't retrieve your last match (Unrecognized user, game mode, bad request, or steam api down). [{1}]".format(requester, exception))

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

def getAPIKey():
    f = open('../.steam.key', 'r')
    return f.readline()
    