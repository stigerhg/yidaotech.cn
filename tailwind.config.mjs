/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  theme: {
    extend: {
      colors: {
        primary: '#1c841c',
        'primary-dark': '#146214',
        'primary-light': '#e8f5e8',
        accent: '#f5a623',
      },
      fontFamily: {
        sans: ['Inter', 'Microsoft YaHei', '微软雅黑', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
