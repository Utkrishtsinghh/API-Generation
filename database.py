import sqlite3
from models import Product

DB_PATH = "products.db"

def fetch_products_from_db() -> list[Product]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, category FROM products ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()
    return [Product(id=r[0], name=r[1], price=r[2], category=r[3]) for r in rows]
