# Virtual Dependencies

This folder contains the minimum QLabs style code needed by this project for virtual QBot Platform testing.

## Purpose

The original Quanser Academic Resources repository provides a large Python package for virtual labs. This project only needs a small part of it for QBot virtual movement, so the small dependency layer lives here.

## Included

```text
virtual_dependencies/
  quanser_qvl/
    qlabs.py
    actor.py
    qbot_platform.py
```

## Still required externally

This folder does not replace the Quanser SDK. QLabs communication still requires:

```text
quanser.communications
quanser.common
```

## License

See `LICENSE_QUANSER_BSD3.txt`.
