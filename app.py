import streamlit as st
from shillelagh.backends.apsw.db import connect

# Create a connection object.
conn = connect(":memory:")

sheet_url = st.secrets["public_gsheets_url"]
query = f'SELECT * FROM "{sheet_url}"'

# Print results.
for row in conn.execute(query):
    st.write(f"{row}")
