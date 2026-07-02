from core.base_package import BasePackage


class Pipeline:

    def __init__(self):
        self.engines = []

    def add_engine(self, engine):
        self.engines.append(engine)

    def run(self, package: BasePackage):

        current = package

        for engine in self.engines:
            current = engine.process(current)

        return current