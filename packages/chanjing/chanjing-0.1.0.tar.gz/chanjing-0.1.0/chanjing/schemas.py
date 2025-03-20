from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar

T = TypeVar('T')

class Figure(BaseModel):
    """人物形象数据模型"""
    pic_path: str
    type: str
    cover: str
    width: int
    height: int
    preview_video_url: str

class CommonPerson(BaseModel):
    """公共数字人信息数据模型"""
    id: str
    name: str
    figures: List[Figure]
    gender: str
    width: int
    height: int
    audio_name: str
    audio_man_id: str
    audio_preview: str

class Person(BaseModel):
    """人物信息数据模型"""
    id: str
    name: str
    type: str
    pic_url: str
    preview_url: str
    width: int
    height: int
    audio_man_id: str
    status: int
    err_reason: str
    is_open: int
    reason: str
    progress: int

class PageInfo(BaseModel):
    """分页信息数据模型"""
    page: int
    size: int
    total_count: int
    total_page: int

class ResponseData(BaseModel, Generic[T]):
    """响应数据模型"""
    list: List[T]
    page_info: Optional[PageInfo]

class APIResponse(BaseModel, Generic[T]):
    """API响应模型"""
    trace_id: str
    code: int
    msg: str
    data: Optional[T] = None


class Audio(BaseModel):
    """音频信息"""
    id: str
    name: str
    progress: int
    audio_path: str
    err_msg: str

class SynthesisVideo(BaseModel):
    """合成视频信息"""
    id: str
    status: int
    progress: int
    msg: str
    video_url: str
    create_time: int
    subtitle_data_url: str
    preview_url: str
    duration: int

class FontInfo(BaseModel):
    """字体信息"""
    id: str
    name: str
    preview: str
    ttf_path: str

class UserInfo(BaseModel):
    """用户信息"""
    name: str
    id: str
    custom_person_nums: int
    custom_person_limit: int
    video_create_seconds: int
    video_create_limit: int

