import os

SECRET_KEY_INTERNAL = os.getenv("SECRET_KEY_INTERNAL")


def content():
    data_headers = {
        "x-internal-secret": SECRET_KEY_INTERNAL,
        "Content-Type": "application/json"
    }
    
    return data_headers