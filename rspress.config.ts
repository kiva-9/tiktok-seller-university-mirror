import * as path from 'path';
import { defineConfig } from 'rspress/config';
import * as fs from 'fs';
import * as yaml from 'js-yaml';
import { execFileSync } from 'child_process';

// 每次构建都重新生成 sidebar，避免同步新增文章后导航仍然陈旧。
const SIDEBAR_FILE = path.join(__dirname, 'sidebar.yml');
execFileSync('python3', ['scripts/generate_sidebar.py'], {
  cwd: __dirname,
  stdio: 'inherit',
});
const sidebar = yaml.load(fs.readFileSync(SIDEBAR_FILE, 'utf-8')) as Record<string, any[]>;

export default defineConfig({
  root: 'docs',
  // GitHub Pages 项目站点需要 base 路径
  base: '/tiktok-seller-university-mirror/',
  // 使用 hash 路由（避免 GitHub Pages SPA 404）
  useHashRouting: true,
  title: 'TikTok Shop Academy BR',
  description: 'TikTok Seller University Brazil knowledge base mirror',
  lang: 'pt-BR',
  globalStyles: path.join(__dirname, 'assets/custom.css'),
  // 搜索配置
  search: {
    codeSearch: true,
    localSearch: true,
  },
  // 全局 head
  head: [
    ['link', { rel: 'icon', href: '/tiktok-seller-university-mirror/favicon.svg' }],
  ],
  // 默认主题配置
  themeConfig: {
    // 导航栏
    nav: [
      { text: '首页', link: '/' },
      { text: 'Cursos', link: '/cursos/' },
      { text: 'Feature Guide', link: '/feature-guide/' },
      { text: 'Policy Center', link: '/policy-center/' },
    ],
    // 侧边栏（从 sidebar.yml 自动生成）
    sidebar,
    socialLinks: [
      {
        icon: 'github',
        mode: 'link',
        content: 'https://github.com/kiva-9/tiktok-seller-university-mirror',
      },
    ],
    // 页脚
    footer: {
      message: '本文档仅用于学习研究，文章版权归 TikTok / TikTok Shop 所有。',
      copyright: 'Copyright © 2026 TikTok Shop Academy Mirror',
    },
  },
});
