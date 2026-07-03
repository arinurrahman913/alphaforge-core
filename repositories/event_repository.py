from chronicles.chronicle import Chronicle


class EventRepository:

    def __init__(self):

        self._storage = {}

        self._chronicles = {}


    def save(self, event):

        if event.company not in self._storage:

            self._storage[event.company] = []

        self._storage[event.company].append(event)


        if event.company not in self._chronicles:

            self._chronicles[event.company] = Chronicle()

        self._chronicles[event.company].record(event)


    def get(self, company):

        return self._storage.get(company, [])


    def history(self, company):

        chronicle = self._chronicles.get(company)

        if chronicle:

            return chronicle.history()

        return []


    def delete(self, company):

        self._storage.pop(company, None)

        self._chronicles.pop(company, None)