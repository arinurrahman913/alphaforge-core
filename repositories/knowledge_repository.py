from chronicles.chronicle import Chronicle


class KnowledgeRepository:

    def __init__(self):

        self._storage = {}

        self._chronicles = {}


    def save(self, knowledge):

        self._storage[knowledge.ticker] = knowledge

        if knowledge.ticker not in self._chronicles:

            self._chronicles[knowledge.ticker] = Chronicle()

        self._chronicles[knowledge.ticker].record(knowledge)


    def get(self, ticker):

        return self._storage.get(ticker)


    def history(self, ticker):

        chronicle = self._chronicles.get(ticker)

        if chronicle:

            return chronicle.history()

        return []


    def all(self):

        return list(self._storage.values())


    def delete(self, ticker):

        self._storage.pop(ticker, None)

        self._chronicles.pop(ticker, None)