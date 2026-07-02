import { defaultLocale, locales, localizedPath, t } from '../i18n';
import type { Locale } from '../i18n';

const SITE_URL = 'https://yidaotech.xyz';

const labelMap: Record<string, keyof ReturnType<typeof t>['nav']> = {
  products: 'products',
  about: 'about',
  contact: 'contact',
  news: 'news',
  'case-studies': 'caseStudies',
};

export function absoluteUrl(path: string) {
  if (path.startsWith('http://') || path.startsWith('https://')) return path;
  return `${SITE_URL}${path.startsWith('/') ? path : `/${path}`}`;
}

export function alternateLinks(pathname: string) {
  const normalized = pathname.endsWith('/') ? pathname : `${pathname}/`;
  const parts = normalized.split('/').filter(Boolean);
  if (parts.length && locales.includes(parts[0] as Locale)) parts.shift();
  const unprefixed = `/${parts.join('/')}${parts.length ? '/' : ''}`;

  return [
    ...locales.map((locale) => ({
      hreflang: locale,
      href: absoluteUrl(localizedPath(locale, unprefixed)),
    })),
    {
      hreflang: 'x-default',
      href: absoluteUrl(localizedPath(defaultLocale, unprefixed)),
    },
  ];
}

export function breadcrumbSchema(lang: Locale, pathname: string, currentName?: string) {
  const copy = t(lang);
  const normalized = pathname.endsWith('/') ? pathname : `${pathname}/`;
  const parts = normalized.split('/').filter(Boolean).filter((part) => !locales.includes(part as Locale));

  const elements = [
    {
      '@type': 'ListItem',
      position: 1,
      name: copy.nav.home,
      item: absoluteUrl(localizedPath(lang, '/')),
    },
  ];

  let currentPath = '';
  parts.forEach((part, index) => {
    currentPath += `/${part}`;
    const isLast = index === parts.length - 1;
    const translated = labelMap[part] ? copy.nav[labelMap[part]] : undefined;
    const fallback = decodeURIComponent(part)
      .split('-')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');

    elements.push({
      '@type': 'ListItem',
      position: index + 2,
      name: isLast && currentName ? currentName : translated ?? fallback,
      item: absoluteUrl(localizedPath(lang, `${currentPath}/`)),
    });
  });

  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: elements,
  };
}

export function productTitle(title: string, category: string) {
  return `${title} | ${category} | Shining Road Technology`;
}

function truncateDescription(value: string, maxLength = 158) {
  const trimmed = value.replace(/\s+/g, ' ').trim();
  if (trimmed.length <= maxLength) return trimmed;

  const sliced = trimmed.slice(0, maxLength - 1);
  const lastSpace = sliced.lastIndexOf(' ');
  return `${(lastSpace > 120 ? sliced.slice(0, lastSpace) : sliced).trim()}.`;
}

export function metaDescription(description: string, cta = 'Contact us for specifications, samples, and bulk pricing.') {
  const trimmed = description.replace(/\s+/g, ' ').trim();
  const withCta = `${trimmed} ${cta}`;
  return truncateDescription(withCta.length <= 160 ? withCta : trimmed);
}

export function productMetaDescription(lang: Locale, description: string) {
  const ctaByLang: Record<Locale, string> = {
    en: 'Contact us for samples and export pricing.',
    ru: 'Запросите образцы и экспортную цену.',
    ar: 'تواصل معنا للعينات وأسعار التصدير.',
    id: 'Hubungi kami untuk sampel dan harga ekspor.',
    zh: '欢迎咨询样品和出口报价。',
  };

  return metaDescription(description, ctaByLang[lang]);
}

export function productImageAlt(title: string, category: string) {
  return `${title} - ${category} product by Shining Road Technology`;
}
