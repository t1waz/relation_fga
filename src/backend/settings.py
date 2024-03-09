import os

JWT_REFRESH_TTL = 30 * 60  # seconds
JWT_ACCESS_TTL = 1 * 60  # seconds

SECRET_KEY = os.getenv("BACKEND_SECRET_KEY")
MONGODB_HOST = os.getenv("BACKEND_MONGODB_HOST")
MONGODB_PORT = os.getenv("BACKEND_MONGODB_PORT")
MONGODB_DB_NAME = os.getenv("BACKEND_MONGODB_DB_NAME")
