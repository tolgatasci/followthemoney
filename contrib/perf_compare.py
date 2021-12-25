from followthemoney import model
from followthemoney.proxy import EntityProxy
from followthemoney import compare

ENTITY = {
    "id": "test",
    "schema": "Person",
    "properties": {
        "name": "Ralph Tester",
        "birthDate": "1972-05-01",
        "idNumber": ["9177171", "8e839023"],
        "website": "https://ralphtester.me",
        "phone": "+12025557612",
        "email": "info@ralphtester.me",
        "topics": "role.spy",
    },
}


def create_proxy():
    proxy = EntityProxy.from_dict(model, ENTITY)
    data = proxy.to_dict()
    return data


def benchmark():
    proxy = create_proxy()
    for i in range(10_000):
        compare.compare(model, proxy, proxy)


if __name__ == "__main__":
    benchmark()
