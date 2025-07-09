"""
Assignment: TalentScout Hiring Assistant Chatbot
------------------------------------------------
You are tasked with developing an intelligent Hiring Assistant chatbot for "TalentScout," a fictional recruitment agency specializing in technology placements. The chatbot should assist in the initial screening of candidates by gathering essential information and posing relevant technical questions based on the candidate's declared tech stack. This project will allow you to demonstrate your understanding of LLMs.
"""
import streamlit as st
from dotenv import load_dotenv
from backend.llm_handler import chat_with_groq, remove_duplicate_questions
import os
from utils.prompt import info_prompt, generate_question_prompt
from utils.context_handler import ConversationManager
import time
import re

load_dotenv()
st.set_page_config(page_title="TalentScout Hiring Assistant", page_icon="🤖", layout="centered")

# Sidebar for branding and info
with st.sidebar:
    st.title("🤖 TalentScout")
    st.markdown("""
    **Hiring Assistant**
    
    _Smart screening for tech candidates._
    
    ---
    **About Ava:**
    Ava is an intelligent hiring assistant designed to help recruiters screen candidates efficiently. She gathers essential information, asks tailored technical questions, and provides a friendly, professional experience for every applicant.
    """)
    st.markdown("---")
    st.markdown("Developed by Sneha Prem")

# Define the order and prompts for info gathering
INFO_FIELDS = [
    ("full_name", "What is your full name?"),
    ("email", "What is your email address?"),
    ("phone", "What is your phone number? (optional)"),
    ("experience", "How many years of experience do you have?"),
    ("position", "What position(s) are you interested in?"),
    ("location", "Where are you currently located?"),
    ("tech_stack", "Please specify your tech stack (languages, frameworks, databases, tools):")
]

if "info_state" not in st.session_state:
    st.session_state.info_state = {field: None for field, _ in INFO_FIELDS}
    st.session_state.info_step = 0
    st.session_state.info_complete = False
    st.session_state.tech_questions = []
    st.session_state.current_question = 0
    st.session_state.followup_count = 0
    st.session_state.asked_final_thankyou = False
    st.session_state.awaiting_answer = False
    st.session_state.last_question = ""
    st.session_state.asked_tech_questions = False
    st.session_state.messages = []
    st.session_state.manager = ConversationManager()
    st.session_state.asking_info = True
    st.session_state.tech_stack = ""

# Helper to add message to history and context
def add_message(role, content):
    st.session_state.messages.append({"role": role, "content": content})
    st.session_state.manager.add_message(role, content)

# Helper to get LLM response and add to history
def get_gpt_response(prompt):
    thinking_idx = len(st.session_state.messages)
    add_message("assistant", "_Ava is thinking..._")
    response = chat_with_groq(st.session_state.manager.get_context())
    cleaned = remove_duplicate_questions(response)
    st.session_state.messages[thinking_idx]["content"] = cleaned
    if cleaned.startswith("I'm sorry") or cleaned.startswith("Something went wrong"):
        debug_msg = f"""**[DEBUG] Prompt sent to LLM:**
```
{prompt}
```
**[DEBUG] LLM Response:**
```
{cleaned}
```
"""
        add_message("assistant", debug_msg)
    return cleaned

# Show info prompt only once at the start
if st.session_state.asking_info:
    intro = info_prompt()
    add_message("assistant", intro)
    st.session_state.asking_info = False

# Display full chat history
st.markdown("<div style='height: 500px; overflow-y: auto;'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
st.markdown("</div>", unsafe_allow_html=True)

# Step-by-step info gathering
if not st.session_state.info_complete:
    # Ask the next info question
    current_field, current_prompt = INFO_FIELDS[st.session_state.info_step]
    if st.session_state.info_state[current_field] is None:
        with st.chat_message("assistant"):
            st.markdown(current_prompt)
    user_input = st.chat_input("Say something...")
    if user_input:
        add_message("user", user_input)
        st.session_state.info_state[current_field] = user_input
        st.session_state.info_step += 1
        if st.session_state.info_step >= len(INFO_FIELDS):
            st.session_state.info_complete = True
            st.session_state.tech_stack = st.session_state.info_state["tech_stack"]
            st.rerun()
        else:
            st.rerun()

# After info gathering, proceed to technical questions
if st.session_state.info_complete:
    # If technical questions not yet generated, do so
    if not st.session_state.tech_questions:
        q_prompt = generate_question_prompt(st.session_state.tech_stack) + "\nPlease ensure you generate exactly 5 unique, non-repetitive, intermediate to advanced technical questions, numbered 1 to 5, based on the candidate's tech stack. Only output the questions, no introduction or summary."
        tech_questions_text = get_gpt_response(q_prompt)
        # Parse questions into a list, skipping any intro/summary lines
        questions = []
        for line in tech_questions_text.split('\n'):
            match = re.match(r"^\s*(\d+)\.\s+(.*)", line)
            if match:
                questions.append(match.group(2).strip())
        st.session_state.tech_questions = questions[:5]  # Only take up to 5
        st.session_state.current_question = 0
        st.session_state.followup_count = 0
        st.session_state.asked_final_thankyou = False
        st.session_state.awaiting_answer = True
        st.session_state.last_question = st.session_state.tech_questions[0] if st.session_state.tech_questions else ""
        st.rerun()
    # Ask technical questions and handle follow-ups
    else:
        # If all questions and follow-ups are done
        if st.session_state.current_question >= len(st.session_state.tech_questions):
            if not st.session_state.asked_final_thankyou:
                thankyou_msg = "Thank you for responding! We'll reach out to you soon. If you have any further questions, feel free to ask."
                add_message("assistant", thankyou_msg)
                st.session_state.asked_final_thankyou = True
            # Allow user to continue asking questions (e.g., about updates)
            user_input = st.chat_input("Say something...")
            if user_input:
                add_message("user", user_input)
                # Fallback/FAQ logic (to be improved in next step)
                if any(kw in user_input.lower() for kw in ["update", "further update", "next step", "when can i get", "when will i get"]):
                    update_msg = "Thank you for your interest! Our team will review your responses and get back to you within a few days. If you have any more questions, feel free to ask."
                    add_message("assistant", update_msg)
                else:
                    fallback_msg = "Thank you for your message! If you have any questions about the process or next steps, let me know."
                    add_message("assistant", fallback_msg)
        else:
            # Ask the current technical question or follow-up
            if st.session_state.followup_count == 0:
                with st.chat_message("assistant"):
                    st.markdown(f"**Technical Question {st.session_state.current_question+1}:** {st.session_state.tech_questions[st.session_state.current_question]}")
            user_input = st.chat_input("Your answer...")
            if user_input:
                add_message("user", user_input)
                # Ask up to 2 follow-ups per technical question
                if st.session_state.followup_count < 2:
                    from utils.prompt import followup_prompt
                    prompt = followup_prompt(st.session_state.tech_questions[st.session_state.current_question], user_input)
                    followup = get_gpt_response(prompt)
                    st.session_state.followup_count += 1
                else:
                    # Move to next technical question
                    st.session_state.current_question += 1
                    st.session_state.followup_count = 0
                st.rerun()

