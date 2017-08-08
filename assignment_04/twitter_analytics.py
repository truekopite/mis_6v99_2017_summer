
# coding: utf-8

# In[1]:

import json
import requests
import operator
import itertools


# In[2]:

#The tweet link
link = 'http://kevincrook.com/utd/tweets.json'
#Putting the train file in the directory
data = requests.get(link)
tweet_file = "data_tweet.json"
#Reading the file
tweet = open(tweet_file,"wb")
tweet.write(data.content)
tweet.close()


# In[3]:

#Read the file into a dictionary
json_s = open(tweet_file).read()
json_data = json.loads(json_s)


# In[4]:

event_count = 0
tweet_count = 0
for tweet in json_data:
    #Calculating event count
    event_count +=1
    if 'text' in tweet:
        #Calculating tweet count
        tweet_count +=1


# In[5]:

#Count of each language in sorted order
lang_count = {}
for tweet in json_data:
    if 'text' in tweet:
        if 'lang' in tweet:
            lang = tweet['lang']
            if lang in lang_count:
                lang_count[lang] +=1
            else:
                lang_count[lang] = 1
lang_count = sorted(lang_count.items(),key=operator.itemgetter(1),reverse = True)


# In[6]:

#Wriiting to file
file = open("twitter_analytics.txt", 'wt', encoding = 'utf-8')
print(event_count, file = file)
print(tweet_count, file = file)
for x in lang_count:
    print(x[0], x[1], sep =',', file = file)
file.close()


# In[7]:

#Writing to file
f = open('tweets.txt', 'wt', encoding = 'utf-8')
for tweet in json_data:
    if 'text' in tweet:
        print(str(tweet['text'].encode('utf-8'))[2:-1],file = f)
f.close()

