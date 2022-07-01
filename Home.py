import streamlit as st
from shillelagh.backends.apsw.db import connect

st.set_page_config(
    page_title="App Home",
    page_icon=""
)

st.title("Language and Identity on Twitter") 
st.subheader("See multiple linguistic Twitter analysis.")
st.warning("""
           By submitting the form below you agree to your data being used for research. 
           Your twitter username will be stored in a private google sheet and will not be shared with anyone (unless extraordinary circumstances force us to share it). 
           You can ask for your data to be deleted by emailing us with an app ID number you'll be issued after submitting the form. 
           """)

st.text_input("Enter a twitter username to begin", key="name")

if "last_name" not in st.session_state:
        st.session_state.last_name = ""
        
if st.session_state.last_name != st.session_state.name:    

    st.session_state.username_mine = st.radio(
        "I confirm that:",
        ('This username belongs to me.', 'This username is belongs to someone else.')) 

    if st.session_state.username_mine == 'This username belongs to me.':

        with st.form("my_form"):
            dem_words = []
            st.markdown("#### Please add five words that describe Democrats best")
            for i in range(5):
                dem_words.append(st.text_input("D"+str(i+1)))
            st.session_state.dem_words = ", ".join(dem_words).lower()

            rep_words = []
            st.markdown("#### Please add five words that describe Republicans best")
            for i in range(5):
                rep_words.append(st.text_input("R"+str(i+1),key = "R"+str(i+1)))
            st.session_state.rep_words = ", ".join(rep_words).lower()

            st.markdown("#### Feeling Thermomether")
            st.slider("How warm do you feel about Democrats (0 = coldest rating; 100 = warmest rating)?", 
                min_value=0, max_value=100, value=50, step=1,key="dem_temp")          
            st.slider("How warm do you feel about Republicans (0 = coldest rating; 100 = warmest rating)?", 
                min_value=0, max_value=100, value=50, step=1,key="rep_temp") 
            st.session_state.party = st.radio(
                "How do you identify?",
                ('Independant','Republican', 'Democrat')) 
    
            st.session_state.submitted = st.form_submit_button("Submit")
    
        if st.session_state.submitted:
            if (st.session_state.rep_words[-2:] != ", "):
                from helper import connect_to_gsheets, insert_user_data
                from datetime import datetime
                from uuid import uuid4

                st.markdown("### Thanks for submitting your answers!")
                st.session_state.id = datetime.now().strftime('%Y%m-%d%H-%M-') + str(uuid4())
                st.markdown(f"Your app ID is {st.session_state.id}. Note it down and email us if you want your answers deleted.") 
                st.session_state.conn = connect(":memory:", 
                    adapter_kwargs = {
                    "gsheetsapi": { 
                        "service_account_info":  st.secrets["gcp_service_account"] 
                                    }
                                        }
                )

                insert_user_data(conn, st.secrets["private_gsheets_url"])

                st.markdown("Click on [Linguistic Analysis]() to find out what language you and others use on Twitter.")
                st.markdown("Click on [Partisanship]() to find out how you and others think and talk about the US political parties.")
            else:
                st.error("Please fill out every field and try again.")

    if st.session_state.username_mine == 'This username is belongs to someone else.' and st.session_state.name != "":
        st.session_state.conn = connect(":memory:", 
                adapter_kwargs = {
                    "gsheetsapi": { 
                        "service_account_info":  st.secrets["gcp_service_account"] 
                                    }
                                        }
                )
        st.warning("""You entered someone else's Twitter username. 
                Some analyses will not be available. 
                If you change your mind at any point, return to this page to enter your Twitter username.
                """)
        st.markdown(f"### Click 'Twitter Language Analysis' to find out what language {st.session_state.name} and others use on Twitter.")
        st.markdown(f"### Click 'Linguistic Partisanship' to find out how {st.session_state.name} and others think and talk about the US political parties.")





