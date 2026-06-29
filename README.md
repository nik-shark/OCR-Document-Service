# OCR Document Service

OCR Document Service is a REST API built with FastAPI for uploading images, extracting text using Tesseract OCR, and
storing the recognized text in a PostgreSQL database.

The project demonstrates asynchronous backend development with FastAPI, SQLAlchemy, Celery, Docker, MinIO, and
PostgreSQL.


## Features

Upload image files
Store images in MinIO (S3-compatible storage)
Extract text from images using Tesseract OCR
Run OCR tasks asynchronously with Celery
Store recognized text in PostgreSQL
Retrieve recognized text by document ID
Delete documents from both MinIO and the database
Interactive API documentation with Swagger UI


## Technology Stack

Python 3.12
FastAPI
SQLAlchemy 2.0
PostgreSQL
MinIO
Celery
Tesseract OCR
Docker & Docker Compose


## API Endpoints

Method Endpoint Description
POST /api/upload - Upload an image
POST /api/analyse - Start OCR processing
GET /api/text - Get recognized text
DELETE /api/delete - Delete a document


## Running the Project

Clone the repository:
git clone <repository_url> cd OCR-Document-Service

Build and start the containers:
docker compose up --build

The application will be available at:
http://localhost:8000

Swagger UI:
http://localhost:8000/docs


## CR Workflow

Upload an image.
The image is stored in MinIO.
A database record is created.
An OCR task is sent to Celery.
Tesseract extracts the text.
The recognized text is stored in PostgreSQL.
The text can be retrieved through the API.


## Project structure:
``` text 
├── app/
│   ├── api/
│   │   ├── analyse.py
│   │   ├── delete.py
│   │   ├── get_text.py
│   │   └── upload.py
│   │
│   ├── db/
│   │   ├── engine.py
│   │   └── models.py
│   │
│   ├── schemas/
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── analyse.py
│   │   ├── delete.py
│   │   ├── get_text.py
│   │   ├── s3_operations.py
│   │   ├── s3_settings.py
│   │   ├── tesseract.py
│   │   └── upload.py
│   │
│   ├── celery_app.py
│   │   
│   ├── main.py
│   │
│   └──task.py
│
├── docker/
│   └── Dockerfile
│
├── tests/
│
├── docker-compose.yaml
│
├── README.md
│
└── requirements.txt
```