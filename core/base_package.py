from enums.package_type import PackageType


class BasePackage:

    def __init__(
        self,
        package_type: PackageType,
        source: str,
        data,
    ):
        self.package_type = package_type
        self.source = source
        self.data = data

    def to_dict(self):
        return {
            "package_type": self.package_type.value,
            "source": self.source,
            "data": self.data,
        }

    def __repr__(self):
        return (
            f"BasePackage("
            f"type={self.package_type.value}, "
            f"source={self.source})"
        )