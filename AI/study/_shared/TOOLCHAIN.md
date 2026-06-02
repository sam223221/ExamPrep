# Toolchain Setup — Study Package Build

This document tells future agents (and future-you) the exact environment
needed to run any agent that touches the study package.

## Python interpreter

Use `py -3.12` exclusively. The system default Python on this machine is 3.14,
which has no pre-built wheels for the pinned dependencies.

Interpreter path:
`C:\Users\samgl\AppData\Local\Programs\Python\Python312\python.exe`

## Pinned dependencies

See `study/requirements.txt`. Install with:

    py -3.12 -m pip install -r study/requirements.txt

## WeasyPrint native runtime (GTK3)

WeasyPrint 62.3 needs the GTK3 native DLLs at runtime. They are installed
via MSYS2 at `C:\msys64\mingw64\bin`.

Before importing `weasyprint` in any Python script or agent task, EITHER:

1. **Preferred — in code, before `import weasyprint`:**

   ```python
   import os
   _gtk = r"C:\msys64\mingw64\bin"
   if _gtk not in os.environ.get("PATH", ""):
       os.environ["PATH"] = _gtk + os.pathsep + os.environ["PATH"]
   import weasyprint
   ```

2. **Or — in the calling shell:**

   ```powershell
   $env:PATH = 'C:\msys64\mingw64\bin;' + $env:PATH
   py -3.12 your_script.py
   ```

The persistent env var `WEASYPRINT_DLL_DIRECTORIES` is also set to
`C:\msys64\mingw64\bin` for forward-compatibility with newer WeasyPrint
versions, but WeasyPrint 62.3 itself only honours PATH.

## Verification

A passing smoke test is recorded in plan Task 0.1: WeasyPrint successfully
renders a tiny HTML string to a PDF on this host (smoke.pdf, 6871 bytes).
Smoke artefacts were deleted after verification.
