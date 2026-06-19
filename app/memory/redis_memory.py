# class SessionStore:
#     def __init__(self):
#         self.store = {}

#     def get(self, session_id):
#         return self.store.get(session_id, [])

#     def set(self, session_id, value):
#         self.store[session_id] = value

#     def append(self, session_id, messages):
#         history = self.get(session_id)
#         history.extend(messages)
#         self.store[session_id] = history


# # SINGLE INSTANCE
# session_store = SessionStore()


import json
import redis

class RedisSessionStore:

    def __init__(self):
        self.redis_client = redis.Redis(
            host="localhost",
            port=6379,
            decode_responses=True
        )

    def get(self, session_id):

        data = self.redis_client.get(session_id)

        if not data:
            return []

        return json.loads(data)

    def append(self, session_id, messages):

        history = self.get(session_id)

        history.extend(messages)

        self.redis_client.set(
            session_id,
            json.dumps(history)
        )