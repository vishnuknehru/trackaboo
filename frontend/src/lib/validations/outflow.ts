import { z } from 'zod'

export const createOutflowSchema = z.object({
  amount: z.number().gt(0),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  categoryId: z.number().int().positive(),
  description: z.string().max(1000).optional().nullable(),
})

export const updateOutflowSchema = createOutflowSchema.partial()

export type CreateOutflowInput = z.infer<typeof createOutflowSchema>
export type UpdateOutflowInput = z.infer<typeof updateOutflowSchema>
