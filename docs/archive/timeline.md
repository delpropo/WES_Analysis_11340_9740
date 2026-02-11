# Original Project Timeline (Archived)

> **Note:** This timeline was created at project inception (April 2025) and is preserved for historical reference. It no longer reflects current project status. See the main [README.md](../../README.md) for current milestone status.

```mermaid
gantt
    title WES Data Analysis Timeline (Original Plan)
    dateFormat YYYY-MM-DD
    section WES
        DNA Submitted          :done,   wes1, 2025-04-07, 2d
        Sequencing             :done,   wes2, after wes1, 2025-06-17
        Data Transfer          :done,   wes_transfer, 2025-06-30, 2d
        QC and Documentation   :active, wes3, 2025-07-01, 7d
        Variant Calling        :done,   analysis1, after wes_transfer, 14d
        Post-Processing        :        analysis2, after analysis1, 14d
        Analysis               :        analysis3, after analysis2, 30d
    section Development
        Post-Processing Dev    :active, dev1, 2025-04-01, 100d
        Analysis Dev           :active, dev2, 2025-05-01, 120d
    section Vacation
        Vacation               :done,   vac1, 2025-06-12, 17d
```
