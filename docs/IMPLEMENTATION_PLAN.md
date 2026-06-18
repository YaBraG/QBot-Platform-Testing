# QBot Pure Python Implementation Plan

This document tracks the project direction and fallback options.

## Rules

TODO:
- Keep the project pure Python.
- Do not use ROS.
- Keep core structure on `main`.
- Keep experimental sensor tests on a separate branch.
- Hide Quanser dependencies behind wrappers or backends.

## Phase 1: Core structure

TODO:
- Finish `QBotMover` backend selection.
- Keep Quanser imports out of the main API.
- Add basic mock backend integration.

## Phase 2: Virtual movement

TODO:
- Implement `VirtualQLabsBackend`.
- Test wheel speed order.
- Test straight movement.
- Test turn direction.
- Add state conversion from QLabs return data.

Fallback:
- Use `MockBackend` if QLabs is unavailable.

## Phase 3: Sensor wrappers

TODO:
- Wrap Quanser CSI after test results.
- Wrap Quanser LIDAR after test results.
- Wrap direct RealSense SDK if it is better than Quanser.

Fallback:
- Use OpenCV for CSI if Quanser CSI is not good enough.
- Use direct LIDAR access later if Quanser LIDAR is not good enough.

## Phase 4: Physical movement

TODO:
- Implement `PhysicalQBotBackend` only after virtual movement is stable.
- Add strict safety limits.
- Add automatic stop on failure.
- Add physical read-only checks before motion.

Fallback:
- Continue with virtual and mock backends if physical movement is unreliable.

## Phase 5: Examples

TODO:
- Implement examples only after backend methods work.
- Keep examples short and safe.
- Put physical movement behind explicit warnings and small speeds.
