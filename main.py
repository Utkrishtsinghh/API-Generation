import logging
import os
import psutil
from fastapi import FastAPI, Query, Response, APIRouter
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Gauge
from prometheus_fastapi_instrumentator import Instrumentator
from flagsmith import Flagsmith
from database import fetch_products_from_db
from json_loader import load_products_from_json
from models import ProductResponse

logging.basicConfig(
    filename='logs/app.log',
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logging.info("FastAPI app starting...")

app = FastAPI()

Instrumentator().instrument(app).expose(app)

flagsmith = Flagsmith(environment_key="AdBMiGnv2RStykRrypzfZV")

metrics_router = APIRouter()

cpu_usage = Gauge("app_cpu_usage_percent", "CPU usage percent")
memory_usage = Gauge("app_memory_usage_mb", "Memory usage in MB")
running_instances = Gauge("app_running_instances", "Number of running app instances")

@metrics_router.get("/custom-metrics") 
def custom_metrics():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().used / 1024 / 1024  
    instance_count = int(os.environ.get("INSTANCE_ID", 1))  

    cpu_usage.set(cpu)
    memory_usage.set(mem)
    running_instances.set(instance_count)

    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

app.include_router(metrics_router)

@app.get("/api/products", response_model=ProductResponse)
def get_products(pageNumber: int = Query(1, ge=1), pageSize: int = Query(None)):
    logging.info(f"Received request: pageNumber={pageNumber}")
    
    flag_enabled = False

    if pageSize is None:
        try:
            flag_enabled = flagsmith.get_environment_flags().is_feature_enabled("show_50_products")

            pageSize = 50 if flag_enabled else 5
        except Exception as e:
            logging.warning(f"Flagsmith error: {e}")
            pageSize = 5

    logging.info(f"Using pageSize={pageSize} (Flag enabled: {flag_enabled})")

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

    logging.info(f"Returning {len(paginated)} products out of {total_products}")

    return {
        "totalCount": total_products,
        "pageNumber": pageNumber,
        "pageSize": pageSize,
        "products": paginated
    }

if __name__ == "__main__":
    logging.info("Uvicorn server starting...")
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
