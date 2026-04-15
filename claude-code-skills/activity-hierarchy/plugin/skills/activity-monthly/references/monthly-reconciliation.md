# Monthly OneNote Export Reconciliation

**Schedule:** First business day of each month (run alongside any Monthly Digest or
quarterly review scripts you maintain).

**Purpose:** Ensure no gaps exist between daily entries logged in your workspace and
notes captured in OneNote. Archive the full export as a reference layer.

---

## Step 1: Export OneNote (Manual)

1. Open OneNote on the web or desktop app.
2. Select the notebook containing your daily notes.
3. Click **File** → **Export** → **PDF**.
4. Name the file using this convention:
   `OneNote_Export_THROUGH_[DD_MMM_YYYY].pdf`
   Example: `OneNote_Export_THROUGH_31_MAR_2026.pdf`
   Note: The date in the filename reflects "through yesterday," not today.
5. Save to your local drive (OneDrive or Downloads).
6. Upload the PDF to your Claude Project as a new document reference.

---

## Step 2: Archive the Previous Export

1. Move the previous month's export to a folder labeled `_Archive/OneNote_Exports/`.
2. Keep it accessible but separate from the active working file.

---

## Step 3: Run Archive Reconciliation

Use the following prompt after uploading your export:

---

```
I am reconciling my OneNote export with my existing daily workspace log for the
period [START_DATE] through [END_DATE].

Here is my current OneNote export (attached): [filename]

Here is my existing archive of processed daily entries: [describe or list]

TASK: Identify any gaps or missing context.

For each day in the OneNote export:
1. Check if a corresponding workspace entry exists.
2. If the OneNote entry is MORE DETAILED than the workspace entry, note the
   additional context.
3. If the OneNote entry is DIFFERENT from the workspace entry (different emphasis,
   omitted details), flag it.
4. If the OneNote entry is COMPLETELY NEW (no workspace counterpart), flag it for
   immediate processing.

Output format:

**Days with Full Match (no action required):**
- Day 01: Workspace entry and OneNote align.

**Days with Additional OneNote Detail (review recommended):**
- Day 05: OneNote includes sensitive item about stakeholder conflict that was
  softened in the workspace entry. Recommend reviewing Section 7 (Sensitive Items).

**Days Completely Missing from Workspace (ACTION REQUIRED):**
- Day 14-23: These appear only in the OneNote export. Process immediately through
  the BLOG script.

**Duplicate or Contradictory Content (REVIEW):**
- [Any sections where OneNote and workspace entry tell different stories]

After the analysis, provide a short summary:
- Total days reviewed: X
- Days fully aligned: X
- Days requiring review: X
- Days requiring immediate processing: X
```

---

## Step 4: Process Flagged Days

**If new days are identified:**
1. Extract the raw notes for each day from the OneNote export.
2. Feed each day through the BLOG script (paste or upload the notes and ask Claude
   to process them).
3. Copy the seven-section output into your workspace under the appropriate date entry.
4. Mark in your archive: "Processed [DD MMM YYYY]".

**If additional context is identified for already-processed days:**
1. Review the sensitive items flagged in Section 7.
2. Update your private sensitive items tracker if new material emerges.
3. Do NOT retroactively change published workspace entries unless the content is
   factually incorrect.

---

## Step 5: Update Your Archive Index

Maintain a simple index in your workspace or a text file:

```
# BLOG Archive Index

## Month: [MONTH YEAR]
- Export file: OneNote_Export_THROUGH_[DD_MMM_YYYY].pdf
- Date range: [START] through [END]
- Total days: X
- Days processed: X
- Days reviewed for gaps: X
- Discrepancies found: X
- New days identified: X
- Archive location: OneDrive / _Archive/OneNote_Exports/
```

---

## Technical Note: OneNote Export Format

The export may arrive as:
- A standard PDF — use normal PDF reading tools.
- A ZIP archive disguised as a PDF containing numbered `.txt` files — attempt ZIP
  extraction first; fall back to PDF text extraction. The highest-numbered file
  typically contains the most recent content.

---

## Filename Convention Reminder

Always name daily text file archives as: `Day_[XX]_-_[DD_MMM].txt`
Example: `Day_01_-_23_FEB.txt`

This ensures consistent sorting and lookup across years.
