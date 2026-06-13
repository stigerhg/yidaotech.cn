import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

import cloudflare from "@astrojs/cloudflare";

export default defineConfig({
  site: 'https://yidaotech.xyz',
  integrations: [tailwind(), sitemap()],

  markdown: {
    shikiConfig: { theme: 'github-light' },
  },

  adapter: cloudflare()
});