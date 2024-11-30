import { change } from "../rake"

export default change(async (db) => {
  await db.createEnum("job_type", ["CREATE", "EDIT"])
  await db.createEnum("job_status", ["NEW", "DONE"])

  await db.createTable("job", t => ({
    id: t.id(),
    job_type: t.enum("job_type"),
    job_status: t.enum("job_status"),
    args: t.text(),
  }))
})
