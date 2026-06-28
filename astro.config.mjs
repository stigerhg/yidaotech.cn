import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://yidaotech.xyz',
  redirects: {
    '/products/color-cold-patch-asphalt/': '/products/ultra-thin-anti-skid-pavement/',
    '/products/color-asphalt-granules/': '/products/ultra-thin-anti-skid-pavement/',
  },
  integrations: [tailwind(), sitemap()],
  i18n: {
    defaultLocale: 'en',
    locales: ['en', 'ru', 'ar', 'id', 'zh'],
    routing: {
      prefixDefaultLocale: false,
    },
  },
  markdown: {
    shikiConfig: { theme: 'github-light' },
  },
});
