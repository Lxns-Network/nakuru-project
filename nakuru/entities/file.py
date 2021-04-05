from pydantic import BaseModel

class File(BaseModel):
    id: str
    name: str
    size: int
    busid: int

class OfflineFile(BaseModel):
    name: str
    size: int
    url: str

class ImageFile(BaseModel):
    size: int
    filename: str
    url: str