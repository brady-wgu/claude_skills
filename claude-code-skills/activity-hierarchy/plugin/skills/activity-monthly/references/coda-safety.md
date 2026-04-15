# Coda Safety Protocol

These 5 constraints are **absolute and non-negotiable**. They apply to every Coda operation in every skill, every session, without exception. The Coda MCP Connector Beta operates in **Global Admin mode** with full administrative authority across Brady's entire Coda workspace. There is no permission guardrail on the Coda side. An accidental write to the wrong doc, table, or row has **real professional consequences** (cause for termination). Every MCP write call is treated as **irreversible and career-impacting** because it is.

---

## Constraint 1: Hard-Code ALL Write Targets with Read-First Verification

Every write operation targets a specific, pre-identified table URI. Before any write to any table in any session, the skill MUST first call `table_rows_read` on that table to confirm its URI and schema match expectations. Never write to a table URI from memory or assumption alone within a single session. The pattern is: **discover, verify, then hard-code**.

**Authorized write targets (hard-coded):**
- Daily Log: `coda://docs/dHXfr0V468/tables/grid-ty2WGfh4qa`
- BEAST (Complete To Do List): `coda://docs/dHXfr0V468/tables/grid-M-DmPD4U5x`

**Daily Log column IDs (verified 14 APR 2026):**

| Column Name | Column ID | Type |
|---|---|---|
| Date | c-oiaBDBstH1 | date |
| Reviewed Notes | c-DXM4h2B28G | canvas |
| Polished Summary | c-FIWz6AEhwd | text |
| Executive Bullets | c-WSCAvrHbnz | text |
| Key Wins | c-QuKWx0lwGp | text |
| Blockers | c-bT-C79ocGH | text |
| Category | c-CA6Nwa3A2N | select |
| Entry Type | c-7IZ-UJNjXG | select |
| Status | c-pR0VmtQ5AV | select |

**BEAST column IDs (verified 14 APR 2026):**

| Column Name | Column ID | Type | Writable |
|---|---|---|---|
| Task ID | c-ImEDreEoEA | text | Yes |
| Name | c-MBRsPfbd6d | text | Yes |
| Status | c-zH_C1i-smP | select | Yes |
| Priority | c-g-kRN3Y2aS | select | Yes |
| Due Date | c-NP39SR6C8D | date | Yes |
| Type | c-Z_PWA6_-Bb | select | Yes |
| Project | c-W3gb8_ca2O | select | Yes |
| Effort | c-RdNqDL9akn | select | Yes |
| Notes | c-ioDsMHggmZ | text | Yes |
| Link | c-wuGVeM0y7z | link | Yes |
| Parent | c-ONPz07rw_J | lookup | **NEVER WRITE** (manual assignment) |
| Subitems | c-RRrt1LG5D9 | lookup | **NEVER WRITE** (calculated display) |

---

## Constraint 2: Zero Deletion Capability

NEVER call `delete_element`, `delete_element_by_text`, or any other destructive MCP operation on any table, row, page, or element in Coda. Period. No exceptions. No workarounds.

If a deletion would be beneficial, describe the exact location:
- Document name and URL
- Table name and URI
- Row number, row ID, or identifying field values
- What should be removed and why

Brady performs the deletion manually with his mouse.

---

## Constraint 3: Single-Doc Write Scope

Writes are permitted in **Brady's Coda Playground** and nowhere else:
- Doc ID: `dHXfr0V468`
- URL: `https://coda.io/d/Bradys-Coda-Playground_ddHXfr0V468/`

If a workflow would benefit from modifying another doc, present:
1. Doc name and URL
2. Specific table or page to modify
3. What the modification would be
4. Justification for why it is necessary

Only Brady's explicit instruction in the conversation constitutes permission to expand access.

---

## Constraint 4: All Other Coda Docs Are Read-Only

If a skill needs to reference data from another doc, it reads it. It does not write to, modify, or create rows/pages in any doc other than `dHXfr0V468`.

---

## Constraint 5: Global Admin Mode Awareness

The Coda MCP Connector Beta has NO permission settings to restrict accidental access. It operates in Global Admin mode with full administrative authority across Brady's entire Coda workspace. There is no safety net on the Coda side.

This means:
- Every `table_rows_manage` call executes immediately with full authority
- A wrong URI could write to any table in any doc Brady has access to
- There is no undo, no rollback, no approval flow on the Coda side
- The behavioral protocol defined here IS the safety net

---

## 7-Step Write Safety Protocol

This protocol is **mandatory before every `table_rows_manage` call**. No exceptions.

```
1. READ: Call table_rows_read on the target table to verify its URI and schema
2. VERIFY: Confirm the table name, column count, and column IDs match the
   hard-coded values in this document
3. BUILD: Construct the write payload using ONLY the columns specified in
   the skill's column mapping section
4. PRESENT: Display the complete payload to Brady for review
   - Show every field name and its value
   - Show the target table URI
   - Show whether this is an "add" (new row) or "update" (existing row)
5. WAIT: Do not proceed until Brady explicitly confirms
   - Acceptable confirmations: "yes", "confirmed", "write it", "go ahead"
   - If Brady says anything else, pause and clarify
6. WRITE: Only after confirmation, call table_rows_manage with the confirmed payload
7. VERIFY: Read the newly created or updated row back from Coda to confirm
   the write succeeded and all field values are correct
```

If ANY step fails or produces unexpected results, **HALT immediately** and report the discrepancy to Brady. Do not attempt to recover, retry, or work around the issue.

---

## Section 7 Prohibition

BLOG Section 7 (Sensitive Items) is **NEVER written to Coda** under any circumstances. It is displayed in the terminal or chat output only. If Section 7 content appears in any write payload, halt and remove it before proceeding. This is a privacy and professional safety requirement, not a formatting preference.
