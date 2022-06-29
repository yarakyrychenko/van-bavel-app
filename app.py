import streamlit as st
from google.oauth2 import service_account
from shillelagh.backends.apsw.db import connect

credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],
    scopes=[
        "https://www.googleapis.com/auth/spreadsheets",
    ],
)

# Create a connection object.
conn = connect(":memory:", adapter_kwargs={"gsheetaspi": { 
    "service_account_info":  st.secrets["gcp_service_account"] }
    )

sheet_url = st.secrets["public_gsheets_url"]
query = f'SELECT * FROM "{sheet_url}"'
insert = f"""INSERT INTO "{sheet_url}" 
            VALUES (1, 'no', 'dem', 'rabbit')
"""
# Print results.
conn.execute(insert)

for row in conn.execute(query):
    st.write(f"{row}")
