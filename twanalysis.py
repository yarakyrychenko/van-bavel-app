from socket import if_nameindex
import matplotlib.pyplot as plt 
import tweepy, re
from wordcloud import WordCloud
from collections import Counter

def make_worddict(file_name):
    text_file = open(file_name, "r")
    stopwords_list = text_file.read().split("\n")
    text_file.close()
    return set(stopwords_list)
     
def authenticate(consumer_key, consumer_secret,access_token_key, access_token_secret):    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    return api

def get_user_tweeets(screen_name,api):
    alltweets = [] 
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    outtweets = [tweet.text for tweet in alltweets] 
    return outtweets

def preprocess(out):
    text = " ".join(out)
    text = re.sub(pattern=r"http\S+",repl="",string=text.lower())
    text = re.sub(pattern=r"@\S+",repl="",string=text)
    return text


def make_wordcloud(st_words, out):
    text = preprocess(out)
    wordcloud = WordCloud(width=1800, height=1200,stopwords=st_words,
                        max_font_size=250, max_words=100, background_color="white",
                        colormap='cool', collocations=True).generate(text)  

    fig = plt.figure(figsize=(18,12))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    return fig, text

def count_words(all_text,dict):
    counter = Counter(all_text) 
    keys = counter.keys()
    total = 0
    for word in dict:
        word = word.split("*")[0]
        numbers = [counter[key] for key in keys if key.startswith(word)]
        total += sum(numbers)
    return total