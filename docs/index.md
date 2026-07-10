# TikTok Shop Academy BR

TikTok Shop 卖家大学（巴西站）知识库镜像，包含 372 篇文章、视频链接和完整元数据。

## 数据来源

- 站点：<https://seller-br.tiktok.com/university/home?identity=1>
- 语言：葡萄牙语（pt-BR）
- 同步方式：通过底层 API 抓取 + HTML→Markdown 转换
- 同步频率：每日自动（GitHub Actions）

## 内容分类

| 分类 | 说明 |
|---|---|
| [Cursos](/cursos/) | 课程（Courses） - 78 篇 |
| [Feature Guide](/feature-guide/) | 功能指南 - 196 篇 |
| [Policy Center](/policy-center/) | 政策中心 - 98 篇 |

## 技术栈

- 数据抓取：Python requests + BeautifulSoup
- 文档站：Rspress
- 自动同步：GitHub Actions（每日 UTC 02:00）

## 本地开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建
npm run build
```

## 免责声明

本仓库仅用于学习研究，文章版权归 TikTok / TikTok Shop 所有。
