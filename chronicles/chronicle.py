from datetime import datetime


class Chronicle:

    def __init__(self):

        self._history = []

    def record(self, data):

        self._history.append({

            "timestamp": datetime.now(),

            "data": data

        })

    def history(self):

        return self._history

    def latest(self):

        if not self._history:

            return None

        return self._history[-1]

    def count(self):

        return len(self._history)