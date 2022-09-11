import streamlit as st
import pandas as pd
from helper import *
from streamlit_lottie import st_lottie

import requests
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

st.set_page_config(
        page_title="Polarization",
        page_icon="🔥",
        layout="wide"
        )
        
lottie_pol = load_lottieurl('https://assets3.lottiefiles.com/packages/lf20_t2xm9bsw.json')
st_lottie(lottie_pol, speed=1, height=150, key="initial")


with st.sidebar:
    st.markdown("""👋 **Welcome!** Go to **Home** to enter a Twitter username. 
                Then navigate to **Language** or **Polarization** to find out how your results. 
                """)


st.title("🔥 Polarization 🔥")

if 'collection' not in st.session_state:
    st.warning("Please go to the homepage and add a twitter username")
elif 'df' not in st.session_state:
    with st.spinner(text="In progress..."):
        cols = ['_id', "id", "twitter_username", "party", "dem_words", "rep_words", "dem_temp", "rep_temp","username_mine"]
        list1 = []
        for row in st.session_state.collection.find():
            list1.append(list(row.values()))
        df = pd.DataFrame(list1, columns = cols)
        st.session_state.df = df.drop(['_id',"id","twitter_username","username_mine"],axis=1)

if 'df' in st.session_state:        
    with st.spinner(text="In progress..."):
        figure = make_v_wordcloud(list(st.session_state.df.dem_words), list(st.session_state.df.rep_words))    
        
    st.markdown(f"#### Here is how the {str(len(st.session_state.df))} people who filled out this app describe and feel about the two parties.")

    group_means = st.session_state.df.groupby("party").agg('mean')
    st.markdown(f"On average, Republicans who filled out this app feel {round(group_means.loc['Republican','dem_temp'],2)}/100 towards Democrats. Democrats who filled out this app feel {round(group_means.loc['Democrat','rep_temp'])}/100 towards Republicans.")
        
    st.markdown(f"In contrast, Republicans feel {round(group_means.loc['Republican','rep_temp'])}/100 towards fellow Republicans. And Democrats feel {round(group_means.loc['Democrat','dem_temp'],2)}/100 towards fellow Democrats.")
    
    st.pyplot(figure)
  
    #make_twitter_button()

    