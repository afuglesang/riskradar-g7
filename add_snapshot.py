#!/usr/bin/env python3
"""Publish one snapshot to the static site.

Usage: python3 tools/add_snapshot.py <snapshot.json>

- Removes every private field named "flocean" (at any depth, including the
  top level) and any "h30" recalibration overlay.
- Refuses to publish if the word "flocean" still appears anywhere in the text.
- Writes data/snapshots/<date>.json and adds the date to data/manifest.json.
"""
import json, os, re, sys

PRIVATE_KEYS = {"flocean", "h30"}

def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if k.lower() not in PRIVATE_KEYS}
    if isinstance(o, list):
        return [strip(x) for x in o]
    return o

def main(path):
    with open(path, encoding="utf-8") as fh:
        snap = json.load(fh)
    date = str(snap.get("date") or snap.get("id") or "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
        sys.exit("error: snapshot has no valid 'date' (YYYY-MM-DD)")
    if not isinstance(snap.get("factors"), list) or not snap["factors"]:
        sys.exit("error: snapshot has no factors")
    clean = strip(snap)
    text = json.dumps(clean, ensure_ascii=False)
    if "flocean" in text.lower():
        hits = [m.start() for m in re.finditer("flocean", text.lower())][:5]
        ctx = [text[max(0, i - 60): i + 60] for i in hits]
        sys.exit("error: the word 'Flocean' still appears in public text; remove it and retry:\n" + "\n".join(ctx))
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    snapdir = os.path.join(root, "data", "snapshots")
    os.makedirs(snapdir, exist_ok=True)
    with open(os.path.join(snapdir, date + ".json"), "w", encoding="utf-8") as fh:
        json.dump(clean, fh, ensure_ascii=False, separators=(",", ":"))
    mpath = os.path.join(root, "data", "manifest.json")
    try:
        with open(mpath, encoding="utf-8") as fh:
            manifest = json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError):
        manifest = {}
    dates = set(manifest.get("snapshots", []))
    dates.add(date)
    manifest["snapshots"] = sorted(dates)
    manifest["updated"] = snap.get("generatedAt") or date
    with open(mpath, "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=1)
    print(f"published {date}: data/snapshots/{date}.json; manifest has {len(dates)} snapshot(s)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
