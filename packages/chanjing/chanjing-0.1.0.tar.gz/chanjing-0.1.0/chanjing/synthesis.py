from typing import Optional, Literal
from pydantic import BaseModel, confloat, conint, constr
import chanjing.schemas
from chanjing.core import ChanjingHttpClient

class PersonConfig(BaseModel):
    id: str  # 形象列表返回的id
    x: int  # x位置
    y: int  # y位置
    figure_type: Optional[str] = None  # 非必传，whole_body仅使用公共数字人时，需传该参数
    width: int = 1080  # 宽
    height: int = 1920  # 高
    drive_mode: Optional[str] = None  # 非必传，驱动模式。支持正常顺序驱动，和随机帧动作驱动random
    is_rgba_mode: bool = False  # 非必传，默认false，是否驱动四通道webm视频
    backway: int = 1  # 非必传，默认1，指定数字人驱动到素材末尾的播放顺序，1正放，2倒放


class TTSConfig(BaseModel):
    text: list  # 文本，字符串类所有内容放到符串上面。使点符号分割不用分多个字
    speed: confloat(ge=0.5, le=2)  # 浮点数类型，围请在0.5和2
    audio_man: str  # 数字人中列表audio_man_id数字人的音色

class BgConfig(BaseModel):
    src_url: str  # 图片地址
    x: int  # x 坐标
    y: int  # y 坐标
    width: conint(ge=1)  # 图片宽度，必须大于等于 1
    height: conint(ge=1)  # 图片高度，必须大于等于 1

class SubtitleConfig(BaseModel):
    x: int  # x 坐标，字体显示范围的起始 x 坐标
    y: int  # y 坐标，字体显示范围的起始 y 坐标
    show: bool  # 是否显示字幕
    width: conint(ge=1)  # 字体显示范围的宽度，必须大于等于 1
    height: conint(ge=1)  # 字体显示范围的高度，必须大于等于 1
    font_size: conint(ge=1)  # 字体大小，必须大于等于 1
    color: constr(pattern=r"^#[0-9A-Fa-f]{6}$") = "#000000"  # 颜色，默认黑色
    font_id: str = ""  # 字体 ID，可选

class AudioConfig(BaseModel):
    tts : TTSConfig
    wav_url: Optional[str] = None  # mp3、m4a 或者 wav 视频文件，根据音频文件驱动数字人
    type: Literal["tts", "audio"] = "tts"  # 生成声音类型，默认 "tts"
    volume: int = 100  # 音量，默认 100
    language: str = "cn"  # 语言类型，默认 "cn"






   
class CreateVideoRequest(BaseModel):
    """创建合成视频请求模型
    
    属性:
        name: 合成视频名称
        url: 外网可下载播放的视频链接
        callback: 回调地址，任务结束后会向该地址发送POST请求
      
    """
    person: PersonConfig
    bg: Optional[BgConfig] = None
    subtitle:Optional[SubtitleConfig] = None
    audio: AudioConfig
    bg_color: constr(pattern=r"^#[0-9A-Fa-f]{6}$") = "#000000"  # 颜色默认黑色
    screen_width: conint(ge=1) =1080 # 字体显示范围的宽度，必须大于等于 1
    screen_height: conint(ge=1) =1920 # 字体显示范围的高度，必须大于等于 1
    callback: Optional[str] = None  # 回调地址，任务结束后会向该地址发送POST请求

class ListVideoRequest(BaseModel):
    """合成视频列表请求模型
    
    属性:
        page: 当前页码
        page_size: 每页记录数
    """
    page : int
    page_size: int


class Video(object):
    def __init__(self,client:ChanjingHttpClient) -> None:
        """
        初始化合成视频管理类
        
        Args:
            client: 禅境HTTP客户端
        """
        self.client = client
        pass
    def create(self , request:CreateVideoRequest)->str:
        """
        创建合成视频
        
        Args:
            request: 创建合成视频请求
        """
        response = self.client.request("POST", "create_video", json=request.model_dump())
        return response.data

    def list(self , request:ListVideoRequest)->chanjing.schemas.ResponseData:
        """
        获取合成视频列表
        
        Args:
            request: 合成视频列表请求
        """
        response = self.client.request("POST", "video_list", json=request.model_dump())
        return response.data

    def detail(self , id:str)->chanjing.schemas.SynthesisVideo:
        """
        合成视频详情
        
        Args:
            id: 合成视频ID
        """
        response = self.client.request("GET", "video", params={"id": id})
        return response.data

    def font_list(self )->chanjing.schemas.ResponseData:
        """
        获取字体列表
        """
        response = self.client.request("GET", "font_list")
        return response.data