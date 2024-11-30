import type { Selectable } from "orchid-orm"

import { BaseTable } from "../base"

export class JobTable extends BaseTable {
  override readonly table = "job"

  override columns = this.setColumns(t => ({
    id: t.id(),
    job_type: t.job_type(),
    job_status: t.job_status(),
    args: t.text(),
  }))
}

export type Job = Selectable<JobTable>
