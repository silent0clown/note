from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any


@dataclass
class Article:
    """Data model for news articles"""
    title: str
    url: str
    source: str
    category: str
    published_date: datetime
    content: Optional[str] = None
    summary: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    hash: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert article to dictionary for serialization"""
        data = asdict(self)
        # Convert datetime to ISO format string
        data['published_date'] = self.published_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Article':
        """Create article from dictionary"""
        # Convert ISO format string back to datetime
        if isinstance(data['published_date'], str):
            data['published_date'] = datetime.fromisoformat(data['published_date'])
        return cls(**data)


@dataclass
class SourceConfig:
    """Configuration for a news source"""
    name: str
    enabled: bool
    type: str
    categories: List[Dict[str, Any]]
    config: Optional[Dict[str, Any]] = None  # 新增：源级别的配置（认证、代理、headers等）


@dataclass
class FetchSettings:
    """Settings for fetching articles"""
    timeout: int = 30
    user_agent: str = "Mozilla/5.0 (compatible; AutoNews/1.0)"
    max_articles_per_source: int = 50
    include_content: bool = True
    respect_robots_txt: bool = True
    proxy: Optional[Dict[str, str]] = None  # 全局代理配置
    headers: Optional[Dict[str, str]] = None  # 全局请求头
