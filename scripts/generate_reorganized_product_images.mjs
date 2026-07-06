import sharp from 'sharp';
import { mkdir, readFile } from 'node:fs/promises';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const productOut = join(root, 'public', 'images', 'products');
const ogOut = join(root, 'public', 'images');

const products = {
  'standard-cold-patch': {
    source: join(productOut, 'cold-mix-pothole-repair-hero.jpg'),
    title: 'Standard Cold Mix Asphalt',
    subtitle: 'All-weather pothole repair',
    accent: '#f59e0b',
  },
  'capsule-pressure-cold-patch': {
    source: join(productOut, 'cold-mix-pothole-repair-hero.jpg'),
    title: 'Capsule Pressure-Sensitive Cold Patch',
    subtitle: 'Smart traffic-activated repair',
    accent: '#166534',
  },
  'black-pavement-sealcoat': {
    source: join(productOut, 'pavement-sealcoat-hero.jpg'),
    title: 'Black Pavement Sealcoat',
    subtitle: 'Coal tar and asphalt emulsion',
    accent: '#1e40af',
  },
  'color-pavement-sealcoat': {
    source: join(productOut, 'color-sprayed-pavement-hero.jpg'),
    title: 'Color Pavement Sealcoat',
    subtitle: 'Anti-skid decorative coating',
    accent: '#dc2626',
  },
  'cold-mix-additive': {
    source: join(productOut, 'cold-mix-additive-hero.jpg'),
    title: 'Cold Mix Asphalt Additive',
    subtitle: '3rd generation concentrate',
    accent: '#f59e0b',
  },
  'asphalt-recycling-agent': {
    source: join(productOut, 'emulsified-asphalt-hero.jpg'),
    title: 'Asphalt Recycling Agent',
    subtitle: 'Rejuvenate aged pavement',
    accent: '#166534',
  },
  'warm-mix-additive': {
    source: join(productOut, 'emulsified-asphalt-hero.jpg'),
    title: 'Warm Mix Asphalt Additive',
    subtitle: 'Reduce production temperature',
    accent: '#1e40af',
  },
};

function escapeXml(value) {
  return value.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;');
}

function wrap(text, max) {
  const words = text.split(' ');
  const lines = [];
  let line = '';
  for (const word of words) {
    const next = line ? `${line} ${word}` : word;
    if (next.length > max && line) {
      lines.push(line);
      line = word;
    } else {
      line = next;
    }
  }
  if (line) lines.push(line);
  return lines.slice(0, 2);
}

function overlaySvg({ width, height, title, subtitle, accent, og = false }) {
  const panelHeight = Math.round(height * (og ? 0.36 : 0.4));
  const panelY = height - panelHeight;
  const pad = Math.round(width * 0.07);
  const titleSize = og ? 48 : 32;
  const subtitleSize = og ? 26 : 19;
  const brandSize = og ? 18 : 15;
  const lines = wrap(title, og ? 34 : 25);
  const titleY = panelY + Math.round(panelHeight * 0.48);
  const lineHeight = Math.round(titleSize * 1.14);
  const lineSvg = lines.map((line, index) => (
    `<text x="${pad}" y="${titleY + index * lineHeight}" class="title">${escapeXml(line)}</text>`
  )).join('');
  const subtitleY = titleY + lines.length * lineHeight + Math.round(height * 0.035);

  return Buffer.from(`
    <svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" xmlns="http://www.w3.org/2000/svg">
      <style>
        .brand { font-family: Arial, Helvetica, sans-serif; font-size: ${brandSize}px; font-weight: 700; letter-spacing: 1.4px; fill: #cbd5e1; }
        .title { font-family: Arial, Helvetica, sans-serif; font-size: ${titleSize}px; font-weight: 700; fill: #ffffff; }
        .subtitle { font-family: Arial, Helvetica, sans-serif; font-size: ${subtitleSize}px; font-weight: 400; fill: #e2e8f0; }
        .export { font-family: Arial, Helvetica, sans-serif; font-size: 17px; font-weight: 700; fill: #ffffff; }
      </style>
      <rect width="${width}" height="${height}" fill="rgba(15, 23, 42, 0.22)" />
      <rect x="0" y="${panelY}" width="${width}" height="${panelHeight}" fill="rgba(15, 23, 42, 0.88)" />
      <rect x="${pad}" y="${panelY + Math.round(panelHeight * 0.16)}" width="${Math.round(width * 0.15)}" height="${Math.max(5, Math.round(height * 0.012))}" rx="3" fill="${accent}" />
      <text x="${pad}" y="${panelY + Math.round(panelHeight * 0.32)}" class="brand">SHINING ROAD TECHNOLOGY</text>
      ${lineSvg}
      <text x="${pad}" y="${subtitleY}" class="subtitle">${escapeXml(subtitle)}</text>
      <rect x="${width - pad - 140}" y="${panelY + panelHeight - 66}" width="140" height="42" rx="21" fill="${accent}" />
      <text x="${width - pad - 112}" y="${panelY + panelHeight - 39}" class="export">EXPORT</text>
    </svg>
  `);
}

async function generate(slug, data, width, height, output, og = false) {
  const input = await readFile(data.source);
  await sharp(input)
    .resize(width, height, { fit: 'cover' })
    .modulate({ brightness: 0.78 })
    .composite([{ input: overlaySvg({ width, height, ...data, og }), top: 0, left: 0 }])
    .jpeg({ quality: 88, mozjpeg: true })
    .toFile(output);
  console.log(`${slug} ${width}x${height}`);
}

await mkdir(productOut, { recursive: true });
await mkdir(ogOut, { recursive: true });

for (const [slug, data] of Object.entries(products)) {
  await generate(slug, data, 800, 400, join(productOut, `${slug}-hero.jpg`));
  await generate(slug, data, 1200, 630, join(ogOut, `${slug}-og.jpg`), true);
}
