# TikTok Seller University (BR) - 镜像库

TikTok Shop 卖家大学（巴西站）知识库的纯文本镜像，供 LLM / RAG 知识库使用。

## 数据来源

- 站点：<https://seller-br.tiktok.com/university/home?identity=1>
- 语言：葡萄牙语（pt-BR）
- 同步方式：通过底层 API 抓取 + HTML→Markdown 转换
- 同步频率：每日自动（GitHub Actions）

## 目录结构

```
docs/
├── cursos/          # 课程（Courses）
├── feature-guide/   # 功能指南（Feature Guide）
└── policy-center/   # 政策中心（Policy Center）
```

## 使用方式

```bash
# 安装依赖
pip install -r requirements.txt

# 手动同步
python scripts/main.py
```

## 自动化

`.github/workflows/daily-sync.yml` 每日 UTC 凌晨自动同步并 push。

## 免责声明

本仓库仅用于学习研究，文章版权归 TikTok / TikTok Shop 所有。
