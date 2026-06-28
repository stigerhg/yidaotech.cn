import en from './translations/en.json';
import ru from './translations/ru.json';
import ar from './translations/ar.json';
import id from './translations/id.json';
import zh from './translations/zh.json';

export const languages = {
  en: { label: 'English', native: 'English', dir: 'ltr', ogLocale: 'en_US' },
  ru: { label: 'Russian', native: 'Русский', dir: 'ltr', ogLocale: 'ru_RU' },
  ar: { label: 'Arabic', native: 'العربية', dir: 'rtl', ogLocale: 'ar_AR' },
  id: { label: 'Indonesian', native: 'Bahasa Indonesia', dir: 'ltr', ogLocale: 'id_ID' },
  zh: { label: 'Chinese', native: '中文', dir: 'ltr', ogLocale: 'zh_CN' },
} as const;

export type Locale = keyof typeof languages;

export const locales = Object.keys(languages) as Locale[];
export const defaultLocale: Locale = 'en';
export const nonDefaultLocales = locales.filter((locale) => locale !== defaultLocale);
export const translations = { en, ru, ar, id, zh } as const;

export function isLocale(value: string | undefined): value is Locale {
  return !!value && locales.includes(value as Locale);
}

export function getLocale(value: string | undefined): Locale {
  return isLocale(value) ? value : defaultLocale;
}

export function getDir(lang: Locale): 'ltr' | 'rtl' {
  return languages[lang].dir;
}

export function t(lang: Locale) {
  return translations[lang];
}

export function localizedPath(lang: Locale, path = '/') {
  const normalized = path.startsWith('/') ? path : `/${path}`;
  if (lang === defaultLocale) return normalized;
  return `/${lang}${normalized === '/' ? '/' : normalized}`;
}

export function unprefixedPath(pathname: string) {
  const parts = pathname.split('/').filter(Boolean);
  if (isLocale(parts[0])) parts.shift();
  return `/${parts.join('/')}${pathname.endsWith('/') && parts.length ? '/' : ''}`;
}

export function translateProduct(lang: Locale, product: any) {
  const overlay = (translations[lang] as any).products?.[product.slug] ?? {};
  return {
    ...product.data,
    ...overlay,
    image: product.data.image,
    gallery: product.data.gallery,
    order: product.data.order,
    draft: product.data.draft,
  };
}
