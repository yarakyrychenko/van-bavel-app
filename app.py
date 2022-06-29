import streamlit as st
from shillelagh.backends.apsw.db import connect
from datetime import datetime
from uuid import uuid4

st.title(" Are you partisan? ") 
st.subheader("See how you and other twitter users see each party visualized in wordclouds ")
st.text_input("Enter a twitter username to begin", key="name")
st.session_state.party = st.radio(
     "How do you identify?",
     ('Independant','Republican', 'Democrat'))

dem_words = []
st.text("Please add five words that describe Democrats best in your opinion:")
for i in range(5):
    dem_words.append(st.text_input("D"+str(i+1)))
st.session_state.dem_words = ", ".join(dem_words)
st.text(f"your words are {st.session_state.dem_words}")

rep_words = []
st.text("Please add five words that describe Republicans best in your opinion:")
for i in range(5):
    rep_words.append(st.text_input("R"+str(i+1),key = "R"+str(i+1)))
st.session_state.rep_words = ", ".join(rep_words)
st.text(f"your words are {st.session_state.rep_words}")

if st.button("Submit", key='submit'):
    st.session_state.id = datetime.now().strftime('%Y%m-%d%H-%M-') + str(uuid4())

    conn = connect(":memory:", 
               adapter_kwargs = {
                   "gsheetsapi": { 
                       "service_account_info":  st.secrets["gcp_service_account"] 
                                   }
                                    }
    )

    sheet_url = st.secrets["private_gsheets_url"]
    query = f'SELECT * FROM "{sheet_url}"'
    insert = f"""
            INSERT INTO "{sheet_url}" (id, twitter_username, party, dem_words, rep_words)
            VALUES ("{st.session_state.id}", "{st.session_state.name}", "{st.session_state.party}", "{st.session_state.dem_words}", "{st.session_state.rep_words}")
            """

    conn.execute(insert)

    for row in conn.execute(query):
        st.write(f"{row}")
