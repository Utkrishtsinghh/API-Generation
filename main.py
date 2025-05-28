from fastapi import FastAPI, Query
from database import fetch_products_from_db
from json_loader import load_products_from_json
from models import ProductResponse

app = FastAPI()

@app.get("/api/products", response_model=ProductResponse)
def get_products(pageNumber: int = Query(1, ge=1), pageSize: int = Query(10, ge=1)):
    db_products = fetch_products_from_db()
    db_total = len(db_products)
    
    json_products = []
    json_total = 0
    
    total_products = db_total
    
    start = (pageNumber - 1) * pageSize
    end = start + pageSize
    if end > db_total:
        json_products = load_products_from_json()
        json_total = len(json_products)
        total_products += json_total

    paginated = []
    
    if end <= db_total:
        paginated = db_products[start:end]
    else:
        if start < db_total:
            paginated.extend(db_products[start:db_total])
        
        json_start = max(0, start - db_total)
        json_end = json_start + (end - max(start, db_total))
        paginated.extend(json_products[json_start:json_end])
        
    return {
        "totalCount": total_products,
        "pageNumber": pageNumber,
        "pageSize": pageSize,
        "products": paginated
    }
