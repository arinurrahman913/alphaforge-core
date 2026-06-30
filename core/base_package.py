class BasePackage:

    def __init__(self, package_type, source, data):
        self.package_type = package_type
        self.source = source
        self.data = data

    def to_dict(self):
        return {
            "package_type": self.package_type,
            "source": self.source,
            "data": self.data,
        }