import groupy
import os
from groupy import Bot, Group
from groupy import attachments

class emotes():
    
    def __init__(self):
        currentOS = os.name
        if currentOS == 'nt':
            self.filesep = '\\'
        else:
            self.filesep = '/'

    def kappa(self,bot):
        kappaImage = attachments.Image.file(open('..' + self.filesep + 'assets' + self.filesep + 'kappa.png','rb'))
        bot.post(kappaImage.url)
    
    def elegiggle(self,bot):
        elegiggleImage = attachments.Image.file(open('..' + self.filesep + 'assets' + self.filesep + 'elegiggle.jpg','rb'))
        bot.post(elegiggleImage.url)
    
    def biblethump(self,bot):
        biblethumpImage = attachments.Image.file(open('..' + self.filesep + 'assets' + self.filesep + 'biblethump.png','rb'))
        bot.post(biblethumpImage.url)
    
    def dansgame(self,bot):
        dansgameImage = attachments.Image.file(open('..' + self.filesep + 'assets' + self.filesep + 'dansgame.jpg','rb'))
        bot.post(dansgameImage.url)
    
    def kreygasm(self,bot):
        kreygasmImage = attachments.Image.file(open('..' + self.filesep + 'assets' + self.filesep + 'kreygasm.jpg','rb'))
        bot.post(kreygasmImage.url)
        
    def fourhead(self,bot):
        fourheadImage = attachments.Image.file(open('..' + self.filesep + 'assets' + self.filesep + '4head.png','rb'))
        bot.post(fourheadImage.url)