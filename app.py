import streamlit as st
from shillelagh.backends.apsw.db import connect

st.title(" Are you partisan? ") 
st.subheader("See how you and other twitter users see each party visualized in wordclouds ")
st.text_input("Enter a twitter username to begin", key="name")
st.session_state.party = st.radio(
     "Which party do you identify with?",
     ('Republican', 'Democratic'))

dem_words = []
st.text("Please add ten words that describe Democrats best in your opinion below:")
for i in range(5):
    dem_words.append(st.text_input("D"+str(i+1)))
st.session_state.dem_words = ",".join(dem_words)

rep_words = []
st.text("Please add ten words that describe Democrats best in your opinion below:")
for i in range(5):
    rep_words.append(st.text_input("R"+str(i+1)))
st.session_state.rep_words = ",".join(rep_words)
       
# Create a connection object.
conn = connect(":memory:", 
               adapter_kwargs = {
                   "gsheetsapi": { 
                       "service_account_info":  st.secrets["gcp_service_account"] 
                                   }
                                    }
    )

sheet_url = st.secrets["private_gsheets_url"]
query = f'SELECT * FROM "{sheet_url}"'
insert = f"""INSERT INTO "{sheet_url}" 
            VALUES (1, {st.session_state.name}, {st.session_state.party}, {st.session_state.dem_words})
"""
# Print results.
conn.execute(insert)

for row in conn.execute(query):
    st.write(f"{row}")
