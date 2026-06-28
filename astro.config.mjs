import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

function addXDefaultSitemapLink(item) {
  if (!item.links?.length || item.links.some((link) => link.lang === 'x-default')) {
    return item;
  }

  const defaultLink = item.links.find((link) => link.lang === 'en');
  if (!defaultLink) return item;

  return {
    ...item,
    links: [
      ...item.links,
      {
        lang: 'x-default',
        url: defaultLink.url,
      },
    ],
  };
}

export default defineConfig({
  site: 'https://yidaotech.xyz',
  redirects: {
    '/products/color-cold-patch-asphalt/': '/products/ultra-thin-anti-skid-pavement/',
    '/products/color-asphalt-granules/': '/products/ultra-thin-anti-skid-pavement/',
  },
  integrations: [tailwind(), sitemap({
    i18n: {
      defaultLocale: 'en',
      locales: {
        en: 'en',
        ru: 'ru',
        ar: 'ar',
        id: 'id',
        zh: 'zh',
      },
    },
    serialize: addXDefaultSitemapLink,
  })],
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
