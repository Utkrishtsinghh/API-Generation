FastAPI Product Listing API with Monitoring

This is a FastAPI-based backend application that serves paginated product listings by combining data from a database and a local JSON file. The project also includes self-hosted observability using Loki, Promtail, and Grafana for logging and monitoring.

---
Features

FastAPI-based REST API
Pagination with `pageNumber` and `pageSize`
Merges data from SQLite DB and JSON file
Dockerized setup with `docker-compose`
Logs captured with Promtail and visualized in Grafana
Loki used as the log storage backend
