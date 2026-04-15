# Activity Hierarchy

Automated five-level activity management system. Each level reads from the level below, synthesizes, performs integrity audits against the BEAST task list, and writes a structured entry to the Coda Daily Log table.

## Skills

| Skill | Trigger | What It Does |
|---|---|---|
| `/activity-daily` | "run daily", "run pipeline", "process my notes", "morning briefing", "run BLOG and BEAST" | Processes raw OneNote notes through 7-section BLOG + 4-section BEAST, writes to Coda |
| `/activity-weekly` | "run weekly", "weekly summary", "weekly digest" | Reads Daily entries for prior week, synthesizes, integrity checks, writes Weekly entry |
| `/activity-monthly` | "run monthly", "monthly digest", "monthly summary" | Reads Daily + Weekly for prior month, synthesizes, blocker lifecycle, writes Monthly Digest |
| `/activity-quarterly` | "run quarterly", "quarterly review" | Reads 3 Monthly Digests, synthesizes strategic narrative, writes Quarterly Review |
| `/activity-annual` | "run annual", "annual review", "year in review" | Reads 4 Quarterly Reviews, generates career narrative, writes Annual Review |

## Cascade Chain

```
Raw Notes --> /activity-daily --> Daily entries
                                      |
                        /activity-weekly --> Weekly entries
                                                |
                              /activity-monthly --> Monthly Digests
                                                        |
                                    /activity-quarterly --> Quarterly Reviews
                                                                |
                                          /activity-annual --> Annual Reviews
```

## Coda Target

- **Doc:** Brady's Coda Playground (dHXfr0V468)
- **Daily Log table:** `coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa`
- **BEAST table:** `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`

## Safety Protocol

Every skill follows the 5 non-negotiable Coda safety constraints and the 7-step Write Safety Protocol defined in each skill's `references/coda-safety.md`. In summary:

1. Hard-code all write targets with read-first verification
2. Zero deletion capability (describe deletions for manual execution)
3. Single-doc write scope (dHXfr0V468 only)
4. All other Coda docs are read-only
5. Global Admin mode awareness (every write is irreversible and career-impacting)

No write operation executes without explicit user confirmation. No exceptions.

## Full Specification

Each skill's complete specification lives in its own `SKILL.md` with supporting reference files in `references/`. The skill is the single source of truth for its processing logic.
