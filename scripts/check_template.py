"""Offline sanity check for office-hours.template.yaml.

Switch Console runs its own validator when you paste a template in, and that is
the real authority. This script repeats the checks that matter for this
template, so a typo shows up before you open Console. Each rule comes from
docs/TEMPLATES.md and core/switch_core/rooms_yaml.py in the Switch repo.

Usage:  python scripts/check_template.py [path]   (needs PyYAML)
Exits 1 and lists every problem if anything is wrong.
"""

import re
import sys

import yaml

PLACEHOLDER = re.compile(r"\{(\$?[A-Za-z_][A-Za-z0-9_]*)\}")  # same regex as Switch
BUILTINS = {"$creator", "$creator_email", "$date", "$timestamp", "$agents_dir", "agent"}
TOP_LEVEL = {"version", "params", "agent", "agents", "room", "group", "rooms", "links", "kickoff", "form"}
PARAM_KEYS = {"type", "description", "label", "default", "required", "input", "enum",
              "multiline", "pattern", "min", "max"}
PARAM_TYPES = {"string", "number", "boolean", "enum", "agent", "bridge", "room", "user",
               "provider", "location", "machine", "directory"}
AGENT_KEYS = {"name", "display_name", "icon_url", "description", "instructions", "provider",
              "machine", "location", "directory", "model", "advanced_config", "isolation",
              "auto_mode", "auto_approve", "can_manage_agents", "connections", "repo",
              "sources", "addressing", "join", "allow_existing"}
ROOM_KEYS = {"name", "description", "instructions", "bridge", "channel_type", "read_visibility",
             "write_visibility", "agents", "users", "roles", "references", "packages", "docs",
             "aliases", "kickoff"}
ADDRESSING = {"owner", "owner-agents", "anyone"}
AGENT_NAME = re.compile(r"^[a-z0-9][a-z0-9._-]*$")


def strings(node):
    """Every string in the document, keys included (Switch fills both)."""
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for k, v in node.items():
            yield from strings(k)
            yield from strings(v)
    elif isinstance(node, list):
        for item in node:
            yield from strings(item)


def fill(text, values):
    """Substitute {param} with its default, the way Switch would."""
    return PLACEHOLDER.sub(lambda m: str(values.get(m.group(1), m.group(0))), text)


def check(doc):
    problems = []
    params = doc.get("params", {})
    defaults = {k: (v.get("default")[0] if isinstance(v.get("default"), list) else v.get("default"))
                for k, v in params.items()}

    for key in doc:
        if key not in TOP_LEVEL:
            problems.append(f"unknown top-level key: {key}")
    if "group" in doc and "kickoff" in doc:
        problems.append("a group document puts kickoff inside each room, not at the top")

    for name, spec in params.items():
        for key in spec:
            if key not in PARAM_KEYS:
                problems.append(f"param {name}: unknown field {key}")
        if spec.get("type", "string") not in PARAM_TYPES:
            problems.append(f"param {name}: unknown type {spec.get('type')}")

    used = {m for s in strings(doc) for m in PLACEHOLDER.findall(s)}
    for p in sorted(used - set(params) - BUILTINS):
        problems.append(f"placeholder {{{p}}} is not a declared param or builtin")
    for p in sorted(set(params) - used):
        problems.append(f"param {p} is declared but never used")

    agent_names = []
    for i, agent in enumerate(doc.get("agents", [])):
        label = agent.get("name", f"agent {i + 1}")
        for key in agent:
            if key not in AGENT_KEYS:
                problems.append(f"{label}: unknown field {key}")
        for need in ("provider", "directory", "instructions"):
            if need not in agent:
                problems.append(f"{label}: missing {need}")
        if "location" not in agent and "machine" not in agent:
            problems.append(f"{label}: missing location or machine")
        if agent.get("addressing", "owner") not in ADDRESSING:
            problems.append(f"{label}: addressing must be one of {sorted(ADDRESSING)}")
        name = fill(agent.get("name", ""), defaults)
        if not AGENT_NAME.match(name):
            problems.append(f"{label}: name {name!r} is not a valid agent name")
        agent_names.append(name)

    rooms = doc.get("rooms", [doc["room"]] if "room" in doc else [])
    room_names = []
    for room in rooms:
        rname = fill(room.get("name", "?"), defaults)
        room_names.append(rname)
        for key in room:
            if key not in ROOM_KEYS:
                problems.append(f"room {rname}: unknown field {key}")
        for need in ("name", "description"):
            if need not in room:
                problems.append(f"room {rname}: missing {need}")
        members = [fill(a, defaults) for a in room.get("agents", [])]
        for a in members:
            if a not in agent_names:
                problems.append(f"room {rname}: agent {a} is not created by this template")
        for a in (room.get("aliases") or {}):
            if fill(a, defaults) not in members:
                problems.append(f"room {rname}: alias for {fill(a, defaults)}, who is not in the room")
        kickoff = fill(room.get("kickoff", ""), defaults)
        for mention in re.findall(r"@([a-z0-9][a-z0-9._-]*)", kickoff):
            if mention.endswith("."):
                problems.append(f"room {rname}: kickoff mention @{mention} ends in a period")

    for link in doc.get("links", []):
        for end in ("from", "to"):
            if fill(link.get(end, ""), defaults) not in room_names:
                problems.append(f"link {end} {link.get(end)} is not a room in this template")

    return problems, agent_names, room_names


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "office-hours.template.yaml"
    with open(path) as f:
        doc = yaml.safe_load(f)
    problems, agents, rooms = check(doc)
    print(f"agents: {', '.join(agents)}")
    print(f"rooms:  {', '.join(rooms)}")
    if problems:
        print("\nProblems:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print("\nOK: no problems found.")


if __name__ == "__main__":
    main()
