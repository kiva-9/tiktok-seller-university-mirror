# TikTok Shop Academy BR - 镜像库

TikTok Shop 卖家大学（巴西站）知识库的纯文本镜像。

## 数据来源

- 站点：<https://seller-br.tiktok.com/university/home?identity=1>
- 语言：葡萄牙语（pt-BR）
- 同步方式：通过底层 API 抓取 + HTML→Markdown 转换
- 同步频率：每日自动（GitHub Actions）

## 内容结构

| 分类 | 说明 |
|---|---|
| [Cursos](cursos/index.md) | 课程（Courses） |
| [Feature Guide](feature-guide/index.md) | 功能指南 |
| [Policy Center](policy-center/index.md) | 政策中心 |

## 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 手动同步
python scripts/main.py

# 本地预览文档站
pip install mkdocs-material
mkdocs serve
```

## 免责声明

本仓库仅用于学习研究，文章版权归 TikTok / TikTok Shop 所有。
