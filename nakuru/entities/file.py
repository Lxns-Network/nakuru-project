from pydantic import BaseModel
import typing as T

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

class GroupFileSystem(BaseModel):
    file_count: int
    limit_count: int
    used_space: int
    total_space: int

class GroupFile(BaseModel):
    file_id: str
    file_name: str
    busid: int
    file_size: int
    upload_time: int
    dead_time: int
    modify_time: int
    download_times: int
    uploader: int
    uploader_name: str

class GroupFolder(BaseModel):
    folder_id: str
    folder_name: str
    create_time: int
    creator: int
    creator_name: str
    total_file_count: int

class GroupFileTree(BaseModel):
    files: T.List[GroupFile]
    folders: T.List[GroupFolder]