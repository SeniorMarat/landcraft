import { orchidORM } from "orchid-orm"

import * as tables from "./tables"

const config = useRuntimeConfig()

export const db = orchidORM(
  { databaseURL: config.database.url, log: config.database.log },
  {
    job: tables.JobTable,
  },
)
