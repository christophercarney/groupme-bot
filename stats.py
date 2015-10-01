import groupy, time
from groupy import Bot, Group

ignored_words = ['', 'its', 'the', 'it\'s', 'they', 'them', 'he', 'she', 'we', 'i', 'it', 'so', 'to', 'a', 'at', 'isn\'t', 
                 'i\'ve', 'you\'ve', 'this', 'on', 'how', 'be', 'wasn\'t', 'for', 'weren\'t', '0', '1', '2', '3', '4', '5',
                 '6', '7', '8', '9', '10', '11', '12', 'thats', 'got', 'im', 'id', 'that', 'we\'re', 'is', 'i\'m', 'my', 'their', 
                 'they\'re', 'there', 'of', 'just', 'you\'d', 'do', 'you', 'ill', 'u', 'b', 'and', 'like', 'but']

month_names = ['null', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']

day_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def stats(broBot, brothers):
    people = []
    word_dict = {}
    posters = {}
    likes = {}
    likers = {}
    pictures = {}

    months_2015 = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0}
    months_2014 = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0}

    hours = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, "8": 0, "9": 0, "10": 0, "11": 0, "12": 0, 
             "13": 0, "14": 0, "15": 0, "16": 0, "17": 0, "18": 0, "19": 0, "20": 0, "21": 0, "22": 0, "23": 0, "0": 0}
    days = {"0": 0, "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}

    output_text = ''

    num_messages, initial_count = brothers.message_count, brothers.message_count

    start = time.time()
    cur = brothers.messages()
    while num_messages > 0:
        for message in cur:

            if message.name not in posters:
                people.append(message.name)
                posters[message.name] = 1
            elif posters[message.name] >= 1:
                posters[message.name] = posters[message.name] + 1

            if len(message.likes()) > 0:
                try:
                    likes[message.name] = likes[message.name] + 1
                except:
                    likes[message.name] = 1

                for liker in message.likes():
                    try:
                        likers[str(liker)] = likers[str(liker)] + 1
                    except:
                        likers[str(liker)] = 1

            if len(message.attachments) > 0:
                if message.attachments[0].type == 'image':
                    try:
                        pictures[message.name] = pictures[message.name] + 1
                    except:
                        pictures[message.name] = 1

            if message.created_at.year == 2014:
                months_2014[str(message.created_at.month)] = months_2014[str(message.created_at.month)] + 1
            else:
                months_2015[str(message.created_at.month)] = months_2015[str(message.created_at.month)] + 1

            hours[str(message.created_at.hour)] = hours[str(message.created_at.hour)] + 1
            days[str(message.created_at.weekday())] = days[str(message.created_at.weekday())] + 1


            if message.text is None:
                continue
            text = message.text.lower()
            text = text.replace('"', ' ')
            text = text.replace('!', ' ')
            text = text.replace('?', ' ')
            text = text.replace('.', ' ')
            text = text.replace(',', ' ')
            text = text.replace('(', ' ')
            text = text.replace(')', ' ')
            text = text.replace('=', ' ')
            text = text.replace('#', ' ')
            text = text.replace('\'s', ' ')
            text = text.replace('@', ' ')
            text = text.replace(';', ' ')

            text = text.split(' ')
            
            for word in text:
                if word not in ignored_words and word not in word_dict:
                    word_dict[word] = 1
                elif word not in ignored_words and word_dict[word] >= 1:
                    word_dict[word] = word_dict[word] + 1

        try:
            cur = cur.older()
        except: 
            pass
        num_messages = num_messages - 100
        print ('{0} messages remain'.format(num_messages))

    end = time.time()

    for key, value in word_dict.items():
        while value > 0:
            output_text = output_text + key + '\n'
            value = value - 1

    f = open('./words.txt', 'w', encoding='utf-8')
    f.write(output_text)
    f.close

    stats_text = ''
    for person in people:
        if person in posters:
            stats_text = stats_text + "{0} has posted {1} times \n".format(person, posters[person])
    stats_text = stats_text + '\n^^^'

    for person in people:
        if person in likers:
            stats_text = stats_text + "{0} has liked {1} messages \n".format(person, likers[person])
    stats_text = stats_text + '\n^^^'

    for person in people:
        if person in likes:
            stats_text = stats_text + "{0} has {1} likes accross all messages \n".format(person, likes[person])
    stats_text = stats_text + '\n^^^'

    for person in people:
        if person in pictures:
            stats_text = stats_text + "{0} has posted {1} images \n".format(person, pictures[person])
    stats_text = stats_text + '\n^^^'

    sorted_months = sorted(months_2014.items(), key=lambda x: x[1])
    stats_text = stats_text + "---2014---\n"
    for result in reversed(sorted_months):
        if result[1] == 0:
            continue
        stats_text = stats_text + "{0} messages were posted in {1} \n".format(result[1], month_names[int(result[0])])
    stats_text = stats_text + '\n^^^'

    sorted_months = sorted(months_2015.items(), key=lambda x: x[1])
    stats_text = stats_text + "---2015---\n"
    for result in reversed(sorted_months):
        if result[1] == 0:
            continue
        stats_text = stats_text + "{0} messages were posted in {1} \n".format(result[1], month_names[int(result[0])])
    stats_text = stats_text + '\n^^^'

    sorted_days = sorted(days.items(), key=lambda x: x[1])
    for result in reversed(sorted_days):
        stats_text = stats_text + "{0} messages were posted on {1} \n".format(result[1], day_names[int(result[0])])
    stats_text = stats_text + '\n^^^'

    sorted_hours = sorted(hours.items(), key=lambda x: x[1])
    for result in reversed(sorted_hours):
        stats_text = stats_text + "{0} messages were posted at {1} hrs\n".format(result[1], result[0])
    stats_text = stats_text + '\n^^^'

    stats_text = stats_text + 'total messages parsed: {0} \ntook {3} seconds \ncreated on {1} \nlast updated {2}'.format(initial_count, brothers.created_at, brothers.updated_at, end-start)

    f = open('./stats.txt', 'w')
    f.write(stats_text)
    f.close()

    sections = stats_text.split('^^^')
    broBot.post('Hey dudes, got some SICK data for you!')
    count = 0
    total = len(sections)
    for s in sections:
        broBot.post("{0}({1}/{2})".format(s, count+1, total))
        print("{0}({1}/{2})".format(s, count+1, total))
        count = count + 1

    f = open('./word_dict.txt', 'w', encoding='utf-8')
    f.write(str(word_dict))
    f.close

    print ("...finished")
    

