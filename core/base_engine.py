from abc import ABC, abstractmethod

from core.base_package import BasePackage


class BaseEngine(ABC):

    @abstractmethod
    def process(self, package: BasePackage) -> BasePackage:
        """
        Process a package and return a new package.
        """
        pass