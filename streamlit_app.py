import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

st.set_page_config(layout="wide", page_title="رفيق التحرر", page_icon="😇")

# Align the title to the right
st.markdown(
    """
    <div style='text-align: right;'>
        <h1>رفيق التحرر</h1>
    </div>
    """,
    unsafe_allow_html=True
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_resource
def get_response(query, _chat_history):

    llm = ChatGoogleGenerativeAI(
        api_key=os.environ['GOOGLE_API_KEY'], model="gemini-2.0-flash-exp", temperature=0.3)

    followup_prompt = ChatPromptTemplate.from_template(
        """
                You are a  psychologist and you are talking to patients who are suffering from phone and social media addiction.
                You are trying to help them to overcome their addiction.
                Try not to mention that you are a  psychologist. Try to not to mention that you are speaking to a patient.
                There are people who are talking to you and they aren't addicted to it but they just are curious about the topic.
                You are trying to tell them about how social media creators are using psychology to keep people addicted to their platforms.
                Your goal is to subtly educate users about the tactics social media creators use—like infinite scrolling, dopamine triggers from likes, and targeted notifications—without explicitly accusing them of being addicted.
                Instead, you want them to realize it on their own by highlighting these techniques in a simple, engaging, and non-judgmental way. 
                Always keep the tone light and relatable, allowing users to connect the dots themselves about their habits.
                You can talk Arabic or English. You can also talk in Egyptian Arabic. Respond in just one language and don't translate to any other language.
                You can have information from Social Dilemma documentary. Your name is "رفيق التحرر".

                Current conversation:
                {_chat_history}

                User: {question}
                Social media bot: 
        """
    )

# Create the followup chain
    followup_chain = followup_prompt | llm | StrOutputParser()
    answer = followup_chain.stream(
        {"question": query, "_chat_history": _chat_history})
    return answer


for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("Bot"):
            st.markdown(message.content)

user_query = st.chat_input("I'm here to help you.")

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("User"):
        st.markdown(user_query)
    with st.chat_message("Bot"):
        with st.spinner("Thinking..."):
            ai_response = get_response(
                user_query, st.session_state.chat_history)
        stream = st.write_stream(ai_response)
    st.session_state.chat_history.append(AIMessage(stream))
