class SessionStore:
    def __init__(self):
        self.store = {}

    def get(self, session_id):
        return self.store.get(session_id, [])

    def set(self, session_id, value):
        self.store[session_id] = value

    def append(self, session_id, messages):
        history = self.get(session_id)
        history.extend(messages)
        self.store[session_id] = history


# SINGLE INSTANCE
session_store = SessionStore()