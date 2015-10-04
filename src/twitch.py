import groupy, os, utils
from groupy import Bot, Group
from groupy import attachments


class emotes():
    
    m_kappaImage = None
    m_elegiggleImage = None
    m_biblethumpImage = None
    m_dansgameImage = None
    m_kreygasm = None
    m_fourheadImage = None
    m_pogchampImage = None

    def __init__(self):
        if utils.cacheExists('twitch.cache'):
            utils.readCache(self, 'twitch.cache')
        else:
            self.m_kappaImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + 'kappa.png','rb')).url
            self.m_elegiggleImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + 'elegiggle.jpg','rb')).url
            self.m_biblethumpImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + 'biblethump.png','rb')).url
            self.m_dansgameImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + 'dansgame.jpg','rb')).url
            self.m_kreygasmImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + 'kreygasm.jpg','rb')).url
            self.m_fourheadImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + '4head.png','rb')).url
            self.m_pogchampImage = attachments.Image.file(open('..' + os.path.sep + 'assets' + os.path.sep + 'pogchamp.jpg','rb')).url
            utils.cacheEmotes(self)

    def kappa(self,bot):        
        bot.post(self.m_kappaImage)
    
    def elegiggle(self,bot):       
        bot.post(self.m_elegiggleImage)
 
    def biblethump(self,bot):
        bot.post(self.m_biblethumpImage)
           
    def dansgame(self,bot):
        bot.post(self.m_dansgameImage)
   
    def kreygasm(self,bot):     
        bot.post(self.m_kreygasmImage)
       
    def fourhead(self,bot):      
        bot.post(self.m_fourheadImage)
        
    def pogchamp(self,bot):
        post.post(self.m_pogchampImage)