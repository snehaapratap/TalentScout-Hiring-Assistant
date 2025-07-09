def info_prompt():
    return """
👋 Hello, and welcome to TalentScout! I'm Ava, your hiring assistant.

I'm here to help you find the best opportunities that match your skills and interests. To get started, could you please share the following details with me?

- **Full Name**
- **Email**
- **Phone Number** (optional)
- **Years of Experience**
- **Desired Position(s)**
- **Current Location**
- **Tech Stack** (languages, frameworks, databases, tools)

Once I have this information, I'll ask you a few technical questions tailored to your background. Feel free to answer in as much detail as you'd like!
"""

def generate_question_prompt(tech_stack):
    return f"""
You are an AI hiring assistant for a technical recruiter.

Given the candidate's tech stack: {tech_stack}

Generate 5 **unique** and **non-repetitive** technical questions to assess their expertise. Ensure the questions are:
- Based on the technologies mentioned
- Contextual to candidate experience
- Intermediate to advanced in difficulty

Only output the questions, numbered 1 to 5. Do NOT include any introduction, summary, or extra text. Only the questions, each on a new line.
"""




def followup_prompt(original_question, candidate_answer):
    return f"""
You asked the candidate the following technical question:

{original_question}

The candidate answered:

{candidate_answer}

Generate 1-2 insightful follow-up questions based on their answer to assess their deeper understanding. Ask only the next most relevant question(s).
"""

def clean_response(response):
    if "Overall Assessment" in response:
        return response.split("Overall Assessment")[0].strip()
    return response
