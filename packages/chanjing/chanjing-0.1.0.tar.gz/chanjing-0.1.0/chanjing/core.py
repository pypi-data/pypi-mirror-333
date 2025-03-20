import requests
import json
import logging
from typing import Dict, Any, Optional
from .schemas import APIResponse




class ChanjingHttpClient(object):

    def __init__(self,app_id: str, app_secret: str, base_url: str = "https://www.chanjing.cc/api/open/v1") -> None:
        """
        初始化禅境HTTP客户端
        Args:
            app_id: API应用ID
            app_secret: API应用密钥
            base_url: API基础URL，默认为"https://www.chanjing.cc/api/open/v1"
        """
        self.base_url = base_url
        url =  f"{self.base_url}/access_token"
        headers = {
            "Content-Type": "application/json",
            "charset ": "utf-8"
        }
        payload = {
                "app_id": app_id,
                "secret_key": app_secret
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
           self.access_token = response.json()['data']['access_token']
        else:
            raise Exception(f"Failed to get access token: {response.text}")
       
        """
        初始化禅境HTTP客户端
        
        Args:
            access_token: API访问令牌
            base_url: API基础URL，默认为"https://www.chanjing.cc/api/open/v1"
        """
        
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.logger = logging.getLogger("chanjing")
        
    def request(self, method: str, url: str, **kwargs) -> APIResponse:
        """
        发送HTTP请求到禅境API
        
        Args:
            method: HTTP方法 (GET, POST, PUT, DELETE等)
            url: API端点路径（不包含基础URL）
            **kwargs: 传递给requests库的额外参数
            
        Returns:
            APIResponse: API响应对象
            
        Raises:
            ValueError: 当HTTP方法不支持或参数无效时
            ConnectionError: 当网络连接失败时
            TimeoutError: 当请求超时时
            Exception: 其他异常情况
        """
        method = method.upper()
        if method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            raise ValueError(f"不支持的HTTP方法: {method}")
            
        # 构建完整URL
        full_url = f"{self.base_url}/{url.lstrip('/')}"
        
        # 设置请求头
        headers = kwargs.pop("headers", {})
        headers.update({
            "access_token": self.access_token,
            "Content-Type": "application/json",
            "Accept": "application/json",
            "charset": "utf-8"
        })
        
        # 记录请求信息（不包含敏感信息）
        safe_headers = {k: v for k, v in headers.items() if k.lower() != "access_token"}
        self.logger.debug(f"发送 {method} 请求到 {full_url}")
        self.logger.debug(f"请求头: {safe_headers}")
        
        try:
            # 发送请求
            response = self.session.request(
                method=method,
                url=full_url,
                headers=headers,
                timeout=30,  # 默认超时时间为30秒
                **kwargs
            )
            
            # 尝试解析JSON响应
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                self.logger.error(f"无法解析JSON响应: {response.text[:100]}...")
                raise ValueError(f"API返回了无效的JSON响应: {response.text[:100]}...")
            
            # 记录响应信息
            self.logger.debug(f"收到状态码: {response.status_code}")
            self.logger.debug(f"响应数据: {response_data}")
            
            # 检查HTTP状态码
            response.raise_for_status()
            
            # 将响应数据转换为APIResponse对象
            api_response = APIResponse.model_validate(response_data)
            
            # 检查API错误码
            if api_response.code != 0:
                self.logger.warning(f"API错误: 代码={api_response.code}, 消息={api_response.msg}")
            
            return api_response
            
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"连接错误: {str(e)}")
            raise ConnectionError(f"无法连接到禅境API: {str(e)}")
        except requests.exceptions.Timeout as e:
            self.logger.error(f"请求超时: {str(e)}")
            raise TimeoutError(f"禅境API请求超时: {str(e)}")
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP错误: {str(e)}")
            raise Exception(f"禅境API返回错误: {str(e)}")
        except Exception as e:
            self.logger.error(f"请求过程中发生异常: {str(e)}")
            raise Exception(f"禅境API请求失败: {str(e)}")