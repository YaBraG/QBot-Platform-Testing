# QBot Platform Testing

Pure Python project for testing and building a clean API around the Quanser QBot Platform.

## Project rules

- Pure Python only.
- No ROS for now.
- Core structure lives on `main`.
- Experimental tests live on test branches.
- Quanser dependencies should be hidden behind wrappers or backend files.
- The final user code should use our own API, not raw Quanser classes.

## Current structure

```text
qbot/
  environment.py
  constants.py
  state.py
  kinematics.py
  limits.py
  mover.py

backends/
  base_backend.py
  mock_backend.py
  virtual_qlabs_backend.py
  physical_qbot_backend.py

sensors/
  quanser_csi.py
  quanser_lidar.py
  realsense_direct.py
  opencv_camera.py

checks/
  kinematics_check.py
  mock_backend_check.py
  virtual_qlabs_check.py

docs/
  ATTACK_PLAN.md
  IMPLEMENTATION_PLAN.md
```

## Current checks

Mock and math checks:

```powershell
py -3.12 -m checks.kinematics_check
py -3.12 -m checks.mock_backend_check
```

Virtual QLabs handoff check:

```powershell
py -3.12 -m checks.virtual_qlabs_check --connect-only
py -3.12 -m checks.virtual_qlabs_check --speed 0.05 --turn 0.0 --seconds 0.5
py -3.12 -m checks.virtual_qlabs_check --speed 0.0 --turn 0.2 --seconds 0.5
```

## Current stop point

The repo is ready for Erick to test the virtual QLabs handoff. Do not continue to physical movement until QLabs behavior is known.

See [`docs/ATTACK_PLAN.md`](docs/ATTACK_PLAN.md).
