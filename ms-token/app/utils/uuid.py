import uuid
from fastapi.responses import JSONResponse

UUID_REGEX = "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$"

def uuid_generate() -> str:
    return str(uuid.uuid4())


def uuid_validate(uuid: str) -> str:
    if uuid != UUID_REGEX: 
        return JSONResponse({"Mensaje": "El formato no es un uuid"})