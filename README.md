# CForces

```txt
┌──────────────────────────────────────────────┐
│      ____________                            │
│     / ____/ ____/___  _____________  _____   │
│    / /   / /_  / __ \/ ___/ ___/ _ \/ ___/   │
│   / /___/ __/ / /_/ / /  / /__/  __(__  )    │
│   \____/_/    \____/_/   \___/\___/____/     │
│                                              │
└──────────────────────────────────────────────┘
```

A custom terminal simulator with python.

## Requirements

- `pip install -r requirements.txt`

## Notes

- This directory should be included under PYTHONPATH, and invoked by
  `python -m cforces`. On Windows, create a batch file called `cforces.bat` and
  add
  ```batch
  @echo off
  python -m cforces
  ```
- If you're using Avast Antivirus, add `*\a.exe` as an exception, so Avast won't
  scan it.

## To-do

- [ ] Wrap all paths with `pathlib.Path()`.