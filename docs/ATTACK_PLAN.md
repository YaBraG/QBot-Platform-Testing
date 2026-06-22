# QBot Attack Plan

## Mission

Move the QBot through one clean Python API, without ROS, while keeping Quanser code isolated behind backends or wrappers.

## Working rule

Core code goes on `main`. Experimental sensor tests stay on separate branches.

## Team model

I implement the core architecture and code up to the virtual-testing handoff. Erick runs the virtual QLabs tests and reports what works or fails. I do not assume QLabs behavior until that feedback exists.

## Sprint 1: Make the API executable

Goal: prove that the architecture works without Quanser, QLabs, or physical hardware.

Implemented:

- `QBotMover` creates and delegates to a backend.
- `MockBackend` simulates basic differential-drive motion.
- `qbot/state.py` contains real dataclasses.
- `qbot/limits.py` clamps movement commands.
- `checks/kinematics_check.py` verifies core movement math.
- `checks/mock_backend_check.py` verifies the first usable movement path.

Run checks:

```powershell
py -3.12 -m checks.kinematics_check
py -3.12 -m checks.mock_backend_check
```

## Sprint 2: Virtual QLabs handoff

Goal: Erick tests QLabs movement from the clean API.

Prepared:

- `VirtualQLabsBackend` imports QLabs/QVL lazily.
- `VirtualQLabsBackend` opens a QLabs connection.
- `VirtualQLabsBackend` spawns actor 0.
- Public wheel order stays left, right.
- The backend converts to QVL order internally.
- `checks/virtual_qlabs_check.py` is the handoff script.

Run virtual handoff checks:

```powershell
py -3.12 -m checks.virtual_qlabs_check --connect-only
py -3.12 -m checks.virtual_qlabs_check --speed 0.05 --turn 0.0 --seconds 0.5
py -3.12 -m checks.virtual_qlabs_check --speed 0.0 --turn 0.2 --seconds 0.5
```

Erick reports:

- Whether QLabs imports work.
- Whether QLabs connection works.
- Whether actor 0 spawns.
- Whether forward motion is correct.
- Whether turn direction is correct.
- Whether returned state is usable.

Stop point:

- Do not continue past virtual execution until Erick reports QLabs results.

## Sprint 3: Sensor decision branch

Goal: decide what to keep.

Tasks on sensor branch:

- Test Quanser CSI.
- Test Quanser LIDAR.
- Test direct RealSense SDK alignment.
- Record FPS, missed frames, saved output, and final recommendation.

## Sprint 4: Physical read-only first

No physical driving until read-only checks are stable.

## Sprint 5: Physical tiny movement

Only after virtual behavior and read-only physical checks are stable.
