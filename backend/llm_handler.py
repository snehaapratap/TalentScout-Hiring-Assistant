import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "llama3-70b-8192")

client = Groq(api_key=groq_api_key)

def chat_with_groq(messages):
    try:
        response = client.chat.completions.create(
            model=groq_model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        reply = response.choices[0].message.content
        if not reply or "I'm not sure" in reply or "as an AI" in reply:
            return "I'm sorry, could you clarify that? I'd love to help you better."
        return reply
    except Exception as e:
        return "Something went wrong. Please try again or rephrase your input."

import re

def remove_duplicate_questions(text):
    questions = re.split(r'\n*\d\.\s+', text.strip())
    questions = [q.strip() for q in questions if q.strip()]
    unique_questions = list(dict.fromkeys(questions))  
    if not unique_questions:
        return text  
    return "\n\n".join([f"{i+1}. {q}" for i, q in enumerate(unique_questions)])
