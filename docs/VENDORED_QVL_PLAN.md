# Vendored Virtual Dependency Plan

## Decision

Do not require every user to clone the full Quanser Academic Resources repository just to run this project.

Current implementation:

- Minimum virtual dependency code lives under `virtual_dependencies/quanser_qvl/`.
- A small `qvl/` compatibility package forwards imports to `virtual_dependencies/quanser_qvl/`.
- This keeps the existing virtual backend import style working while the real code is local to this repo.

## Current structure

```text
virtual_dependencies/
  __init__.py
  README.md
  quanser_qvl/
    __init__.py
    qlabs.py
    actor.py
    qbot_platform.py

qvl/
  __init__.py
  qlabs.py
  actor.py
  qbot_platform.py
```

## Still required externally

Vendoring this layer does not replace the Quanser SDK.

The QLabs communication layer still requires:

```text
quanser.communications
quanser.common
```

## Current scope

Included now:

- QLabs TCP connection and container send/receive basics.
- Actor spawn by explicit actor number.
- QBot Platform wheel command and state request.

Not included yet:

- QVL camera image helper.
- QVL LIDAR helper.
- QBot Platform flooring actor.
- Full QVL actor utilities.

## Test command

Run this first to verify imports:

```powershell
py -3.12 -m checks.virtual_dependency_check
```

Then run QLabs:

```powershell
py -3.12 -m checks.virtual_qlabs_check --connect-only
```

## License note

The QVL-style code is based on the public Quanser Academic Resources QVL files. License review must remain on the task list before external redistribution.
