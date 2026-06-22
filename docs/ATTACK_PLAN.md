# QBot Attack Plan

## Mission

Move the QBot through one clean Python API, without ROS, while keeping Quanser code isolated behind backends or wrappers.

## Working rule

Core code goes on `main`. Experimental sensor tests stay on separate branches.

## Team model

I implement the core architecture and code up to the virtual-testing handoff. Erick runs the virtual QLabs tests and reports what works or fails. I do not assume QLabs behavior until that feedback exists.

## Sprint 1: Make the API executable

Goal: prove that the architecture works without Quanser, QLabs, or physical hardware.

Implemented now:

- `QBotMover` creates and delegates to a backend.
- `MockBackend` simulates basic differential-drive motion.
- `qbot/state.py` now contains real dataclasses.
- `qbot/limits.py` clamps movement commands.
- `checks/kinematics_check.py` verifies core movement math.
- `checks/mock_backend_check.py` verifies the first usable movement path.

Run checks:

```powershell
py -3.12 checks/kinematics_check.py
py -3.12 checks/mock_backend_check.py
```

## Sprint 2: Virtual QLabs handoff

Goal: prepare the code so Erick can test QLabs movement from the clean API.

Tasks before handoff:

- Keep `VirtualQLabsBackend` isolated from the rest of the code.
- Keep all QLabs/QVL imports lazy inside the virtual backend.
- Prepare the backend methods that need implementation.
- Document the expected QLabs behavior to verify.

Erick tests:

- Whether QLabs imports work.
- Whether QLabs connection works.
- Whether actor 0 can be spawned or attached.
- Whether wheel command order is correct.
- Whether turn sign is correct.
- Whether returned QLabs state is reliable enough.

Stop point:

- Do not continue past virtual execution until Erick reports QLabs results.

Fallbacks:

- If QLabs import fails, keep mock development moving.
- If wheel order is wrong, fix only inside `VirtualQLabsBackend`.
- If QLabs state is unreliable, start with time-based commands and improve feedback later.

## Sprint 3: Sensor decision branch

Goal: decide what to keep.

Tasks on sensor branch:

- Test Quanser CSI.
- Test Quanser LIDAR.
- Test direct RealSense SDK alignment.
- Record FPS, missed frames, saved output, and final recommendation.

Decision:

- Keep Quanser CSI only if stable and simple.
- Keep Quanser LIDAR only if scan quality and rate are stable.
- Use direct RealSense if alignment/control is clearly better.

## Sprint 4: Physical read-only first

Goal: touch physical QBot without movement first.

Tasks:

- Implement physical connect.
- Read state or driver feedback.
- Read battery if available.
- Confirm stop command can be sent.

No physical driving until read-only checks are stable.

## Sprint 5: Physical tiny movement

Goal: run tiny controlled movements on the real QBot.

Rules:

- Always use low speeds.
- Always use short durations.
- Always stop in `finally`.
- Stop immediately if state feedback is stale or unexpected.

First commands:

- 0.1 m/s forward for 0.5 seconds.
- 0.2 rad/s turn for 0.5 seconds.
- Stop-only test.

## Definition of success

The project succeeds when this same code shape works in mock, virtual, and physical modes:

```python
from qbot.mover import QBotMover

qbot = QBotMover(force_mode="mock")
qbot.connect()
qbot.drive_for_seconds(0.1, 0.0, 1.0)
state = qbot.read_state()
qbot.close()
```
