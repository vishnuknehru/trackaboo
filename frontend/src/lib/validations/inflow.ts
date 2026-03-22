import { z } from 'zod'

export const createInflowSchema = z.object({
  amount: z.number().gt(0),
  date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/),
  source: z.string().min(1).max(255),
  description: z.string().max(1000).optional().nullable(),
  categoryId: z.number().int().positive().optional().nullable(),
})

export const updateInflowSchema = createInflowSchema.partial()

export type CreateInflowInput = z.infer<typeof createInflowSchema>
export type UpdateInflowInput = z.infer<typeof updateInflowSchema>
