import streamlit as st
from shillelagh.backends.apsw.db import connect
from datetime import datetime
from uuid import uuid4

st.title(" America divided? ") 
st.header("See how you and other twitter users see each party visualized in wordclouds ")
st.text_input("Enter your twitter username", key="name")

dem_words = []
st.subheader("Please add five words that describe Democrats best")
for i in range(5):
    dem_words.append(st.text_input("D"+str(i+1)))
st.session_state.dem_words = ", ".join(dem_words).lower()
st.markdown(f"Your words are {st.session_state.dem_words}.")

rep_words = []
st.subheader("Please add five words that describe Republicans best")
for i in range(5):
    rep_words.append(st.text_input("R"+str(i+1),key = "R"+str(i+1)))
st.session_state.rep_words = ", ".join(rep_words).lower()
st.markdown(f"Your words are {st.session_state.rep_words}.")

st.subheader("Feeling Thermomether")
st.slider("How warm do you feel about Democrats (0 = coldest rating; 100 = warmest rating)?", 
    min_value=0, max_value=100, value=50, step=1,key="dem_temp")          
st.slider("How warm do you feel about Republicans (0 = coldest rating; 100 = warmest rating)?", 
    min_value=0, max_value=100, value=50, step=1,key="rep_temp") 
st.session_state.party = st.radio(
     "How do you identify?",
     ('Independant','Republican', 'Democrat')) 

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
            INSERT INTO "{sheet_url}" (id, twitter_username, party, dem_words, rep_words, dem_temp, rep_temp)
            VALUES ("{st.session_state.id}", "{st.session_state.name}", "{st.session_state.party}", "{st.session_state.dem_words}", "{st.session_state.rep_words}", "{st.session_state.dem_temp}","{st.session_state.rep_temp}")
            """

    conn.execute(insert)

    all_dem_words = []
    all_rep_words = []
    for row in conn.execute(query):
        all_dem_words.append(row[3])
        all_rep_words.append(row[4])

    all_dem_words = ", ".join(all_dem_words)
    all_dem_words = all_dem_words.split(", ")
    all_rep_words = ", ".join(all_rep_words)
    all_rep_words = all_rep_words.split(", ")


    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    from matplotlib_venn_wordcloud import venn2_wordcloud

    fig, ax = plt.subplots(figsize=(15,12))

    ax.set_title('Words People Think Describe Republicans and Democrats', fontsize=20)
    v = venn2_wordcloud([set(all_rep_words), set(all_dem_words)],
                    set_colors=['red', 'blue'],
                    set_edgecolors=['w', 'w'],
                    alpha = .2,
                    ax=ax, set_labels=['Republican', 'Democrat'])
                    #word_to_frequency=all_pos_freq
    # add color
    #v.get_patch_by_id('10').set_color('red')
    #v.get_patch_by_id('10').set_alpha(0.4)
    #v.get_patch_by_id('01').set_color('blue')
    #v.get_patch_by_id('01').set_alpha(0.4)
    v.get_patch_by_id('11').set_color('purple')
    v.get_patch_by_id('11').set_alpha(0.2)
    st.pyplot(fig)


