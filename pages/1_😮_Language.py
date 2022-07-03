
import streamlit as st
from helper import *
from shillelagh.backends.apsw.db import connect
from twanalysis import *
from collections import Counter

st.set_page_config(
    page_title="Language",
    page_icon="😮",
    layout="wide"
    )

with st.sidebar:
    st.markdown("""👋 **Welcome!** Go to **Home** to enter a Twitter username. 
                Then navigate to **Language** or **Polarization** to find out how your results. 
                """)

st.title("😮 Language 😮")

if 'conn' not in st.session_state:
    st.warning("Please go to the homepage and add a twitter username")
elif 'df' not in st.session_state:
    with st.spinner(text="In progress..."):
        sheet_url = st.secrets["private_gsheets_url"]
        query = f'SELECT * FROM "{sheet_url}"'
        st.session_state.df = make_dataframe(st.session_state.conn.execute(query))

if "all_stopwords" not in st.session_state:
     st.session_state.all_stopwords = make_worddict("dictionaries/all_stopwords.txt")
     st.session_state.moral_emotional = make_worddict("dictionaries/moral_emotional.txt")

if "api" not in st.session_state:    
            st.session_state.api = authenticate(st.secrets["consumer_key"],
                                            st.secrets["consumer_secret"],
                                            st.secrets["access_token_key"],
                                            st.secrets["access_token_secret"])

if 'df' in st.session_state:
    #try:
    outtweets = get_user_tweeets(st.session_state.name,st.session_state.api)
        #try:
    cat = outtweets[9]  
            
    with st.spinner(text='We\'re analyzing the tweets. Give it a sec...'):
        figure, all_text = make_wordcloud(st.session_state.all_stopwords, outtweets)
        #n_moral_emotional = count_words(all_text, st.session_state.moral_emotional)

    counter = Counter(all_text) 
    keys = counter.keys()
    st.write(keys)
    total = 0
    for word in dict:
        word = word.split("*")[0]
        numbers = [counter[key] for key in keys if key.startswith(word)]
        st.write(numbers)
        total += sum(numbers)
    st.write(len(all_text.split()))
    st.write(total)
    #st.pyplot(figure)
    #st.markdown(f"{n_moral_emotional/len(all_text.split())}\% of words you used are moral emotional.")

                
        #except:
          #  st.markdown("This account has fewer than 10 tweets. Tweet more and come back later or try again.")  
            
    #except:
         #   st.markdown("This account doesn't exist. Please try again.")        
