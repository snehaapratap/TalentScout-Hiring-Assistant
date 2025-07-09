import streamlit as st
from dotenv import load_dotenv
from backend.llm_handler import chat_with_groq, remove_duplicate_questions
import os
from utils.prompt import info_prompt, generate_question_prompt
from utils.context_handler import ConversationManager

load_dotenv()
st.set_page_config(page_title="TalentScout Hiring Assistant")

st.title("🤖 TalentScout - Hiring Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.manager = ConversationManager()
    st.session_state.asking_info = True
    st.session_state.tech_stack = ""

def get_gpt_response(prompt):
    st.session_state.manager.add_message("user", prompt)
    response = chat_with_groq(st.session_state.manager.get_context())
    st.session_state.manager.add_message("assistant", response)
    cleaned = remove_duplicate_questions(response)
    st.chat_message("assistant").write(cleaned)

    return response

if st.session_state.asking_info:
    intro = info_prompt()
    reply = get_gpt_response(intro)
    st.write(reply)
    st.session_state.asking_info = False

user_input = st.chat_input("Say something...")
if user_input:
    st.session_state.manager.add_message("user", user_input)


    if any(kw in user_input.lower() for kw in ["exit", "quit", "bye", "end"]):
        st.write("Thank you for applying! We'll reach out soon.")
        st.stop()


    if "tech stack" in user_input.lower() or any(x in user_input for x in [",", "Python", "React"]):
        st.session_state.tech_stack = user_input

    response = get_gpt_response(user_input)
    st.write(response)

    if st.session_state.tech_stack:
        q_prompt = generate_question_prompt(st.session_state.tech_stack)
        tech_questions = get_gpt_response(q_prompt)
        st.subheader("📘 Technical Questions:")
        st.markdown(tech_questions)
        st.session_state.tech_stack = ""  

    if "awaiting_answer" not in st.session_state:
        st.session_state.awaiting_answer = False
        st.session_state.last_question = ""

if user_input:
    if any(kw in user_input.lower() for kw in ["exit", "quit", "bye"]):
        farewell = "Thanks for your time! We'll contact you for next steps. 👋"
        st.session_state.manager.add_message("assistant", farewell)
        st.chat_message("assistant").write(farewell)
        st.stop()

    if st.session_state.awaiting_answer:
        from utils.prompt import followup_prompt
        prompt = followup_prompt(st.session_state.last_question, user_input)
        followup = get_gpt_response(prompt)
        st.chat_message("assistant").write(followup)
        st.session_state.manager.add_message("assistant", followup)
        st.session_state.awaiting_answer = False
    else:
        st.session_state.manager.add_message("user", user_input)
        response = get_gpt_response(user_input)
        st.session_state.manager.add_message("assistant", response)
        st.chat_message("assistant").write(response)

        if "1." in response and "2." in response:
            st.session_state.awaiting_answer = True
            st.session_state.last_question = response.split("1.")[1].split("\n")[0].strip()

