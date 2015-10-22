import groupy, time, os
from groupy import Bot, Group

def getAllText(groupObj, groupName, botName):
    output_text = ''
    all_text = ''
    if os.path.exists("..{1}cache{1}messages-{0}.txt...".format(groupName, os.path.sep)):
        print("found existing messages cached, continuing lexicon generation..")
        return
    print("Compiling all messages to ..{1}cache{1}messages-{0}.txt...".format(groupName, os.path.sep))
    num_messages, initial_count = groupObj.message_count, groupObj.message_count

    start = time.time()
    cur = groupObj.messages()
    while num_messages > 0:
        for message in cur:
            if message.text is None or message.name.lower() == botName.lower():
                continue
            all_text = all_text + message.text + ' '          
        try:
            cur = cur.older()
        except: 
            pass
        num_messages = num_messages - 100
        print ('{0} messages remain'.format(num_messages))
    
    f = open('..{1}cache{1}messages-{0}.txt'.format(groupName, os.path.sep), 'w+', encoding='utf-8')
    f.write(all_text)
    f.close()
    print("completed.")

