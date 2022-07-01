import streamlit as st
from helper import *
from shillelagh.backends.apsw.db import connect

st.set_page_config(
        page_title="Polarization",
        page_icon=""
        )

st.title("Polarization")

if 'conn' not in st.session_state:
    st.warning("Please go to the homepage and add a twitter username")
elif 'df' not in st.session_state:
    with st.spinner(text="In progress..."):
        sheet_url = st.secrets["private_gsheets_url"]
        query = f'SELECT * FROM "{sheet_url}"'
        st.session_state.df = make_dataframe(st.session_state.conn.execute(query))
if 'df' in st.session_state:        
    with st.spinner(text="In progress..."):
        figure = make_v_wordcloud(list(st.session_state.df.dem_words), list(st.session_state.df.rep_words))    
        
    st.markdown(f"#### Here is how {str(len(st.session_state.df))} people who filled out this app describe the two parties.")
    st.pyplot(figure)

    group_means = st.session_state.df.groupby("party").agg('mean')

    st.markdown("#### Feeling Thermometer Results")

    st.markdown(f"On average, Republicans who filled out this app feel {group_means.loc['Republican','dem_temp']} towards Democrats. Democrats who filled out this app feel {group_means.loc['Democrat','rep_temp']} towards Republicans.")
        
    st.markdown(f"In contrast, Republicans feel {group_means.loc['Republican','rep_temp']} towards fellow Republicans. And Democrats feel {group_means.loc['Democrat','dem_temp']} towards fellow Democrats.")
        
    #make_twitter_button()

    