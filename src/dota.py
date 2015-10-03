import json, groupy, urllib, time
from groupy import Bot

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

def getAPIKey():
    f = open('../.steam.key', 'r')
    return f.readline()

def populateSteamIds():
    f = open('../assets/steamids.txt', 'r')
    input = f.readline().split(' ')
    dict = {}

    for i in range(len(input) - 1):
        dict[input[i]] = input[i+1]

    return dict

def registerId(name, steamid, bot):
    f = open('../assets/steamids.txt', 'a')
    f.write(' {0} {1}'.format(name, steamid))
    f.close()

    bot.post("Steam ID {0} has been successfully registered as {1}".format(steamid, name))
    