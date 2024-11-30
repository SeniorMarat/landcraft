import { createBaseTable } from "orchid-orm"
import { uuidv7 } from "uuidv7"

export const BaseTable = createBaseTable({
  columnTypes: t => ({
    ...t,
    id: () => t.uuid().default(uuidv7).primaryKey(),
    job_type: () => t.enum("job_type", ["CREATE", "EDIT"]),
    job_status: () => t.enum("job_status", ["NEW", "DONE"]),
  }),
  snakeCase: true,
})

export const { sql } = BaseTable
