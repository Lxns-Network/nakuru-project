from pydantic import BaseModel


class Device(BaseModel):
    app_id: int
    device_name: str
    device_kind: str
