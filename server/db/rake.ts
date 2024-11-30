import { rakeDb } from "orchid-orm/migrations"

import { BaseTable } from "./base"
import { migrations } from "./migrations"

const config = useRuntimeConfig()

export const { change, run } = rakeDb.lazy(
  { databaseURL: config.database.url },
  {
    baseTable: BaseTable,
    basePath: import.meta.url,
    migrations,
    migrationsTable: "rake_migration",
  },
)
