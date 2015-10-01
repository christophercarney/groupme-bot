import groupy
from groupy import Bot, Group
from groupy import attachments

def kappa(bot):
    #kappa = attachments.Image.file('kappa.png')            #why doesnt this work? taken directly from api 
    #bot.post('test', loc, kappa)                          #http://groupy.readthedocs.org/en/latest/pages/advanced.html#sending-attachments

    bot.post('http://i.imgur.com/kRIBtxE.png')