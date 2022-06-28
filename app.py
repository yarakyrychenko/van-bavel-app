import streamlit as st
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

# Create a connection object.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)
conn = connect(credentials=credentials)

cursor = conn.cursor()

st.title(" Life vs Twitter Identity ") 
st.subheader("See how your 'real' identity compares to your Twitter identity.")
st.text_input("Enter a twitter username to begin", key="name")

sheet_url = st.secrets["private_gsheets_url"]


SQL = """
    SELECT *
    FROM "{sheet_url}"
    """
for row in cursor.execute(SQL):
    print(row)


