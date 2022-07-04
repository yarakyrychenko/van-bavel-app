
import streamlit as st
from helper import *
from shillelagh.backends.apsw.db import connect
from twanalysis import *
import tweepy
from collections import Counter
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Language",
    page_icon="😮",
    layout="wide"
    )

lottie_lang= load_lottieurl('https://assets6.lottiefiles.com/packages/lf20_tnrzlN.json')
st_lottie(lottie_lang, speed=1, height=150, key="initial")

with st.sidebar:
    st.markdown("""👋 **Welcome!** Go to **Home** to enter a Twitter username. 
                Then navigate to **Language** or **Polarization** to find out how your results. 
                """)

st.title("😮 Language 😮")

if 'conn' not in st.session_state:
    st.warning("We're analyzing tweets from the President of the United States (POTUS). You can go to the homepage and add a different twitter handle.")
#elif 'df' not in st.session_state:
    #with st.spinner(text="In progress..."):
        #sheet_url = st.secrets["private_gsheets_url"]
        #query = f'SELECT * FROM "{sheet_url}"'
        #st.session_state.df = make_dataframe(st.session_state.conn.execute(query))

if "all_stopwords" not in st.session_state:
    st.session_state.all_stopwords = make_worddict("dictionaries/all_stopwords.txt")
    st.session_state.moral_emotional = make_worddict("dictionaries/moral_emotional.txt")

if "api" not in st.session_state:    
    st.session_state.api = authenticate(st.secrets["consumer_key"],
                                            st.secrets["consumer_secret"],
                                            st.secrets["access_token_key"],
                                            st.secrets["access_token_secret"])
if 'client' not in st.session_state:
    st.session_state.client = tweepy.Client(bearer_token=st.secrets["bearer_token"])

if 'name' not in st.session_state:
    st.session_state.name = "POTUS"

if 'name' in st.session_state:

    try:
        with st.spinner("We\'re retrieving tweets."):
            outtweets = get_3200_tweets(st.session_state.name,st.session_state.api,st.session_state.client, 3200)

        try:
            cat = outtweets[9]  
            st.markdown(f"We scraped {len(outtweets)} tweets from {st.session_state.name}.")
            
            with st.spinner(text='We\'re analyzing the tweets. Give it a sec...'):
                figure, all_text = make_wordcloud(st.session_state.all_stopwords, outtweets)
                n_moral_emotional = count_words(all_text, st.session_state.moral_emotional)

            st.pyplot(figure)
            st.markdown(f"On average, {st.session_state.name} used {n_moral_emotional/len(outtweets)} moral emotional words per tweet.")

                
        except:
            st.markdown("This account has fewer than 10 tweets. Tweet more and come back later or try again.")  
            
    except:
        st.markdown("This account doesn't exist. Please try again.")        
