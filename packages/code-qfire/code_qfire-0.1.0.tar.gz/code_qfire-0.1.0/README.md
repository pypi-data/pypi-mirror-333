# CODE-QFIRE
CODE-QFIRE is a lightweight tool that scans code for inefficiencies and suggests optimizations.

## Features:
- Detects nested loops (O(n²) inefficiency)
- Finds unused variables
- Identifies slow SQL queries (`SELECT * FROM` without indexing)

## Usage:
```bash
code-qfire scan my_script.py
