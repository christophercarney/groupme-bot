import startbot, stats, os, re, random, sys
import utils

MARKOV_LENGTH = 2

#majority of the code taken from https://github.com/hrs/markov-sentence-generator
#changes made: allowed it to hook up from the text gotten directly from messages
#changed it to be encompassed in a class structure. Made minor changes to make it Py3.X compatible

class markov():
    # These mappings can get fairly large -- they're stored globally to
    # save copying time.

    # (tuple of words) -> {dict: word -> number of times the word appears following the tuple}
    # Example entry:
    #    ('eyes', 'turned') => {'to': 2.0, 'from': 1.0}
    # Used briefly while first constructing the normalized mapping
    tempMapping = {}

    # (tuple of words) -> {dict: word -> *normalized* number of times the word appears following the tuple}
    # Example entry:
    #    ('eyes', 'turned') => {'to': 0.66666666, 'from': 0.33333333}
    mapping = {}

    # Contains the set of words that can start sentences
    starts = []

    m_botName = None

    def __init__(self, groupObj, groupName, bot):
        self.m_botName = bot.name
        self.train(groupObj, groupName)

    def train(self, groupObj, groupName):
        stats.getAllText(groupObj, groupName, self.m_botName)
        self.buildMapping(self.wordlist('..{1}cache{1}messages-{0}.txt'.format(groupName, os.path.sep)), MARKOV_LENGTH)
        utils.showOutput("bot successfully trained.")

    def talk(self, message, bot, groupName):
        try:
            bot.post(self.genSentence2(message, MARKOV_LENGTH))
        except:
            bot.post(self.genSentence(MARKOV_LENGTH))

    # We want to be able to compare words independent of their capitalization.
    def fixCaps(self, word):
        # Ex: "FOO" -> "foo"
        if word.isupper() and word != "I":
            word = word.lower()
            # Ex: "LaTeX" => "Latex"
        elif word [0].isupper():
            word = word.lower().capitalize()
            # Ex: "wOOt" -> "woot"
        else:
            word = word.lower()
        return word

    # Tuples can be hashed; lists can't.  We need hashable values for dict keys.
    # This looks like a hack (and it is, a little) but in practice it doesn't
    # affect processing time too negatively.
    def toHashKey(self, lst):
        return tuple(lst)

    # Returns the contents of the file, split into a list of words and
    # (some) punctuation.
    def wordlist(self, filename):
        f = open(filename, 'r', encoding='utf-8')
        wordlist = [self.fixCaps(w) for w in re.findall(r"[\w']+|[.,!?;]", f.read())]
        f.close()
        return wordlist

    # Self-explanatory -- adds "word" to the "tempMapping" dict under "history".
    # tempMapping (and mapping) both match each word to a list of possible next
    # words.
    # Given history = ["the", "rain", "in"] and word = "Spain", we add "Spain" to
    # the entries for ["the", "rain", "in"], ["rain", "in"], and ["in"].
    def addItemToTempMapping(self, history, word):
        while len(history) > 0:
            first = self.toHashKey(history)
            if first in self.tempMapping:
                if word in self.tempMapping[first]:
                    self.tempMapping[first][word] += 1.0
                else:
                    self.tempMapping[first][word] = 1.0
            else:
                self.tempMapping[first] = {}
                self.tempMapping[first][word] = 1.0
            history = history[1:]

    # Building and normalizing the mapping.
    def buildMapping(self, wordlist, markovLength):
        self.starts.append(wordlist [0])
        for i in range(1, len(wordlist) - 1):
            if i <= markovLength:
                history = wordlist[: i + 1]
            else:
                history = wordlist[i - markovLength + 1 : i + 1]
            follow = wordlist[i + 1]
            # if the last elt was a period, add the next word to the start list
            if history[-1] == "." and follow not in ".,!?;":
                self.starts.append(follow)
            self.addItemToTempMapping(history, follow)
        # Normalize the values in tempMapping, put them into mapping
        for first, followset in self.tempMapping.items():
            total = sum(followset.values())
            # Normalizing here:
            self.mapping[first] = dict([(k, v / total) for k, v in followset.items()])

    # Returns the next word in the sentence (chosen randomly),
    # given the previous ones.
    def next(self, prevList):
        sum = 0.0
        retval = ""
        index = random.random()
        # Shorten prevList until it's in mapping
        while self.toHashKey(prevList) not in self.mapping:
            prevList.pop(0)
        # Get a random word from the mapping, given prevList
        for k, v in self.mapping[self.toHashKey(prevList)].items():
            sum += v
            if sum >= index and retval == "":
                retval = k
        return retval

    def genSentence2(self, message, markovLength):      #attempts to use input sentence material to construct a sentence
        # Start with a random "starting word" from the input message
        splitmessage = message.lower().split()
        splitmessage.remove('{0},'.format(self.m_botName.lower()))
        if len(splitmessage) == 0:
            curr = random.choice(self.starts)
        else:
            curr = random.choice(splitmessage)

        sent = curr.capitalize()
        prevList = [curr]
        # Keep adding words until we hit a period
        while (curr not in "."):
            curr = self.next(prevList)
            prevList.append(curr)
            # if the prevList has gotten too long, trim it
            if len(prevList) > markovLength:
                prevList.pop(0)
            if (curr not in ".,!?;"):
                sent += " " # Add spaces between words (but not punctuation)
            sent += curr
        return sent

    def genSentence(self, markovLength):
        # Start with a random "starting word"
        curr = random.choice(self.starts)
        sent = curr.capitalize()
        prevList = [curr]
        # Keep adding words until we hit a period
        while (curr not in "."):
            curr = self.next(prevList)
            prevList.append(curr)
            # if the prevList has gotten too long, trim it
            if len(prevList) > markovLength:
                prevList.pop(0)
            if (curr not in ".,!?;"):
                sent += " " # Add spaces between words (but not punctuation)
            sent += curr
        return sent

