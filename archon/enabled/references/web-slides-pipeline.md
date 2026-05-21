# Web Slides 输出管道

> reveal.js + Python HTTP Server + Cloudflare Tunnel 的三层架构，为 Xuan Master 分析产出提供公网可访问的演示文稿。

## 目录结构

```
/tmp/slides/
├── <subject-slug>/          ← 每个主题一个子目录，互不冲突
│   ├── index.html           ← reveal.js 幻灯片（单文件，CDN 依赖）
│   └── guide.pdf            ← 同名 PDF 下载
├── another-topic/
│   ├── index.html
│   └── guide.pdf
└── ...
```

## 三步启动

### 1. 生成 HTML 幻灯片

使用 reveal.js 5.x CDN，暗色主题，单文件自包含。关键样式：
- 中文字体：`WenQuanYi Zen Hei` / `Noto Sans CJK SC`
- 模型编号用 `.model-tag` 标签
- 危险/安全区域用 `.danger-zone` / `.safe-zone`
- 状态机图用 `.state-diagram`（monospace pre）

模板参考：`templates/slides-template.html`

### 2. 启动 HTTP 服务器

```bash
# 停旧启新
kill $(lsof -t -i:8888) 2>/dev/null
cd /tmp/slides && python3 -m http.server 8888 &
```

验证：`curl -s -o /dev/null -w '%{http_code}' http://localhost:8888/<slug>/`

### 3. 打通公网访问（Cloudflare Tunnel）

```bash
# 安装（一次性）
curl -L https://github.com/cloudflare/cloudflare/releases/latest/download/cloudflared-linux-amd64 -o /tmp/cloudflared
chmod +x /tmp/cloudflared

# 启动隧道（后台）
/tmp/cloudflared tunnel --url http://localhost:8888 --no-autoupdate > /tmp/cf-tunnel.log 2>&1 &

# 获取 URL
grep trycloudflare.com /tmp/cf-tunnel.log
```

### 4. 更新飞书文档末尾

在每个飞书文档末尾追加资源链接：

```python
blocks = [
    divider(),
    h2('📎 附加资源'),
    p(f'PDF 下载：{base_url}/{slug}/guide.pdf'),
    p(f'Web Slides：{base_url}/{slug}/'),
    gap(),
    p('提示：点击上方链接即可直接访问。Slides 用方向键翻页，Esc 看总览。'),
]
append_blocks(doc_id, blocks)
```

## 自定义域名（Cloudflare Tunnel 命名隧道）

Quick Tunnel 的 URL 是临时的（`*.trycloudflare.com`）。要使用自定义域名（如 `apollo.agileway.ai`），需要：

1. Cloudflare API Token（权限：`Account → Cloudflare Tunnel → Edit`）
2. 创建命名隧道 + 配置 DNS CNAME

详见 Cloudflare 文档：https://developers.cloudflare.com/cloudflare-one/connections/connect-apps

## reveal.js 快捷键

| 键 | 功能 |
|----|------|
| `→` `↓` `Space` | 下一页 |
| `←` `↑` | 上一页 |
| `Esc` | 缩略图总览 |
| `F` | 全屏 |
| `S` | 演讲者模式（计时器+备注） |
