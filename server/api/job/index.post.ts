import { db } from "~/server/db"

export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const { args } = body
  const job = await db.job.create({ job_type: "CREATE", job_status: "NEW", args })
  return { job }
})
