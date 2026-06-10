import os

from minio import Minio

client = Minio("minio:9000",
               access_key=os.getenv("MINIO_ROOT_USER"),
               secret_key=os.getenv("MINIO_ROOT_PASSWORD"),
               secure=False,
               )

BUCKET_NAME = "documents"