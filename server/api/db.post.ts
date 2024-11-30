import { run } from "~/server/db/rake"

export default defineEventHandler(async (event) => {
  const body = await readRawBody(event)
  const messages: string[] = []
  function log(message: string) {
    messages.push(message)
  }

  await run(body?.split(/\s+/) ?? [], {
    logger: { log, warn: log, error: log },
  })

  return messages.join("\n")
})
