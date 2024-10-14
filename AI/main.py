import os
import tempfile
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
from whisper_mic.whisper_mic import WhisperMic 
from gtts import gTTS  # Text-to-speech library

# Load environment variables
load_dotenv()


# Configure Streamlit page settings
st.set_page_config(
    page_title="ASSISTANT",
    page_icon=":mahjong:",  # Favicon emoji
    layout="centered",  # Page layout option
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Function to translate roles between Gemini-Pro and Streamlit terminology
def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

# Initialize chat session in Streamlit if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

# Display the chatbot's title on the page
st.title("AI ASSISTANT 👽")  # Adjust title as needed

# Display the chat history
for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)

# Text input field for user's message
user_prompt = st.chat_input("I'm here to assist you ask me some thing...")

# Send user's message to the chatbot and display the response
try:
    if user_prompt:
         st.chat_message("user").markdown(user_prompt)
         gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Text-to-speech for chatbot response (using temporary file)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
        tts = gTTS(text=gemini_response.text, lang='en')  # Change 'en' for other languages
        tts.save(temp_file.name)
        st.audio(temp_file.name)  # Streamlit will automatically refresh and play

    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)

except:
    st.write("Audio not Available")

# Initialize WhisperMic
mic = WhisperMic()

# Button to capture speech input and convert to text

try:
    if st.button("Voice Chat"):
        result = mic.listen()
    # Display the captured speech input in the user chat message
        if result:
            st.chat_message("user").markdown(result)
            gemini_response = st.session_state.chat_session.send_message(result)

        # Text-to-speech for chatbot response (repeat logic with temporary file)
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            tts = gTTS(text=gemini_response.text, lang='en')  # Change 'en' for other languages
            tts.save(temp_file.name)
            st.audio(temp_file.name)

        with st.chat_message("assistant"):
            st.markdown(gemini_response.text)
except:
    st.write("Not Available")
