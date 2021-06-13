#!/usr/bin/env python
# coding: utf-8

# In[1]:


import io
import random
import string # to process standard python strings
import warnings
from datetime import datetime
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')


# In[2]:





# In[3]:


import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only


# In[4]:


f=open('chatbot.txt','r',errors = 'ignore')
raw=f.read()
raw = raw.lower()# converts to lowercase


# In[5]:


sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words


# In[6]:


lemmer = nltk.stem.WordNetLemmatizer()
#WordNet is a semantically-oriented dictionary of English included in NLTK.
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# In[7]:


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey","how are you?")
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
 
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# In[8]:



DATE_INPUT = ("today's date", "current date", "date today","date","can you tell me today's date?")
#DATE_OUTPUT = [(dt_date.strftime("%A, %d %b %Y"))]

def date(date_now):
   for word in date_now.split():
       if word.lower() in DATE_INPUT:
           dt_date = datetime.now()
           return (dt_date.strftime("%d %b %Y"))


# In[9]:


DAY_INPUT = ("today's day", "current day", "day today","day","can you tell me which day is today?")
#DATE_OUTPUT = [(dt_date.strftime("%A, %d %b %Y"))]

def day(day_now):
    for word in day_now.split():
        if word.lower() in DAY_INPUT:
            dt_date = datetime.now()
            return (dt_date.strftime("%A"))


# In[10]:

TIME_INPUT = ("time", "current time", "time now","can you tell me what time is it?", "tell me the time")
#DATE_OUTPUT = [(dt_date.strftime("%A, %d %b %Y"))]

def time(time_now):
    for word in time_now.split():
        if word.lower() in TIME_INPUT:
            now = datetime.now()
            dt_string = now.strftime("%H:%M:%S")
            return dt_string

import wikipedia
#QUERY_INPUT = ("search wiki about","wiki search","wikipedia search")
def query(wiki):
    for word in wiki.split():
        if "wiki search" in wiki:
            n = 2
            wiki = wiki.replace("wikipedia","")
            text = (wikipedia.summary(wiki,sentences=n))
            return text

import pywhatkit as kit
#SEARCH_INPUT = ("search google about","google search about", "google search")
def srch(search):
    for word in search.split():
        if "google search" in search:
            search = search.replace("google search","\b")
            return kit.search(search)

import randfacts
FACTS_INPUT=("tell me some facts", "facts", "can you tell me some facts?", "tell me facts")
def fact(facts):
    for word in facts.split():
        if word.lower() in FACTS_INPUT:
            facts = randfacts.getFact(True)
            return facts

from textblob import TextBlob

HAPPY_RESPONSES = ("I'm glad to hear that!", "Oh! Good", "I'm happy that you're happy")
SAD_RESPONSES = ("Sorry to hear that, would a joke make you feel better?", "Oh no! It may not be much, but let me know if there is anything  can do for you","I'm sorry to hear that")
def emot(em):
    #for word in em.split():
     #   if word.lower() in em:
    feedback_polarity = TextBlob(em).sentiment.polarity
    if feedback_polarity > 0:
        return random.choice(HAPPY_RESPONSES)
    elif feedback_polarity < 0:
        return random.choice(SAD_RESPONSES)
    else:
        return

import pyjokes

JOKE_INPUTS = ("tell me a joke", "tell me joke")
def jokes(joke):
    for word in joke.split():
        if word.lower() in joke:
            if "joke" in joke:
                return pyjokes.get_joke()
            elif (("yes" in joke)):
                return pyjokes.get_joke()
            elif (("no" in joke)):
                return "ok"

# In[11]:

NEWS_INPUT = ("news", "trending news", "top 5 news", "show me the news", "top news")

def newsTrending(news_now):
    for word in news_now.split():
        if word.lower() in NEWS_INPUT:
            if "news" in news_now:
                news_url="https://news.google.com/news/rss"
                root = urlopen(news_url)
                xml_page = root.read()
                root.close()
                soup_page = soup(xml_page,"xml")
                news_list = soup_page.findAll("item")
                str="  "
                for news in news_list[:5]:
                    headlines = news.title.text
                    str = str + " \n\n " + headlines
                return str
                


# In[12]:


'''
import emoji
import demoji
EMOJI_INPUTS = (":smiling_face_with_smiling_eyes:", ":grinning_face:", ":grinning_face_with_big_eyes:", ":beaming_face_with_smiling_eyes:", ":smiling_face_with_smiling_eyes:","I am happy", "happy")
EMOJI_RESPONSES = ["\U0001F600", "\U0001F603", "\U0001F604", "\U0001F601", "Someone's having a great day \U0001F600", "What a sweetie","\U0001F60A"]

def happy(happy_emoji):
 
    for word in happy_emoji.split():
        if "happy" in EMOJI_INPUTS:
            return random.choice(EMOJI_RESPONSES)
        if emoji.demojize(happy_emoji) in EMOJI_INPUTS:
            return random.choice(EMOJI_RESPONSES) 
'''

# In[13]:


def response(msg):
    robo_response=''
    sent_tokens.append(msg)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


# In[ ]:





# In[14]:



'''flag=True
print("ALICE: My name is Alice. How can I help you?")
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ALICE: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("ALICE: "+greeting(user_response))
            elif(date(user_response)!=None):
                print("ALICE: "+date(user_response))
            elif(day(user_response)!=None):
                print("ALICE: "+day(user_response))
            elif(happy(user_response)!=None):
                emoji.demojize(user_response)
                print("ALICE: "+happy(user_response))
            else:
                print("ALICE: ",end="")
                print(response(user_response))
                sent_tokens.remove(user_response)
    else:
        flag=False
        print("ALICE: Bye! take care..")
'''


# In[15]:


bot_name = "ALICE"

def get_response(msg):
    
    msg=msg.lower()
    if(msg!='bye'):
        if(msg=='thanks' or msg=='thank you' ):
            return "You are welcome.."
        else:
            if(greeting(msg)!=None):
                return (greeting(msg))
            elif(date(msg)!=None):
                return (date(msg))
            elif(day(msg)!=None):
                return (day(msg))
            elif(time(msg)!=None):
                return (time(msg))
            #elif(happy(msg)!=None):
                #emoji.demojize(msg)
            #    print(happy(msg))
            elif(newsTrending(msg)!=None):
                return(newsTrending(msg))
            elif(fact(msg)!=None):
                return (fact(msg))
            elif(srch(msg)!=None):
                return(srch(msg))
            elif(query(msg)!=None):
                return(query(msg))
            elif(jokes(msg)!=None):
                return (jokes(msg))
            elif(emot(msg)!=None):
                return (emot(msg))
            


            #elif(happy(msg)!=None):
            #    return (happy(msg))
            else:
                #sent_tokens.remove(msg)
                return response(msg)
                            
                
    else:
        return "Bye! take care.."


# In[ ]:





# %%
