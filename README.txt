Requirements:

Python 3.4
Pillow 2.5.3 
groupyAPI
groupme api key 
steam api key
Windows or Linux (Have not tested Mac OSX but it should work on any unix-like operating system)

DETAILED INSTALL INSTRUCTIONS:
***Windows***
#ensure Python 3.4 is installed, the groupyAPI module will not work with Python 2.X or Python 3.5 >

open up a command prompt and navigate to your python install dir then:
cd Scripts
./pip3.exe install groupyAPI        #almost all windows distributions should have everything required for pillow

#follow install instructions at http://groupy.readthedocs.org/en/latest/pages/installation.html to place your GroupMe api key
#   in the right place (https://dev.groupme.com/ to get your access token from top right)
#from https://dev.groupme.com/ click bots -> create bot and fill out the required fields to your liking (callback url not 
#   required for this bot to function)  

Afterwards clone the git repo from https://github.com/crc5464/groupme-bot.git in your desired directory

#go to http://steamcommunity.com/dev/apikey and get your api key, make a file named .steam.key in the top level
#   bot dir (same folder with assets, src, cache,and place your key, make sure there are no spaces or newlines in the file


in the assets folder create a file admins-[GROUPNAME].txt will a csv of admin names e.g. John Smith,Joe Smith,Jane Doe (not required)
edit the sample steamids.txt , follow the format given, in general it is Name followed by 32bit steam id you can get this number from dota or easily from your dotabuff profile at http://www.dotabuff.com/players/[your number]
you can always dynamically register more users by using the bot commands once it starts running

change directories to the src directory and run:
python ./startbot.py [GROUPNAME FOR WHICH BOT IS REGISTERED]
(note if python isn't in your environment then you'll need to use the full path to python.exe instead of just python)


***LINUX***
start a terminal and enter the following commands:

#ensure Python 3.4 is installed, the groupyAPI module will not work with Python 2.X or Python 3.5 >
sudo apt-get install libjpeg-dev zlib1g-dev       #most linux systems will have these installed by default
sudo apt install libfreetype6-dev                 # for bare minimum installation these are required for picture creation
sudo pip3 -I install pillow==2.5.3                #important to do the above BEFORE installing pillow, if pillow is installed                                                   #  and you don't have thes, uninstall pillow then reinstall it after
sudo pip3 install groupyAPI

#follow install instructions at http://groupy.readthedocs.org/en/latest/pages/installation.html to place your GroupMe api key
#   in the right place (https://dev.groupme.com/ to get your access token from top right)
#from https://dev.groupme.com/ click bots -> create bot and fill out the required fields to your liking (callback url not 
#   required for this bot to function)  

cd [bot install dir]
git clone https://github.com/crc5464/groupme-bot.git

#go to http://steamcommunity.com/dev/apikey and get your api key, make a file named .steam.key in the top level
#   bot dir (same folder with assets, src, cache,and place your key, make sure there are no spaces or newlines in the file

cd assets
#create a file admins-[GROUPNAME].txt will a csv of admin names e.g. John Smith,Joe Smith,Jane Doe (not required)
#edit the sample steamids.txt , follow the format given, in general it is Name followed by 32bit steam id you can get this 
#   number from dota or easily from your dotabuff profile at http://www.dotabuff.com/players/[your number]
#   you can always dynamically register more users by using the bot commands once it starts running

cd ../src
python3 ./startbot.py [GROUPNAME FOR WHICH BOT IS REGISTERED]
