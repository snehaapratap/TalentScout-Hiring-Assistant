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
Given the tech stack: {tech_stack}, generate 3-5 technical questions to assess the candidate’s proficiency.
Questions should be intermediate-to-advanced level.
Only return questions, numbered, no explanation.
"""
