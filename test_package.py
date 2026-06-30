from core.base_package import BasePackage

package = BasePackage(
    package_type="Knowledge",
    source="YahooFinanceConnector",
    data={
        "ticker": "NVDA",
        "price": 194.97
    }
)

print(package)
print(package.to_dict())