"""
Session Manager - 管理HTTP会话、认证、Cookie和代理
"""
import json
import requests
from pathlib import Path
from typing import Dict, Optional, Any
from src.utils.logger import get_logger

logger = get_logger()


class SessionManager:
    """HTTP会话管理器，支持认证、Cookie、代理等"""

    def __init__(self, cookie_dir: str = "data/cookies"):
        """
        初始化会话管理器

        Args:
            cookie_dir: Cookie存储目录
        """
        self.cookie_dir = Path(cookie_dir)
        self.cookie_dir.mkdir(parents=True, exist_ok=True)
        self.sessions: Dict[str, requests.Session] = {}

    def get_session(self, source_name: str, config: Optional[Dict[str, Any]] = None) -> requests.Session:
        """
        获取或创建一个会话

        Args:
            source_name: 源名称，用于标识会话
            config: 配置字典，包含：
                - auth: 认证配置 {type: 'basic'|'token'|'session', username, password, token}
                - proxy: 代理配置 {http: 'http://...', https: 'https://...'}
                - headers: 自定义请求头
                - cookies: Cookie配置 {key: value} 或 文件路径
                - user_agent: User-Agent字符串
                - timeout: 超时时间
                - verify_ssl: 是否验证SSL证书

        Returns:
            配置好的requests.Session对象
        """
        # 如果已存在会话，返回
        if source_name in self.sessions:
            return self.sessions[source_name]

        # 创建新会话
        session = requests.Session()

        if config:
            # 设置User-Agent
            if 'user_agent' in config:
                session.headers['User-Agent'] = config['user_agent']

            # 设置自定义请求头
            if 'headers' in config:
                session.headers.update(config['headers'])

            # 设置代理
            if 'proxy' in config:
                session.proxies.update(config['proxy'])
                logger.info(f"[{source_name}] 使用代理: {config['proxy']}")

            # 加载Cookie
            if 'cookies' in config:
                self._load_cookies(session, source_name, config['cookies'])

            # SSL验证
            if 'verify_ssl' in config:
                session.verify = config['verify_ssl']

            # 处理认证
            if 'auth' in config:
                self._setup_auth(session, source_name, config['auth'])

        # 保存会话
        self.sessions[source_name] = session
        return session

    def _load_cookies(self, session: requests.Session, source_name: str, cookie_config: Any):
        """
        加载Cookie

        Args:
            session: Session对象
            source_name: 源名称
            cookie_config: Cookie配置（字典、文件路径或'auto'）
        """
        if isinstance(cookie_config, dict):
            # 直接设置Cookie字典
            session.cookies.update(cookie_config)
            logger.info(f"[{source_name}] 加载了 {len(cookie_config)} 个Cookie")

        elif isinstance(cookie_config, str):
            if cookie_config == 'auto':
                # 自动从文件加载
                cookie_file = self.cookie_dir / f"{source_name}.json"
                if cookie_file.exists():
                    with open(cookie_file, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
                        session.cookies.update(cookies)
                        logger.info(f"[{source_name}] 从文件加载了Cookie: {cookie_file}")
            else:
                # 从指定文件加载
                cookie_file = Path(cookie_config)
                if cookie_file.exists():
                    with open(cookie_file, 'r', encoding='utf-8') as f:
                        cookies = json.load(f)
                        session.cookies.update(cookies)
                        logger.info(f"[{source_name}] 从 {cookie_file} 加载了Cookie")

    def save_cookies(self, source_name: str):
        """
        保存会话的Cookie到文件

        Args:
            source_name: 源名称
        """
        if source_name not in self.sessions:
            logger.warning(f"[{source_name}] 会话不存在，无法保存Cookie")
            return

        session = self.sessions[source_name]
        cookie_file = self.cookie_dir / f"{source_name}.json"

        # 将Cookie转换为字典
        cookies = requests.utils.dict_from_cookiejar(session.cookies)

        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(cookies, f, indent=2, ensure_ascii=False)

        logger.info(f"[{source_name}] Cookie已保存到: {cookie_file}")

    def _setup_auth(self, session: requests.Session, source_name: str, auth_config: Dict[str, Any]):
        """
        设置认证

        Args:
            session: Session对象
            source_name: 源名称
            auth_config: 认证配置
        """
        auth_type = auth_config.get('type', 'none')

        if auth_type == 'basic':
            # HTTP Basic认证
            username = auth_config.get('username')
            password = auth_config.get('password')
            if username and password:
                session.auth = (username, password)
                logger.info(f"[{source_name}] 设置Basic认证: {username}")

        elif auth_type == 'bearer' or auth_type == 'token':
            # Bearer Token认证
            token = auth_config.get('token')
            if token:
                session.headers['Authorization'] = f"Bearer {token}"
                logger.info(f"[{source_name}] 设置Bearer Token认证")

        elif auth_type == 'api_key':
            # API Key认证
            api_key = auth_config.get('api_key')
            key_name = auth_config.get('key_name', 'X-API-Key')
            if api_key:
                session.headers[key_name] = api_key
                logger.info(f"[{source_name}] 设置API Key认证: {key_name}")

        elif auth_type == 'session':
            # Session-based认证（需要登录）
            login_url = auth_config.get('login_url')
            username = auth_config.get('username')
            password = auth_config.get('password')
            login_data = auth_config.get('login_data', {})

            if login_url and username and password:
                # 准备登录数据
                login_payload = {**login_data}
                login_payload[auth_config.get('username_field', 'username')] = username
                login_payload[auth_config.get('password_field', 'password')] = password

                try:
                    # 执行登录
                    logger.info(f"[{source_name}] 正在登录: {login_url}")
                    response = session.post(login_url, data=login_payload, timeout=30)

                    if response.ok:
                        logger.info(f"[{source_name}] 登录成功")
                        # 自动保存Cookie
                        self.save_cookies(source_name)
                    else:
                        logger.error(f"[{source_name}] 登录失败: {response.status_code}")

                except Exception as e:
                    logger.error(f"[{source_name}] 登录异常: {e}")

        elif auth_type == 'custom':
            # 自定义认证头
            custom_headers = auth_config.get('headers', {})
            session.headers.update(custom_headers)
            logger.info(f"[{source_name}] 设置自定义认证头")

    def close_session(self, source_name: str):
        """
        关闭会话

        Args:
            source_name: 源名称
        """
        if source_name in self.sessions:
            self.sessions[source_name].close()
            del self.sessions[source_name]
            logger.debug(f"[{source_name}] 会话已关闭")

    def close_all(self):
        """关闭所有会话"""
        for source_name in list(self.sessions.keys()):
            self.close_session(source_name)
        logger.info("所有会话已关闭")
