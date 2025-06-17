import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)

# Test API connection


def test_api_connection():
    """Test if the Google API key is working"""
    try:
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            return False, "No API key found"
          # Simple test call
        test_llm = ChatGoogleGenerativeAI(
            api_key=api_key,
            model="gemini-1.5-flash",
            temperature=0.3
        )

        # Test with a simple message
        test_response = test_llm.invoke(
            "Hello, can you respond with just 'OK'?")
        return True, "Connection successful"
    except Exception as e:
        return False, str(e)


# Check API connection on startup
if 'api_tested' not in st.session_state:
    st.session_state.api_tested = False
    is_connected, message = test_api_connection()
    st.session_state.api_connected = is_connected
    st.session_state.api_message = message
    st.session_state.api_tested = True

# Show connection status
if not st.session_state.api_connected:
    st.error(f"API Connection Issue: {st.session_state.api_message}")
    st.info("Please check your GOOGLE_API_KEY environment variable and try refreshing the page.")

st.set_page_config(layout="wide", page_title="رفيق التحرر", page_icon="😇")

# Add RTL support and custom CSS
st.markdown(
    """
    <style>
    /* RTL support for the entire app */
    .stApp {
        direction: rtl;
    }
    
    /* RTL support for chat messages */
    .stChatMessage {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL support for markdown content */
    .stMarkdown {
        direction: rtl;
        text-align: right;
    }
    
    /* RTL support for input */
    .stChatInput {
        direction: rtl;
    }
    
    /* RTL support for chat input field */
    .stChatInput > div > div > input {
        direction: rtl;
        text-align: right;
    }
    
    /* Custom styling for user messages */
    .stChatMessage[data-testid="user-message"] {
        background-color: #f0f2f6;
        direction: rtl;
        text-align: right;
    }
    
    /* Custom styling for bot messages */
    .stChatMessage[data-testid="assistant-message"] {
        background-color: #ffffff;
        direction: rtl;
        text-align: right;
    }
    
    /* Title alignment */
    .main-header {
        text-align: right;
        direction: rtl;
    }
    
    /* Ensure all text content is RTL */
    p, div, span {
        direction: rtl;
        text-align: right;
    }
    
    /* Fix for Streamlit's default LTR elements */
    .element-container {
        direction: rtl;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Align the title to the right
st.markdown(
    """
    <div class='main-header'>
        <h1>رفيق التحرر</h1>
    </div>
    """,
    unsafe_allow_html=True
)


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


@st.cache_resource
def get_response(query, _chat_history):
    try:
        # Check if API key exists
        api_key = os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            st.error(
                "Google API key not found. Please check your environment variables.")
            return None

        llm = ChatGoogleGenerativeAI(
            api_key=api_key,
            model="gemini-2.0-flash",  # Using a more stable model
            temperature=0.3
        )

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
                    You can be concise in your responses.
                    
                    
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

    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        logging.error(f"Error in get_response: {str(e)}")
        return None


# Display chat history
for i, message in enumerate(st.session_state.chat_history):
    if isinstance(message, HumanMessage):
        with st.chat_message("User"):
            st.markdown(
                f'<div style="direction: rtl; text-align: right;">{message.content}</div>', unsafe_allow_html=True)
    elif isinstance(message, AIMessage):
        with st.chat_message("Assistant"):
            st.markdown(
                f'<div style="direction: rtl; text-align: right;">{message.content}</div>', unsafe_allow_html=True)

user_query = st.chat_input("أنا هنا لمساعدتك...")

if user_query is not None and user_query != "":
    # Only proceed if API is connected
    if not st.session_state.api_connected:
        st.error(
            "لا يمكن معالجة الطلب: فشل الاتصال بواجهة برمجة التطبيقات. يرجى التحقق من مفتاح API وإعادة تحميل الصفحة.")
    else:
        # Add user message to history
        st.session_state.chat_history.append(HumanMessage(user_query))

        # Display user message
        with st.chat_message("User"):
            st.markdown(
                f'<div style="direction: rtl; text-align: right;">{user_query}</div>', unsafe_allow_html=True)

        # Generate and display assistant response
        with st.chat_message("Assistant"):
            with st.spinner("جاري التفكير..."):
                ai_response = get_response(
                    user_query, st.session_state.chat_history)

            if ai_response is not None:
                try:
                    # Use streaming response
                    response_text = st.write_stream(ai_response)
                    # Add the complete response to history
                    st.session_state.chat_history.append(
                        AIMessage(response_text))
                except Exception as e:
                    # Fallback to non-streaming response
                    logging.error(f"Streaming failed: {str(e)}")
                    st.warning("فشل في البث، جاري المحاولة بطريقة بديلة...")

                    try:
                        # Get non-streaming response - create new response to avoid caching issues
                        api_key = os.environ.get('GOOGLE_API_KEY')
                        llm = ChatGoogleGenerativeAI(
                            api_key=api_key,
                            model="gemini-1.5-flash",
                            temperature=0.3
                        )

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
                            You can be concise in your responses.
                            
                            Current conversation:
                            {_chat_history}

                            User: {question}
                            Social media bot: 
                            """
                        )

                        followup_chain = followup_prompt | llm | StrOutputParser()
                        response_text = followup_chain.invoke(
                            {"question": user_query, "_chat_history": st.session_state.chat_history})

                        st.markdown(
                            f'<div style="direction: rtl; text-align: right;">{response_text}</div>', unsafe_allow_html=True)
                        st.session_state.chat_history.append(
                            AIMessage(response_text))
                    except Exception as e2:
                        error_message = "عذراً، أواجه صعوبة في الرد الآن. قد يكون هذا بسبب حدود واجهة برمجة التطبيقات أو مشاكل في الشبكة. يرجى المحاولة مرة أخرى بعد قليل."
                        st.error(error_message)
                        st.session_state.chat_history.append(
                            AIMessage(error_message))
                        logging.error(
                            f"Both streaming and fallback failed: {str(e2)}")
            else:
                error_message = "عذراً، لم أتمكن من إنشاء رد. يرجى المحاولة مرة أخرى."
                st.error(error_message)
                st.session_state.chat_history.append(AIMessage(error_message))
