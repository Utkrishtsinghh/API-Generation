import sqlite3

DB_PATH = "products.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY,
    name TEXT,
    price REAL,
    category TEXT
)
""")

products_to_insert = [
    (1, "Laptop", 90, "Electronics"),
    (2, "Chair", 40, "Furniture"),
    (3, "Watch", 10, "Accessories")
]

cursor.executemany("INSERT INTO products (id, name, price, category) VALUES (?, ?, ?, ?)", products_to_insert)

conn.commit()
conn.close()

print("Products added to DB!")
