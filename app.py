import streamlit as st
from shillelagh.backends.apsw.db import connect

# Create a connection object.
conn = connect(":memory:")

sheet_url = st.secrets["public_gsheets_url"]
query = f'SELECT * FROM "{sheet_url}"'
insert = f"""INSERT INTO "{sheet_url}" 
            VALUES (1, 'no', 'dem', 'rabbit')
"""
# Print results.
conn.execute(insert)

for row in conn.execute(query):
    st.write(f"{row}")
