# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

Personal workspace for experimenting with Claude Code skills and building small Python desktop tools.

## Pomodoro timer (`pomodoro.py`)

Python 3 desktop app using tkinter. No external dependencies beyond Python stdlib.

```bash
python pomodoro.py
```

Four-mode cycle tracked by 4 dot indicators:

| Mode | Duration | Purpose |
|---|---|---|
| FOCUS | 25 min | Deep work |
| STRETCH | 3 min | Stand up, move (after F1, F3) |
| REVIEW | 5 min | Mid-cycle progress check (after F2) |
| LONG BREAK | 15 min | Full rest (after F4), dots reset |

Timeout constants and colors are at the top of the file. `RoundedButton` is a custom Canvas widget.

## Installed skills

- **Matt Pocock skills** (29 skills, `.agents/skills/`) — engineering + productivity slash commands (`/diagnose`, `/grill-me`, `/tdd`, etc.)
- **andrej-karpathy-skills** (Claude Code plugin, user scope) — behavioral guidelines in CLAUDE.md format

## Python

Python 3.14 at `D:\Python\`. Shell uses bash (Git Bash), not PowerShell. Paths use forward slashes.
