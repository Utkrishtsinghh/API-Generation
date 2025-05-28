import json
from models import Product

JSON_PATH = "products.json"

def load_products_from_json() -> list[Product]:
    try:
        with open(JSON_PATH) as f:
            data = json.load(f)
            return [Product(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []
