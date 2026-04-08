# blog-beast-pipeline

Automated daily workflow that processes raw work notes into a structured journal, syncs to Coda, pulls your task list, produces a morning briefing with task updates, and syncs everything back to Coda.

## What are BLOG and BEAST?

**BLOG** and **BEAST** are two tables I built in my Coda workspace ("Brady's Coda Playground") to manage my daily work:

- **BLOG** = **B**rady's **L**earnings, **O**bservations, and **G**rowth -- a daily journal. Each row is one day's entry with reviewed notes, a polished summary, executive bullets, wins, blockers, and a category tag. The idea is to turn raw messy notes into something a manager or stakeholder could actually read.

- **BEAST** = **B**rady's **E**xecution, **A**ction, and **S**trategy **T**asks -- a task list. Each row is a tracked task with status, priority, due date, project, effort, and dated notes. It functions as a personal project tracker that stays current through the pipeline.

This pipeline connects the two: your daily notes feed the BLOG, the BLOG drives updates to the BEAST, and everything syncs to Coda automatically. Before this existed, I was doing all of it by hand every morning -- writing up notes, updating tasks, copying things into Coda. Now it takes one command.

If you want to use this for your own work, you would create your own versions of these two tables in your own Coda doc. The setup guide walks you through it, and the discovery script auto-configures the column mappings so you don't have to hunt for Coda IDs.

## Quick Start

1. Copy `config.example.env` to `.env` and add your Coda API key and doc ID
2. Run `pip install -r requirements.txt`
3. Run `python scripts/discover_config.py` to auto-configure your Coda tables
4. Install the Claude Code plugin (see Setup below)
5. Type `run pipeline` in Claude Code and paste your daily notes

## Setup

Full installation guide: **[docs/SETUP.md](docs/SETUP.md)**

## Specification

Complete pipeline spec (processing rules, section formats, field standards): **[plugin/skills/run-pipeline/SKILL.md](plugin/skills/run-pipeline/SKILL.md)**
