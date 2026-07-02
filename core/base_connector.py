from abc import ABC, abstractmethod


class BaseConnector(ABC):

    @abstractmethod
    def fetch(self, *args, **kwargs):
        """
        Fetch data from external source.
        """
        pass