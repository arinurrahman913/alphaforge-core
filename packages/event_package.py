from dataclasses import dataclass

from models.event import Event


@dataclass
class EventPackage:

    event: Event

    def __str__(self):

        return str(self.event)