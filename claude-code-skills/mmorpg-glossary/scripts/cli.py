"""
cli.py
------
Thin CLI layer for the MMORPG glossary tool.
All output is JSON so Claude Code can parse it reliably.

Usage:
    python scripts/cli.py discover [--verbose]
    python scripts/cli.py list [--verbose]
    python scripts/cli.py search <query> [--verbose]
    python scripts/cli.py add --term T [--full-name N] [--definition D] [--source S] [--force] [--dry-run] [--verbose]
    python scripts/cli.py edit --term T [--field F --value V | --row-id R --field F --value V] [--dry-run] [--verbose]
    python scripts/cli.py delete --term T [--row-id R] [--dry-run] [--verbose]
    python scripts/cli.py dump [--verbose]
"""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.glossary_service import GlossaryService


def out(data):
    print(json.dumps(data, indent=2, ensure_ascii=False))


def cmd_discover(args):
    svc = GlossaryService(verbose=args.verbose)
    out(svc.discover())


def cmd_list(args):
    svc = GlossaryService(verbose=args.verbose)
    entries = svc.fetch_all()
    out({"count": len(entries), "entries": entries})


def cmd_search(args):
    svc = GlossaryService(verbose=args.verbose)
    results = svc.search(args.query)
    out({"query": args.query, "count": len(results), "results": results})


def cmd_add(args):
    svc = GlossaryService(verbose=args.verbose)

    if args.dry_run:
        out({
            "dry_run": True,
            "action": "add",
            "term": args.term,
            "full_name": args.full_name or "",
            "definition": args.definition or "",
            "source": args.source or "",
        })
        return

    if args.force:
        result = svc.add_term_force(
            args.term,
            full_name=args.full_name or "",
            definition=args.definition or "",
            source=args.source or "",
        )
    else:
        result = svc.add_term(
            args.term,
            full_name=args.full_name or "",
            definition=args.definition or "",
            source=args.source or "",
        )
    out(result)


def cmd_edit(args):
    svc = GlossaryService(verbose=args.verbose)

    updates = {}
    if args.full_name is not None:
        updates["full_name"] = args.full_name
    if args.definition is not None:
        updates["definition"] = args.definition
    if args.source is not None:
        updates["source"] = args.source
    if args.new_term is not None:
        updates["term"] = args.new_term

    if not updates:
        out({"status": "error", "message": "No fields to update. Use --full-name, --definition, --source, or --new-term."})
        return

    if args.dry_run:
        out({"dry_run": True, "action": "edit", "term": args.term, "row_id": args.row_id, "updates": updates})
        return

    if args.row_id:
        result = svc.edit_term_by_row_id(args.row_id, updates)
    else:
        result = svc.edit_term(args.term, updates)
    out(result)


def cmd_delete(args):
    svc = GlossaryService(verbose=args.verbose)

    if args.dry_run:
        out({"dry_run": True, "action": "delete", "term": args.term, "row_id": args.row_id})
        return

    if args.row_id:
        result = svc.delete_term_by_row_id(args.row_id)
    else:
        result = svc.delete_term(args.term)
    out(result)


def cmd_dump(args):
    svc = GlossaryService(verbose=args.verbose)
    entries = svc.dump()
    out({"count": len(entries), "glossary": entries})


def build_parser():
    parser = argparse.ArgumentParser(description="MMORPG Glossary Tool")
    parser.add_argument("--verbose", action="store_true", help="Verbose API logging")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("discover", help="Show table and column IDs")

    sub.add_parser("list", help="List all glossary terms")

    p_search = sub.add_parser("search", help="Search glossary")
    p_search.add_argument("query", help="Search string")

    p_add = sub.add_parser("add", help="Add a new term")
    p_add.add_argument("--term", required=True, help="Term abbreviation or name")
    p_add.add_argument("--full-name", help="Expanded name")
    p_add.add_argument("--definition", help="Definition text")
    p_add.add_argument("--source", help="Source attribution")
    p_add.add_argument("--force", action="store_true", help="Add even if duplicate exists")
    p_add.add_argument("--dry-run", action="store_true", help="Show payload without writing")

    p_edit = sub.add_parser("edit", help="Edit an existing term")
    p_edit.add_argument("--term", required=True, help="Term to edit (lookup key)")
    p_edit.add_argument("--row-id", help="Specific row ID for ambiguous terms")
    p_edit.add_argument("--new-term", help="Rename the term")
    p_edit.add_argument("--full-name", help="New full name")
    p_edit.add_argument("--definition", help="New definition")
    p_edit.add_argument("--source", help="New source")
    p_edit.add_argument("--dry-run", action="store_true", help="Show payload without writing")

    p_del = sub.add_parser("delete", help="Delete a term")
    p_del.add_argument("--term", required=True, help="Term to delete")
    p_del.add_argument("--row-id", help="Specific row ID for ambiguous terms")
    p_del.add_argument("--dry-run", action="store_true", help="Show payload without deleting")

    sub.add_parser("dump", help="Dump full glossary as JSON")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "discover": cmd_discover,
        "list": cmd_list,
        "search": cmd_search,
        "add": cmd_add,
        "edit": cmd_edit,
        "delete": cmd_delete,
        "dump": cmd_dump,
    }

    handler = dispatch.get(args.command)
    if handler:
        handler(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
