import { z } from 'zod'

export const createCategorySchema = z.object({
  name: z.string().min(1).max(100),
  type: z.enum(['outflow', 'inflow', 'any']).default('outflow'),
  color: z
    .string()
    .regex(/^#[0-9a-fA-F]{6}$/)
    .optional()
    .nullable(),
  description: z.string().max(500).optional().nullable(),
})

export const updateCategorySchema = createCategorySchema.partial()

export type CreateCategoryInput = z.infer<typeof createCategorySchema>
export type UpdateCategoryInput = z.infer<typeof updateCategorySchema>
