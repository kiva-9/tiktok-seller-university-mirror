import * as path from 'path';
import { defineConfig } from 'rspress/config';
import * as fs from 'fs';
import * as yaml from 'js-yaml';

// 动态读取 sidebar.yml（如果存在），否则自动生成
const SIDEBAR_FILE = path.join(__dirname, 'sidebar.yml');
if (!fs.existsSync(SIDEBAR_FILE)) {
  require('child_process').execSync('python scripts/generate_sidebar.py');
}
const sidebar = yaml.load(fs.readFileSync(SIDEBAR_FILE, 'utf-8')) as Record<string, any[]>;

export default defineConfig({
  root: 'docs',
  // GitHub Pages 项目站点需要 base 路径
  base: '/tiktok-seller-university-mirror/',
  // 使用 hash 路由（避免 GitHub Pages SPA 404）
  useHashRouting: true,
  title: 'TikTok Shop Academy BR',
  description: 'TikTok Seller University Brazil knowledge base mirror',
  lang: 'zh',
  // 搜索配置
  search: {
    codeSearch: true,
    localSearch: true,
  },
  // 全局 head
  head: [
    ['link', { rel: 'icon', href: '/tiktok-seller-university-mirror/favicon.png' }],
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
