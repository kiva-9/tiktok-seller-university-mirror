# Google Docs 同步设置指南

本仓库的 CI 在每日同步完成后，会将 `docs/` 下所有 `.md` 文件按分类合流到多个 Google Docs 中。

## 总体流程

```
GitHub 多 .md 文件 → 按分类合流 + 自动拆分 → Google Docs API 覆写 → NotebookLM 自动刷新
```

## 第一步：创建 Google Cloud 项目并启用 API

1. 打开 [Google Cloud Console](https://console.cloud.google.com/)，确保你有一个项目
2. 左侧菜单 → **APIs & Services → Library**
3. 搜索并启用：**Google Docs API**

## 第二步：创建服务账号

1. 左侧菜单 → **IAM & Admin → Service Accounts**
2. 点 **+ Create Service Account**
3. 名称随意，如 `tiktok-docs-sync`，点 **Create and Continue**
4. Role 两步都可跳过，直接点 **Done**

## 第三步：创建服务账号密钥

1. 点刚创建的账号，切换 **Keys** 标签
2. **+ Add Key → Create new key**
3. 选 **JSON**，点 **Create** — 会下载一个 `.json` 文件
4. **打开这个文件，复制全部内容** — 这就是后续要填的 Secret 值

## 第四步：创建 Google Docs 目标文档

根据分类创建文档（共 10 个，其中 5 个备用）：

| 用途 | 标题建议 |
|------|---------|
| Cursos 主 | Cursos |
| Cursos 备用 1 | Cursos (备用) |
| Cursos 备用 2 | Cursos (备用) |
| Feature Guide 主 1 | Feature Guide (1/4) |
| Feature Guide 主 2 | Feature Guide (2/4) |
| Feature Guide 主 3 | Feature Guide (3/4) |
| Feature Guide 主 4 | Feature Guide (4/4) |
| Policy Center 主 | Policy Center |
| Policy Center 备用 1 | Policy Center (备用) |
| Policy Center 备用 2 | Policy Center (备用) |

**重要：** 把每个文档都共享给服务账号邮箱（`xxx@project.iam.gserviceaccount.com`），权限选 **Editor**。

从每个文档的 URL 中提取文档 ID：

```
https://docs.google.com/document/d/{DOCUMENT_ID}/edit
```

## 第五步：填入 GitHub Secrets

回到你的 GitHub 仓库 → **Settings → Secrets and variables → Actions**，添加 2 个 Secret：

### Secret 1: `GOOGLE_SERVICE_ACCOUNT_JSON`

粘贴第三步下载的 `.json` 文件完整内容。

### Secret 2: `GOOGLE_DOCS_DOCUMENT_IDS`

值是 JSON 格式，包含每个分类的 Doc ID 数组：

```json
{
  "cursos": ["ID_1", "ID_2", "ID_3"],
  "feature-guide": ["ID_4", "ID_5", "ID_6", "ID_7"],
  "policy-center": ["ID_8", "ID_9", "ID_10"]
}
```

**说明：**
- 每个分类至少提供一个 ID
- 脚本按需使用，多余的 ID 闲置作为备用
- 如果某分类内容增长超过当前文档容量上限（~1M 字符），脚本会自动使用下一个备用 ID
- **单篇文章不会跨文档拆分**

## 完成

设置完成后，下次 CI 运行（每日自动或手动触发）时，会自动合并文档并覆写到 Google Docs。

** NotebookLM 使用方式：**
1. NotebookLM 中添加所有 5 个（或更多）Google Docs
2. 之后每次 CI 运行都会原地更新，NotebookLM 自动刷新

## 验证

去 **Actions → Daily Sync Knowledge Base → Run workflow** 手动触发一次，跑完后去 Google Docs 确认内容格式正确（有目录、隔离标头、分割线）。
