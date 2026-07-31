#!/usr/bin/env python3

import sys
import os
import json
from datetime import datetime

DATA_DIR = os.path.expanduser("~/.fastnode")
DATA_FILE = os.path.join(DATA_DIR, "data.json")


def load_notes():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_notes(notes):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)
    os.chmod(DATA_FILE, 0o600)


def parse_text_and_tags(args):
    text_parts = []
    tags = []
    for arg in args:
        if arg.startswith("#"):
            tags.append(arg)
        else:
            text_parts.append(arg)
    text = " ".join(text_parts)
    return text, tags


def cmd_wfnode():
    text, tags = parse_text_and_tags(sys.argv[1:])
    if not text and not tags:
        print("Использование: wfnode <текст> [теги через #]")
        print("Пример: wfnode Сделать задачу \\#today \\#123")
        sys.exit(1)
    notes = load_notes()
    next_id = max([n["id"] for n in notes], default=0) + 1
    note = {
        "id": next_id,
        "text": text,
        "tags": tags,
        "created": datetime.now().isoformat(),
    }
    notes.append(note)
    save_notes(notes)


def cmd_fnode():
    filter_tags = [t for t in sys.argv[1:] if t.startswith("#")]
    notes = load_notes()
    if filter_tags:
        notes = [n for n in notes if all(tag in n["tags"] for tag in filter_tags)]
    if not notes:
        print("Заметок не найдено.")
        return
    for n in notes:
        print(f"[{n['id']}] {n['text']}")


def cmd_dfnode():
    if len(sys.argv) < 2:
        print("Использование: dfnode <id>")
        sys.exit(1)
    try:
        target_id = int(sys.argv[1])
    except ValueError:
        print(f"ID должен быть числом, получено: {sys.argv[1]}")
        sys.exit(1)
    notes = load_notes()
    original_count = len(notes)
    notes = [n for n in notes if n["id"] != target_id]
    if len(notes) == original_count:
        print(f"Заметка с id {target_id} не найдена.")
        sys.exit(1)
    save_notes(notes)


def main():
    me = os.path.basename(sys.argv[0])

    if me == "wfnode":
        cmd_wfnode()
    elif me == "fnode":
        cmd_fnode()
    elif me == "dfnode":
        cmd_dfnode()
    else:
        print("Использование:")
        print("  wfnode <текст> [теги...]    — добавить заметку")
        print("  fnode [теги...]                  — найти заметки")
        print("  fnode                              — все заметки")
        print("  dfnode <id>                          — удалить заметку по ID")
        sys.exit(1)


if __name__ == "__main__":
    main()