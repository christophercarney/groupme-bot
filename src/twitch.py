import groupy
from groupy import Bot, Group
from groupy import attachments

def kappa(bot):
    kappaImage = attachments.Image.file(open('..\\assets\\kappa.png','rb'))
    bot.post(kappaImage.url)

def elegiggle(bot):
    elegiggleImage = attachments.Image.file(open('..\\assets\\elegiggle.jpg','rb'))
    bot.post(elegiggleImage.url)

def biblethump(bot):
    biblethumpImage = attachments.Image.file(open('..\\assets\\biblethump.png','rb'))
    bot.post(biblethumpImage.url)

def dansgame(bot):
    dansgameImage = attachments.Image.file(open('..\\assets\\dansgame.jpg','rb'))
    bot.post(dansgameImage.url)

def kreygasm(bot):
    kreygasmImage = attachments.Image.file(open('..\\assets\\kreygasm.jpg','rb'))
    bot.post(kreygasmImage.url)
    
def fourhead(bot):
    fourheadImage = attachments.Image.file(open('..\\assets\\4head.png','rb'))
    bot.post(fourheadImage.url)