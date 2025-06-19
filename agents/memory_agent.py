import datetime


class MemoryAgent:
    def __init__(self):
        self.history = []

    def add_to_memory(self, question, answer):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.history.append((timestamp, question, answer))

    def get_memory(self):
        return self.history
