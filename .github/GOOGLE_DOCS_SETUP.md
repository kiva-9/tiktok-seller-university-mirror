# Google Docs 同步设置指南

本仓库的 CI 在每日同步完成后，会将 `docs/` 下所有 `.md` 文件（除 `index.md`）合并为一个文档，并覆写到指定的 Google Docs 中。

## 总体流程

```
GitHub 多 .md 文件 → 脚本合流（目录 + 隔离标头） → Google Docs API 覆写 → NotebookLM 自动刷新
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

1. 打开 [Google Docs](https://docs.google.com/)，新建空白文档
2. 看地址栏获取文档 ID：

   ```
   https://docs.google.com/document/d/{DOCUMENT_ID}/edit
   ```

3. 把这个文档**共享给服务账号邮箱**：
   - 点右上角 **Share**
   - 粘贴服务账号邮箱（`xxx@project.iam.gserviceaccount.com`）
   - 权限选 **Editor**，点 **Send**

## 第五步：填入 GitHub Secrets

回到你的 GitHub 仓库 → **Settings → Secrets and variables → Actions**，添加 2 个 Secret：

| Name | Value |
|------|-------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | 第三步下载的 `.json` 文件的**完整内容**，直接粘贴 |
| `GOOGLE_DOCS_DOCUMENT_ID` | 第四步从 URL 拿到的文档 ID |

## 完成

设置完成后，下次 CI 运行（每日自动或手动触发）时，会自动合并文档并覆写到 Google Docs。

** NotebookLM 使用方式：**
1. NotebookLM 中添加这个 Google Docs
2. 之后每次 CI 运行都会原地更新，NotebookLM 自动刷新

## 验证

去 **Actions → Daily Sync Knowledge Base → Run workflow** 手动触发一次，跑完后去 Google Docs 确认内容格式正确（有目录、隔离标头、分割线）。
