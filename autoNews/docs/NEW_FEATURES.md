# AutoNews 新增功能：通用认证和代理系统

## 更新日期：2026-02-07

## 概述

AutoNews 现在支持完整的认证、Cookie和代理管理系统，可以访问需要登录、付费或被墙的新闻网站。

---

## 🎉 新功能

### 1. 多种认证方式

- **HTTP Basic 认证** - 标准用户名密码认证
- **Bearer Token 认证** - API Token认证
- **API Key 认证** - 自定义API Key头
- **Session 认证** - 自动登录并保持会话
- **自定义认证头** - 灵活的自定义认证方式

### 2. Cookie 管理

- **手动配置** - 直接在配置文件中指定Cookie
- **自动管理** - 自动加载和保存Cookie到文件
- **浏览器导入** - 从Chrome/Firefox导出Cookie
- **持久化存储** - Cookie文件保存在 `data/cookies/`

### 3. 代理支持

- **HTTP/HTTPS 代理** - 支持标准HTTP代理
- **SOCKS5 代理** - 支持SOCKS5协议
- **带认证代理** - 支持需要用户名密码的代理
- **全局/源级别代理** - 可以为特定源配置独立代理

### 4. 灵活的配置

- **源级别配置** - 每个新闻源可以有独立的配置
- **全局默认配置** - 设置全局默认值，源配置可覆盖
- **自定义请求头** - 完全控制HTTP请求头

---

## 🚀 快速开始

### 场景1：访问需要更真实浏览器头的网站（如36氪）

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
      headers:
        Accept: "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        Accept-Language: "zh-CN,zh;q=0.9,en;q=0.8"
        Referer: "https://www.36kr.com/"
      timeout: 20
```

### 场景2：访问需要翻墙的网站

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
        http: "http://127.0.0.1:7890"   # Clash默认端口
        https: "http://127.0.0.1:7890"
```

### 场景3：需要登录的付费网站

```yaml
sources:
  - name: "付费媒体"
    enabled: true
    type: "rss"
    categories:
      - name: "科技"
        url: "https://premium.example.com/feed"
        tags: ["科技"]
    config:
      auth:
        type: "session"
        login_url: "https://premium.example.com/login"
        username: "your_email@example.com"
        password: "your_password"
      cookies: "auto"  # 自动保存登录后的Cookie
```

---

## 📖 使用指南

### 配置文件位置

- **主配置**: `config/config.yaml`
- **新闻源配置**: `config/sources.yaml`
- **配置示例**: `config/sources.example.yaml` （包含所有功能示例）
- **Cookie存储**: `data/cookies/{源名称}.json`

### Cookie 管理工具

我们提供了便捷的 Cookie 管理工具：

```bash
# 导入Cookie（从浏览器导出的JSON文件）
python tools/cookie_helper.py import "36氪" cookies.json

# 验证Cookie是否有效
python tools/cookie_helper.py validate "36氪" https://www.36kr.com/

# 列出所有已保存的Cookie
python tools/cookie_helper.py list

# 查看特定源的Cookie
python tools/cookie_helper.py list "36氪"

# 删除Cookie
python tools/cookie_helper.py delete "36氪"
```

### 从浏览器导出 Cookie

**Chrome/Edge:**
1. 安装扩展：[EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/)
2. 访问目标网站并登录
3. 点击扩展图标 → Export
4. 保存为 JSON 文件

**Firefox:**
1. 安装扩展：[Cookie-Editor](https://addons.mozilla.org/firefox/addon/cookie-editor/)
2. 访问目标网站并登录
3. 点击扩展图标 → Export → JSON
4. 保存为 JSON 文件

---

## 📚 详细文档

完整的配置说明和示例，请查看：

- **[认证与代理配置指南](AUTHENTICATION_GUIDE.md)** - 详细的配置说明和FAQ
- **[配置示例文件](../config/sources.example.yaml)** - 包含所有功能的完整示例

---

## 🔧 技术实现

### 新增文件

- `src/core/session_manager.py` - 会话管理器，处理认证、Cookie、代理
- `tools/cookie_helper.py` - Cookie管理辅助工具
- `docs/AUTHENTICATION_GUIDE.md` - 详细配置指南

### 修改文件

- `src/models.py` - 增加源级别配置支持
- `src/fetchers/content_extractor.py` - 支持共享Session
- `main.py` - 集成SessionManager

### 数据结构

**源配置结构**:
```python
@dataclass
class SourceConfig:
    name: str
    enabled: bool
    type: str
    categories: List[Dict[str, Any]]
    config: Optional[Dict[str, Any]] = None  # 新增
```

**配置选项** (`config` 字段):
```yaml
config:
  user_agent: str           # 自定义User-Agent
  proxy: dict               # 代理配置
  headers: dict             # 自定义请求头
  cookies: dict|str         # Cookie配置
  auth: dict                # 认证配置
  timeout: int              # 超时时间
  verify_ssl: bool          # SSL验证
```

---

## ⚠️ 安全提示

1. **不要在配置文件中明文存储密码** - 使用环境变量或在运行时输入
2. **保护Cookie文件** - 设置适当的文件权限：`chmod 600 data/cookies/*.json`
3. **不要提交敏感信息到Git** - 在 `.gitignore` 中排除Cookie文件和包含密码的配置

---

## 🐛 常见问题

### Q: 36氪的内容还是无法获取怎么办？

A: 36氪有较强的反爬虫保护，建议：
1. 使用更真实的浏览器头（已在配置中添加）
2. 增加请求间隔时间
3. 考虑使用Cookie（从浏览器导出）
4. 如果仍然失败，可能需要使用Selenium等浏览器自动化工具

### Q: 代理不工作怎么办？

A: 检查以下几点：
1. 代理软件是否正在运行
2. 端口号是否正确（Clash默认7890，V2Ray默认1080）
3. 代理格式是否正确
4. 查看日志确认代理是否被使用

### Q: Session认证登录失败？

A: 确认：
1. `username_field` 和 `password_field` 是否匹配网站表单
2. 是否需要额外的表单字段（如CSRF token）
3. 查看日志中的详细错误信息

---

## 🔄 下一步计划

- [ ] 添加更多认证方式（OAuth2等）
- [ ] 支持浏览器自动化（Selenium/Playwright）
- [ ] Cookie自动刷新机制
- [ ] 代理池支持
- [ ] 验证码处理

---

## 💡 贡献

如果您有任何建议或发现问题，欢迎反馈！

---

**享受您的自动化新闻聚合之旅！** 🎊
