import { defineCollection, z } from 'astro:content';

const products = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    category: z.string(),
    description: z.string(),
    image: z.string().optional(),
    gallery: z.array(z.string()).optional(),
    features: z.array(z.string()).optional(),
    specifications: z.array(z.object({
      label: z.string(),
      value: z.string(),
    })).optional(),
    order: z.number().default(0),
    draft: z.boolean().default(false),
  }),
});

const news = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.date(),
    description: z.string(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),
  }),
});

export const collections = { products, news };
