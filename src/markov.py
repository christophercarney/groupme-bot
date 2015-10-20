import pickle, random, startbot, stats, os

class markov():

    def __init__(self, groupObj, groupName):
        self.train(groupObj, groupName)

    def train(self, groupObj, groupName):
        #get all messages
        print('Checking for existing lexicon...', end='')
        if os.path.exists('..{1}cache{1}lexicon-{0}'.format(groupName, os.path.sep)):
            print('found.')
            return
        print('not found. Generating...', end='')

        stats.getAllText(groupObj, groupName)
        b=open('..{1}cache{1}messages-{0}.txt'.format(groupName, os.path.sep), encoding='utf-8')
        text=[]
        for line in b:
            for word in line.split():
                text.append (word)
        b.close()
        textset=list(set(text))
        follow={}
        for l in range(len(textset)):
            working=[]
            check=textset[l]
            for w in range(len(text)-1):
                if check==text[w] and text[w][-1] not in '(),.?!':
                    working.append(str(text[w+1]))
            follow[check]=working
        a=open('..{1}cache{1}lexicon-{0}'.format(groupName, os.path.sep),'wb')
        pickle.dump(follow,a,2)
        a.close()
        print("bot successfully trained.")

    def talk(self, message, bot, groupName):
        a=open('..{1}cache{1}lexicon-{0}'.format(groupName, os.path.sep),'rb')
        successorlist=pickle.load(a)
        a.close()
        def nextword(a):
            if a in successorlist:
                return random.choice(successorlist[a])
            else:
                return 'the'
        speech=message
        try:
            s=random.choice(speech.split())
        except:
            s = speech.split()[0]
        response=''
        while True:
            neword=nextword(s)
            response+=' '+neword
            s=neword
            if neword[-1] in ',?!.':
                break
        bot.post(response)