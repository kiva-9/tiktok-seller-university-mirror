import * as path from 'path';
import { defineConfig } from 'rspress/config';

export default defineConfig({
  root: 'docs',
  // GitHub Pages 项目站点需要 base 路径
  base: '/tiktok-seller-university-mirror/',
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
    // 侧边栏
    sidebar: {
      '/cursos/': [
        {
          text: 'Cursos',
          items: [
            { text: '入门指南', link: '/cursos/iniciar/' },
            { text: '成长策略', link: '/cursos/crescimento/' },
            { text: '进阶课程', link: '/cursos/avançado/' },
            { text: '直播指南', link: '/cursos/live/' },
            { text: '短视频', link: '/cursos/vídeo-curto/' },
            { text: '联盟营销', link: '/cursos/afiliado/' },
            { text: '选品策略', link: '/cursos/seleção-de-produtos/' },
            { text: '平台规则', link: '/cursos/regras-e-suporte-da-plataforma/' },
            { text: '网络研讨会', link: '/cursos/webinar/' },
            { text: '创作者入门', link: '/cursos/começar/' },
          ],
        },
      ],
      '/feature-guide/': [
        {
          text: 'Feature Guide',
          items: [
            { text: '入门指南', link: '/feature-guide/primeiros-passos/registro-e-configuração-da-conta/' },
            { text: '产品管理', link: '/feature-guide/produtos/gerenciar-produtos/' },
            { text: '订单管理', link: '/feature-guide/pedidos/gerenciar-pedidos/' },
            { text: '营销推广', link: '/feature-guide/marketing/' },
            { text: '联盟营销', link: '/feature-guide/afiliados/' },
            { text: '直播功能', link: '/feature-guide/live/' },
            { text: '数据分析', link: '/feature-guide/análise-de-dados/' },
            { text: '财务管理', link: '/feature-guide/finanças/' },
            { text: '广告推广', link: '/feature-guide/ads-anúncio-de-loja/' },
          ],
        },
      ],
      '/policy-center/': [
        {
          text: 'Policy Center',
          items: [
            { text: '注册政策', link: '/policy-center/registro/' },
            { text: '账户管理', link: '/policy-center/gerenciamento-de-conta/' },
            { text: '产品政策', link: '/policy-center/gerencie-seus-produtos/' },
            { text: '知识产权', link: '/policy-center/direitos-de-propriedade-intelectual/' },
            { text: '订单管理', link: '/policy-center/gerenciamento-de-pedidos/' },
            { text: '营销政策', link: '/policy-center/marketing/' },
            { text: '客户服务', link: '/policy-center/atendimento-ao-cliente/' },
            { text: '履约管理', link: '/policy-center/gerenciamento-de-desempenho/' },
            { text: '支付政策', link: '/policy-center/pagamentos/' },
            { text: '重点政策', link: '/policy-center/políticas-em-destaque/' },
          ],
        },
      ],
    },
    // 社交链接
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
