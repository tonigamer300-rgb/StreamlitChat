import streamlit as st
from datetime import datetime

# 1. SETUP GLOBAL STORAGE (Shared across all users)
@st.cache_resource
def get_chat_history():
    # This list lives on the server memory as long as the app is running
    return []

chat_history = get_chat_history()

st.title("🌐 Local WiFi Chat Room")

if "username" not in st.session_state:
    with st.form("login_form"):
        name = st.text_input("Choose a username")
        submit = st.form_submit_button("Join Chat")
        if submit and name:
            st.session_state.username = name
            st.rerun()
    
    # We force the script to stop here if the username isn't set
    st.stop() 

else:
    # This block ONLY runs if the 'if' above is False
    st.sidebar.write(f"Logged in as: **{st.session_state.username}**")
    if st.sidebar.button("Refresh Chat"):
        st.rerun()
    
    if st.sidebar.button("Logout"):
        del st.session_state.username
        st.rerun()

# 4. CHAT DISPLAY
st.subheader("Messages")
# We create a container so the chat stays in one scrollable area
chat_container = st.container(height=400)

with chat_container:
    for msg in chat_history:
        # Style based on whether it's 'me' or 'them'
        is_me = msg['user'] == st.session_state.username
        align = "right" if is_me else "left"
        
        st.markdown(
            f"""<div style='text-align: {align}; color: grey; font-size: 0.8em;'>
                {msg['user']} • {msg['time']}
            </div>
            <div style='background-color: {"#2e7bcf" if is_me else "#444"}; 
                        padding: 10px; border-radius: 10px; margin-bottom: 10px;
                        text-align: {align}; color: white;'>
                {msg['text']}
            </div>""", 
            unsafe_allow_html=True
        )

# 5. SEND MESSAGE
if prompt := st.chat_input("Type a message..."):
    new_msg = {
        "user": st.session_state.username,
        "text": prompt,
        "time": datetime.now().strftime("%H:%M")
    }
    chat_history.append(new_msg)
    st.rerun() # Refresh to show the new message immediately