# blog-beast-pipeline

Automated daily workflow that processes raw work notes into a structured journal (BLOG), syncs to Coda, pulls your task list, produces a morning briefing (BEAST), and syncs task updates back to Coda.

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
