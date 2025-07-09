class ConversationManager:
    def __init__(self):
        self.context = [
            {"role": "system", "content": "You are a professional hiring assistant helping TalentScout evaluate candidates. Gather information and ask relevant technical questions based on tech stack. Be friendly, professional, and helpful."}
        ]

    def add_message(self, role, content):
        self.context.append({"role": role, "content": content})

    def get_context(self):
        # Optionally, trim if context gets too large
        return self.context[-20:]
