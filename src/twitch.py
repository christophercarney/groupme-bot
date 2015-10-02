import groupy
from groupy import Bot, Group
from groupy import attachments

def kappa(bot):
    #kappa = attachments.Image.file('kappa.png')            #why doesnt this work? taken directly from api 
    #bot.post('test', loc, kappa)                          #http://groupy.readthedocs.org/en/latest/pages/advanced.html#sending-attachments
    bot.post('http://i.imgur.com/kRIBtxE.png')

def elegiggle(bot):
    bot.post('https://cdn0.gamesports.net/league_team_logos/25000/25975.jpg?1436875872')

def biblethump(bot):
    bot.post('http://www.merlinidota.com/wp-content/uploads/2014/08/BibleThump-300x300.png')

def dansgame(bot):
    bot.post('https://pbs.twimg.com/profile_images/457558207599497216/IyX7TmAC.jpeg')

def kreygasm(bot):
    bot.post('http://cs623725.vk.me/v623725040/341cc/hH8If15BQkA.jpg')