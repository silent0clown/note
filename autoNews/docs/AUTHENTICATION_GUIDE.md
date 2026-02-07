# AutoNews 认证与代理配置指南

本指南详细介绍如何配置 AutoNews 以访问需要认证、Cookie、代理的新闻源。

## 目录

- [快速开始](#快速开始)
- [认证方式](#认证方式)
- [代理配置](#代理配置)
- [Cookie管理](#cookie管理)
- [完整示例](#完整示例)
- [常见问题](#常见问题)

---

## 快速开始

### 1. 基本配置（无认证）

最简单的配置，适用于公开的 RSS 源：

```yaml
sources:
  - name: "IT之家"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://www.ithome.com/rss/"
        tags: ["科技", "IT"]
```

### 2. 添加自定义 User-Agent

如果网站检查 User-Agent：

```yaml
sources:
  - name: "36氪"
    enabled: true
    type: "rss"
    categories:
      - name: "快讯"
        url: "https://www.36kr.com/feed-article"
        tags: ["科技"]
    config:
      user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
```

### 3. 添加代理

如果需要翻墙访问：

```yaml
sources:
  - name: "HackerNews"
    enabled: true
    type: "rss"
    categories:
      - name: "Top"
        url: "https://hnrss.org/frontpage"
        tags: ["tech"]
    config:
      proxy:
        http: "http://127.0.0.1:7890"
        https: "http://127.0.0.1:7890"
```

---

## 认证方式

AutoNews 支持 5 种认证方式：

### 1. HTTP Basic 认证

适用于使用标准 HTTP Basic Auth 的网站：

```yaml
sources:
  - name: "需要Basic认证的网站"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://example.com/feed"
        tags: ["tech"]
    config:
      auth:
        type: "basic"
        username: "your_username"
        password: "your_password"
```

### 2. Bearer Token 认证

适用于 API Token 认证：

```yaml
sources:
  - name: "API服务"
    enabled: true
    type: "rss"
    categories:
      - name: "文章"
        url: "https://api.example.com/feed"
        tags: ["tech"]
    config:
      auth:
        type: "bearer"  # 或 "token"
        token: "your_api_token_here"
```

**请求头会变成：**
```
Authorization: Bearer your_api_token_here
```

### 3. API Key 认证

适用于自定义 API Key 头：

```yaml
sources:
  - name: "API服务"
    enabled: true
    type: "rss"
    categories:
      - name: "新闻"
        url: "https://api.example.com/news"
        tags: ["news"]
    config:
      auth:
        type: "api_key"
        api_key: "your_api_key_here"
        key_name: "X-API-Key"  # 默认为 "X-API-Key"，可自定义
```

**请求头会变成：**
```
X-API-Key: your_api_key_here
```

### 4. Session 认证（需要登录）

适用于需要用户名密码登录的网站：

```yaml
sources:
  - name: "需要登录的网站"
    enabled: true
    type: "rss"
    categories:
      - name: "会员内容"
        url: "https://example.com/feed"
        tags: ["premium"]
    config:
      auth:
        type: "session"
        login_url: "https://example.com/login"
        username: "your_username"
        password: "your_password"
        username_field: "email"      # 默认 "username"
        password_field: "password"   # 默认 "password"
        login_data:                  # 额外的登录表单数据（可选）
          remember_me: "1"
          csrf_token: "xxx"
      cookies: "auto"  # 登录后自动保存Cookie
```

**登录流程：**
1. AutoNews 会自动发送 POST 请求到 `login_url`
2. 登录成功后，Cookie 会被保存到 `data/cookies/{源名称}.json`
3. 后续请求会自动使用这些 Cookie

### 5. 自定义认证头

适用于特殊认证方式：

```yaml
sources:
  - name: "自定义认证"
    enabled: true
    type: "rss"
    categories:
      - name: "文章"
        url: "https://example.com/feed"
        tags: ["tech"]
    config:
      auth:
        type: "custom"
        headers:
          Authorization: "Custom your_custom_auth_string"
          X-Custom-Header: "custom_value"
          X-User-ID: "12345"
```

---

## 代理配置

### 支持的代理类型

1. **HTTP 代理**
2. **HTTPS 代理**
3. **SOCKS5 代理**
4. **带认证的代理**

### 配置方式

#### 1. 源级别代理（推荐）

为特定源配置代理：

```yaml
sources:
  - name: "需要代理的网站"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://example.com/feed"
        tags: ["tech"]
    config:
      proxy:
        http: "http://127.0.0.1:7890"
        https: "http://127.0.0.1:7890"
```

#### 2. 全局代理

为所有源配置默认代理：

```yaml
fetch_settings:
  timeout: 15
  user_agent: "Mozilla/5.0 ..."
  proxy:
    http: "http://127.0.0.1:7890"
    https: "http://127.0.0.1:7890"
```

### 常见代理端口

| 工具    | 默认端口 | 协议         |
|---------|----------|--------------|
| Clash   | 7890     | HTTP/HTTPS   |
| V2Ray   | 1080     | SOCKS5       |
| SS      | 1080     | SOCKS5       |
| Surge   | 6152     | HTTP         |

### 代理格式示例

```yaml
# HTTP 代理
proxy:
  http: "http://127.0.0.1:7890"
  https: "http://127.0.0.1:7890"

# SOCKS5 代理
proxy:
  http: "socks5://127.0.0.1:1080"
  https: "socks5://127.0.0.1:1080"

# 带认证的代理
proxy:
  http: "http://username:password@proxy.example.com:8080"
  https: "http://username:password@proxy.example.com:8080"
```

---

## Cookie 管理

AutoNews 支持三种 Cookie 管理方式：

### 1. 手动配置 Cookie

直接在配置文件中指定 Cookie：

```yaml
sources:
  - name: "网站"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://example.com/feed"
        tags: ["tech"]
    config:
      cookies:
        session_id: "abc123xyz"
        user_token: "token_value"
        _ga: "GA1.2.xxxxxxxxx"
```

### 2. 自动管理 Cookie（推荐）

AutoNews 自动加载和保存 Cookie：

```yaml
sources:
  - name: "网站"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://example.com/feed"
        tags: ["tech"]
    config:
      cookies: "auto"
```

**Cookie 文件位置：** `data/cookies/网站.json`

**首次使用：**
1. 方式A：从浏览器复制 Cookie 到 `data/cookies/网站.json`
2. 方式B：使用 Session 认证自动登录生成

### 3. 指定 Cookie 文件

从特定文件加载 Cookie：

```yaml
sources:
  - name: "网站"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://example.com/feed"
        tags: ["tech"]
    config:
      cookies: "/path/to/cookies.json"
```

### Cookie 文件格式

```json
{
  "session_id": "your_session_value",
  "user_token": "your_token_value",
  "_ga": "GA1.2.xxxxxxxxx"
}
```

### 从浏览器导出 Cookie

**Chrome/Edge：**
1. 安装扩展：EditThisCookie
2. 访问目标网站并登录
3. 点击扩展图标 → Export
4. 复制JSON到文件

**Firefox：**
1. 安装扩展：Cookie-Editor
2. 访问目标网站并登录
3. 点击扩展图标 → Export → JSON
4. 保存到文件

---

## 完整示例

### 示例 1：36氪（反爬虫保护）

```yaml
sources:
  - name: "36氪"
    enabled: true
    type: "rss"
    categories:
      - name: "快讯"
        url: "https://www.36kr.com/feed-article"
        tags: ["科技", "创业"]
    config:
      user_agent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
      headers:
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        Accept-Language: "zh-CN,zh;q=0.9,en;q=0.8"
        Referer: "https://www.36kr.com/"
      timeout: 20
```

### 示例 2：付费订阅网站

```yaml
sources:
  - name: "付费媒体"
    enabled: true
    type: "rss"
    categories:
      - name: "科技"
        url: "https://premium.example.com/feed"
        tags: ["科技", "深度"]
    config:
      user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      auth:
        type: "session"
        login_url: "https://premium.example.com/login"
        username: "your_email@example.com"
        password: "your_password"
      cookies: "auto"
      timeout: 30
```

### 示例 3：需要代理 + 认证

```yaml
sources:
  - name: "国外付费媒体"
    enabled: true
    type: "rss"
    categories:
      - name: "全部"
        url: "https://international.example.com/feed"
        tags: ["international"]
    config:
      proxy:
        http: "http://127.0.0.1:7890"
        https: "http://127.0.0.1:7890"
      auth:
        type: "bearer"
        token: "your_api_token"
      user_agent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
      verify_ssl: true
```

---

## 常见问题

### Q1: 如何测试代理是否工作？

在配置中添加代理后，查看日志：

```bash
tail -f logs/autonews.log | grep proxy
```

应该看到：
```
[源名称] 使用代理: {'http': 'http://127.0.0.1:7890', 'https': 'http://127.0.0.1:7890'}
```

### Q2: Cookie 过期怎么办？

**方法1：** 重新从浏览器导出 Cookie

**方法2：** 使用 Session 认证自动登录

```yaml
config:
  auth:
    type: "session"
    login_url: "https://example.com/login"
    username: "user"
    password: "pass"
  cookies: "auto"  # 自动更新Cookie
```

### Q3: SSL 证书错误怎么办？

如果遇到 SSL 证书验证错误，可以禁用验证（不推荐）：

```yaml
config:
  verify_ssl: false
```

### Q4: 如何查看请求头是否正确？

启用调试日志：

```yaml
# config/config.yaml
logging:
  level: "DEBUG"
```

然后查看日志：
```bash
tail -f logs/autonews.log
```

### Q5: 代理需要认证怎么办？

在代理 URL 中包含用户名密码：

```yaml
proxy:
  http: "http://username:password@127.0.0.1:7890"
  https: "http://username:password@127.0.0.1:7890"
```

### Q6: 如何为不同的源使用不同的代理？

每个源可以有独立的代理配置：

```yaml
sources:
  - name: "国内网站"
    config:
      # 不配置代理，直连

  - name: "国外网站"
    config:
      proxy:
        http: "http://127.0.0.1:7890"
        https: "http://127.0.0.1:7890"
```

### Q7: 登录失败怎么办？

检查以下几点：

1. `username_field` 和 `password_field` 是否正确
2. 是否需要额外的表单字段（如 CSRF token）
3. 查看日志中的错误信息
4. 尝试手动在浏览器中登录，确认登录流程

---

## 安全建议

### 1. 不要在配置文件中明文存储密码

**推荐做法：** 使用环境变量

```yaml
# .env 文件
EXAMPLE_USERNAME=your_username
EXAMPLE_PASSWORD=your_password
```

```python
# 在代码中使用
import os
from dotenv import load_dotenv

load_dotenv()
username = os.getenv('EXAMPLE_USERNAME')
password = os.getenv('EXAMPLE_PASSWORD')
```

### 2. Cookie 文件权限

确保 Cookie 文件只有您可读：

```bash
chmod 600 data/cookies/*.json
```

### 3. 不要提交敏感信息到 Git

在 `.gitignore` 中添加：

```
data/cookies/
.env
config/sources.yaml  # 如果包含密码
```

---

## 更多帮助

如果遇到问题，请：

1. 查看日志：`tail -f logs/autonews.log`
2. 启用调试模式：设置 `logging.level: "DEBUG"`
3. 检查网络连接和代理设置
4. 查看完整配置示例：`config/sources.example.yaml`

---

最后更新：2026-02-07
