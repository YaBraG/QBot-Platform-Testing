# Vendored QVL Plan

## Decision

We should not require every user to clone the full Quanser Academic Resources repository just to run this project.

Preferred direction:

- Vendor only the QVL pieces we need.
- Keep the vendored code isolated.
- Preserve the Quanser BSD 3-Clause license notice.
- Do not copy the entire Quanser repository.
- Do not mix vendored QVL code into our own `qbot` API.

## Why not copy everything?

Copying the entire QVL folder would work faster at first, but it adds a lot of code we do not need and makes debugging harder.

The QBot virtual layer mainly needs:

- QLabs connection/container code.
- Base actor spawn methods.
- QBot Platform actor methods.
- Optional QBot Platform flooring if we later build scenes.

## Important limitation

Vendoring QVL does not remove every Quanser dependency.

The QLabs communication layer still depends on Quanser's communications package. That means the first vendored version may still require Quanser runtime libraries installed on the machine.

## Target structure

```text
vendor/
  quanser_qvl/
    LICENSE.quanser
    __init__.py
    qlabs.py
    actor.py
    qbot_platform.py
    qbot_platform_flooring.py
```

## Import rule

Our backend should import from our vendored namespace first:

```python
from vendor.quanser_qvl.qlabs import QuanserInteractiveLabs
from vendor.quanser_qvl.qbot_platform import QLabsQBotPlatform
```

Fallback to external `qvl` can remain temporarily during transition.

## Implementation order

1. Add Quanser BSD 3-Clause license text under `vendor/quanser_qvl/LICENSE.quanser`.
2. Add the minimum QVL files.
3. Rename imports from `qvl.*` to `vendor.quanser_qvl.*` inside the vendored files.
4. Update `VirtualQLabsBackend` to prefer vendored QVL.
5. Keep a fallback import from external `qvl` until the vendored path is tested.
6. Run virtual check again.

## Longer-term cleanup

Later, if needed, replace the Quanser communications dependency with our own TCP client that speaks the same QLabs container protocol. Do not do this until the vendored QVL path works.
