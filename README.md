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
  environment.py      Runtime mode detection: virtual, physical, or mock
  constants.py        Shared QBot constants
  state.py            Dataclasses for command, state, camera, and LIDAR data
  kinematics.py       Differential-drive math
  limits.py           Command limit helpers
  mover.py            Main user-facing QBotMover API

backends/
  base_backend.py          Abstract backend interface
  mock_backend.py          Pure Python development backend
  virtual_qlabs_backend.py QLabs/QVL backend placeholder
  physical_qbot_backend.py Physical QBot backend placeholder

sensors/
  quanser_csi.py       Quanser CSI wrapper placeholder
  quanser_lidar.py     Quanser LIDAR wrapper placeholder
  realsense_direct.py  Direct pyrealsense2 wrapper placeholder
  opencv_camera.py     OpenCV camera fallback placeholder

checks/
  kinematics_check.py
  mock_backend_check.py

examples/
  drive_forward.py
  turn_in_place.py
  drive_square.py
  sensor_preview.py

docs/
  ATTACK_PLAN.md
  IMPLEMENTATION_PLAN.md
```

## Runtime mode override

The project will use `QBOT_MODE` to force a mode when needed:

```powershell
$env:QBOT_MODE="virtual"
$env:QBOT_MODE="physical"
$env:QBOT_MODE="mock"
```

On Linux:

```bash
export QBOT_MODE=virtual
export QBOT_MODE=physical
export QBOT_MODE=mock
```

## Current executable checks

These checks do not require Quanser, QLabs, ROS, or physical hardware.

```powershell
py -3.12 checks/kinematics_check.py
py -3.12 checks/mock_backend_check.py
```

## Current stop point

The repo is ready up to the mock/backend architecture stage. The next major step is virtual QLabs testing, which Erick will run. Development should stop at that handoff until QLabs results are known.

## Development direction

1. Keep mock-mode movement stable.
2. Prepare virtual backend handoff.
3. Erick tests QLabs virtual behavior.
4. Use Erick's QLabs result to implement or correct `VirtualQLabsBackend`.
5. Test Quanser CSI and LIDAR on a test branch.
6. Compare RealSense direct SDK against Quanser RealSense.
7. Only then work on physical movement.

See [`docs/ATTACK_PLAN.md`](docs/ATTACK_PLAN.md).
