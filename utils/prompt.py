def info_prompt():
    return """
You are a hiring assistant bot for TalentScout. Greet the candidate, ask for:
- Full Name
- Email
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (languages, frameworks, databases, tools)
"""

def generate_question_prompt(tech_stack):
    return f"""
You are an AI hiring assistant for a technical recruiter.

Given the candidate's tech stack: {tech_stack}

Generate 5 **unique** and **non-repetitive** technical questions to assess their expertise. Ensure the questions are:
- Based on the technologies mentioned
- Contextual to candidate experience
- Intermediate to advanced in difficulty

Only output the questions once, numbered 1 to 5. Do NOT repeat the same questions.
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
