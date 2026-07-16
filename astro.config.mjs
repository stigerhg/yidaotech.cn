import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

import cloudflare from "@astrojs/cloudflare";

const defaultLocale = 'en';
const locales = ['en', 'ru', 'ar', 'id', 'zh'];
const sitemapLocales = Object.fromEntries(locales.map((locale) => [locale, locale]));

function addXDefaultSitemapLink(item) {
  if (!item.links?.length || item.links.some((link) => link.lang === 'x-default')) {
    return item;
  }

  const defaultLink = item.links.find((link) => link.lang === defaultLocale);
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

const productRedirectTargets = {
  'cold-mix-pothole-repair': 'standard-cold-patch',
  'pavement-sealcoat': 'black-pavement-sealcoat',
  'ultra-thin-anti-skid-pavement': 'color-pavement-sealcoat',
  'color-sprayed-pavement': 'color-pavement-sealcoat',
  'color-cold-patch-asphalt': 'color-pavement-sealcoat',
  'color-asphalt-granules': 'color-pavement-sealcoat',
  'cold-mix-production-plant': 'cold-mix-additive',
  'cold-pour-crack-filler': 'black-pavement-sealcoat',
  'crack-sealing-tape': 'black-pavement-sealcoat',
  'emulsified-asphalt': 'black-pavement-sealcoat',
  'hot-applied-crack-sealer': 'black-pavement-sealcoat',
  'technology-licensing': 'cold-mix-additive',
  'quick-repair-cement': 'standard-cold-patch',
};

const localizedProductRedirects = Object.fromEntries(
  ['', ...locales.filter((locale) => locale !== defaultLocale).map((locale) => `/${locale}`)].flatMap((prefix) =>
    Object.entries(productRedirectTargets).map(([oldSlug, newSlug]) => [
      `${prefix}/products/${oldSlug}/`,
      { status: 301, destination: `${prefix}/products/${newSlug}/` },
    ])
  )
);

export default defineConfig({
  site: 'https://yidaotech.xyz',
  redirects: localizedProductRedirects,

  integrations: [tailwind(), sitemap({
    i18n: {
      defaultLocale,
      locales: sitemapLocales,
    },
    serialize: addXDefaultSitemapLink,
  })],

  i18n: {
    defaultLocale,
    locales,
    routing: {
      prefixDefaultLocale: false,
    },
  },

  markdown: {
    shikiConfig: { theme: 'github-light' },
  },

  adapter: cloudflare()
});