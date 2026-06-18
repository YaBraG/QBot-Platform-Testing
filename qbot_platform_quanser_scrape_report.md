# QBot Platform Quanser Academic Resources Scrape Report

Date: 2026-06-18
Target upstream: https://github.com/quanser/Quanser_Academic_Resources
Working project: https://github.com/YaBraG/QBot-Platform-Testing

## Main finding

Quanser has two QBot Platform software layers that matter for this project:

1. **QVL / QLabs virtual actor layer**
   - Path: `0_libraries/python/qvl/qbot_platform.py`
   - Purpose: Spawn and control a simulated QBot Platform actor in Quanser Interactive Labs.
   - Best for: our first virtual testing wrapper.

2. **PAL product / driver/sensor layer**
   - Path: `0_libraries/python/pal/products/qbot_platform.py`
   - Purpose: Product-level Python wrappers for QBot Platform driver, keyboard stream, lidar, RealSense, and CSI camera.
   - Best for: matching virtual and physical APIs later.

The custom project should not copy Quanser code directly. It should copy the interface ideas and create a clean wrapper with a stable API that can use virtual QLabs first and hardware/PAL later.

---

## QVL / QLabs virtual actor layer

### File

`0_libraries/python/qvl/qbot_platform.py`

### Class

`QLabsQBotPlatform`

### Constants found

- Actor class ID: `ID_QBOT_PLATFORM = 23`
- Command/state request: `FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE = 10`
- Command/state response: `FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE = 11`
- Transform request: `FCN_QBOT_PLATFORM_SET_TRANSFORM = 14`
- Transform response: `FCN_QBOT_PLATFORM_SET_TRANSFORM_RESPONSE = 15`
- Possess request: `FCN_QBOT_PLATFORM_POSSESS = 20`
- Possess ACK: `FCN_QBOT_PLATFORM_POSSESS_ACK = 21`
- Image request: `FCN_QBOT_PLATFORM_IMAGE_REQUEST = 100`
- Image response: `FCN_QBOT_PLATFORM_IMAGE_RESPONSE = 101`
- LIDAR request: `FCN_QBOT_PLATFORM_LIDAR_DATA_REQUEST = 120`
- LIDAR response: `FCN_QBOT_PLATFORM_LIDAR_DATA_RESPONSE = 121`

### Camera/viewpoint constants

- `VIEWPOINT_RGB = 0`
- `VIEWPOINT_DEPTH = 1`
- `VIEWPOINT_DOWNWARD = 2`
- `VIEWPOINT_TRAILING = 3`
- `CAMERA_RGB = 0`
- `CAMERA_DEPTH = 1`
- `CAMERA_DOWNWARD = 2`

### Useful methods

#### `possess(camera)`
Takes control of a QBot actor camera in QLabs. Useful for visual debugging.

#### `command_and_request_state(rightWheelSpeed, leftWheelSpeed, leftLED, rightLED)`
Sends wheel speeds and LED colors, then returns:

- status
- world location `[x, y, z]`
- forward vector
- up vector
- front bumper hit
- left bumper hit
- right bumper hit
- gyro turn rate in rad/s
- heading in rad
- left encoder count
- right encoder count

Important detail: wheel speed inputs are right wheel speed first, left wheel speed second.

#### `set_transform(location, rotation, scale, leftLED, rightLED, enableDynamics, waitForConfirmation)`
Sets the simulated QBot pose, LED color, scale, and physics/dynamics state.

#### `set_transform_degrees(...)`
Same transform logic but rotation is passed in degrees.

#### `get_image(camera)`
Requests a JPG image from the simulated QBot camera and decodes it using OpenCV.

#### `get_lidar(samplePoints=400)`
Returns LIDAR angles and distances. Internally, the simulation uses 4096 raw samples and an 8 m range, then resamples to the requested sample count.

### Wrapper idea

Create `QBotPlatformVirtual` with these public methods:

```python
spawn(location, yaw_deg)
reset_pose(x, y, yaw_rad)
set_wheel_speeds(left_mps, right_mps)
set_body_velocity(v_mps, omega_radps)
read_state() -> QBotState
read_camera(camera="rgb") -> np.ndarray
read_lidar(samples=400) -> LidarScan
stop()
```

Internally it will call Quanser's QVL class, but our API should use left/right order consistently and hide the Quanser right-first ordering.

---

## PAL product/hardware/digital-twin layer

### File

`0_libraries/python/pal/products/qbot_platform.py`

### Purpose

Quanser describes this module as API classes/tools for QBot Platform sensors, components, basic IO, and safety features.

### Physical-vs-virtual detection

Quanser uses:

```python
IS_PHYSICAL_QBOTPLATFORM = (os.getlogin() == "nvidia" and platform.machine() == "aarch64")
```

Meaning:

- Physical QBot Platform likely runs on NVIDIA/aarch64 Linux hardware.
- Virtual/digital twin uses localhost TCP/IP ports.

### `QBotPlatformDriver`

Default constructor:

```python
QBotPlatformDriver(mode=1, ip="192.168.2.15", driverPort=18888)
```

Important constants:

- `WHEEL_RADIUS = 3.5*0.0254/2`
- `WHEEL_BASE = 0.3928`
- `WHEEL_WIDTH = 0.04445`
- `ENCODER_COUNTS = 85.0`
- `ENCODER_MODE = 4`
- `COUNTS_PER_REV = ENCODER_COUNTS * ENCODER_MODE`
- `LIDAR_POS_X = 8.75*0.0254`
- `LIDAR_POS_Y = 0`

Driver stream:

- URI: `tcpip://<ip>:18888`
- Receive buffer length: 17 doubles
- Send buffer length: 10 doubles

Receive buffer layout:

| Index | Meaning |
|---:|---|
| 0:2 | wheel positions |
| 2:4 | wheel speeds |
| 4:6 | motor commands |
| 6:9 | accelerometer |
| 9:12 | gyroscope |
| 12:14 | motor currents |
| 14 | battery voltage |
| 15 | watchdog |
| 16 | received timestamp |

Send buffer layout:

| Index | Meaning |
|---:|---|
| 0 | mode |
| 1 | user LED flag |
| 2:5 | RGB LED color |
| 5 | arm/motor enable |
| 6 | hold position |
| 7 | command 0 |
| 8 | command 1 |
| 9 | timestamp |

Mode meanings from the Python file:

- `1` and `2`: education modes
- `3` and `4`: research modes
- `1` and `3`: body mode
- `2` and `4`: wheeled mode

### `Keyboard`

- Stream URI: `tcpip://<ip>:18889`
- Receive buffer length: 25 doubles
- Useful values:
  - `wheelCmd = receiveBuffer[16:18]`
  - `bodyCmd = receiveBuffer[18:20]`
  - `k_7 = receiveBuffer[0]`
  - `k_u = receiveBuffer[5]`
  - `k_space = receiveBuffer[24]`

### `QBotPlatformLidar`

Defaults:

```python
QBotPlatformLidar(numMeasurements=1680, lidarPort=18918)
```

Physical URL:

```text
serial://localhost:0?...device='/dev/lidar'
```

Virtual URL:

```text
tcpip://localhost:18918
```

LIDAR type:

```text
leishenm10p
```

### `QBotPlatformRealSense`

Defaults:

- mode: `RGB&DEPTH`
- RGB: 640 x 480 at 30 fps
- Depth: 640 x 480 at 30 fps
- IR: 640 x 480 at 30 fps
- virtual port: `18917`
- physical device ID: `0`
- virtual device ID: `0@tcpip://localhost:18917`

### `QBotPlatformCSICamera`

Defaults:

- width: 640
- height: 400
- frame rate: 60 physical, forced 30 virtual
- virtual port: `18915`
- physical device ID: `0`
- virtual device ID: `0@tcpip://localhost:18915`

---

## Quick-start guides

### Digital twin quick start

Path:

`2_quick_start_guides/qbot_platform/digital_twin/python/quick_start_qbot_platform.py`

Important patterns:

- Imports `setup` from `qlabs_setup.py`.
- Uses localhost for both host and driver.
- Runs a 60 Hz loop.
- Creates:
  - `QBotPlatformDriver(mode=1, ip="localhost")`
  - `QBotPlatformCSICamera(exposure=10)`
  - `QBotPlatformRealSense()`
  - `QBotPlatformLidar()`
  - `Keyboard()`
  - `Probe(...)` visual display sender
- Reads downward camera, RealSense depth/RGB, LIDAR, and keyboard commands.
- Converts keyboard body commands into `commands = [forward_speed, turn_speed]`.
- Uses `k_space` as arm/motor enable and `k_u` as emergency stop.
- Terminates all devices in `finally`.

### Digital twin QLabs setup

Path:

`2_quick_start_guides/qbot_platform/digital_twin/python/qlabs_setup.py`

Important patterns:

- Starts `quanser_host_peripheral_client.exe`.
- Connects to QLabs on localhost.
- Destroys all spawned actors.
- Spawns QBot Platform at requested location.
- Possesses trailing camera.
- Spawns walls.
- Spawns QBot Platform floor tiles.
- Starts real-time models:
  - workspace model: `rtmodels.QBOT_PLATFORM`
  - driver model: `rtmodels.QBOT_PLATFORM_DRIVER`
- Starts driver model with extra argument:
  - `-uri tcpip://localhost:17098`

### Hardware quick start

Path:

`2_quick_start_guides/qbot_platform/hardware/python/quick_start_qbot_platform.py`

Similar structure to the digital twin quick start, but aimed at real hardware. It includes the same ideas: driver, keyboard, cameras, lidar, probe/observer, and cleanup.

### Hardware observer

Path:

`2_quick_start_guides/qbot_platform/hardware/python/observer.py`

Displays:

- Downward facing image: `[400, 640, 1]`
- RealSense RGB image: `[480, 640, 3]`
- RealSense depth image: `[480, 640, 1]`
- Leishen M10P LIDAR plot: `1680` measurements

---

## User manuals found

Path:

`3_user_manuals/qbot_platform/`

Files found:

- `user_manual_connectivity.pdf`
- `user_manual_power.pdf`
- `user_manual_software_python.pdf`
- `user_manual_software_simulink.pdf`
- `user_manual_system_hardware.pdf`
- `ancillary material/`

These should be reviewed later if we need exact startup/power/network steps. For this scrape pass, the code files are more directly useful for our wrapper design.

---

## Research material found

Path:

`5_research/qbot_platform/`

Subfolders:

- `IO_examples/`
  - contains MATLAB and Python IO examples.
- `localization/`
  - contains Simulink localization/state-estimation material and physical driver RT model.
- `ros2/`
  - contains ROS 2 package, launch files, configs, source nodes, and RT models.

### ROS 2 package

Path:

`5_research/qbot_platform/ros2/src/qbot_platform/`

Top-level package files/folders:

- `config/`
- `launch/`
- `rt_models/`
- `src/`
- `CMakeLists.txt`
- `package.xml`
- `LICENSE`

ROS 2 source files:

- `command.cpp`
- `csi.cpp`
- `fixed_lidar_frame.cpp`
- `lidar.cpp`
- `qbot_platform_driver_interface.cpp`
- `rgbd.cpp`

ROS 2 launch files:

- `qbot_platform_cartographer_launch.py`
- `qbot_platform_launch.py`
- `qbot_platform_manual_drive_launch.py`
- `qbot_platform_manual_map_launch.py`
- `qbot_platform_slam_and_nav_bringup_launch.py`

ROS 2 dependencies in `package.xml`:

- `rclcpp`
- `cv_bridge`
- `image_transport`
- `libopencv-dev`
- `std_msgs`
- `geometry_msgs`
- `sensor_msgs`
- `control_msgs`
- `ros2launch`
- `cartographer_ros`
- `nav2_bringup`

ROS 2 executables in `CMakeLists.txt`:

- `qbot_platform_driver_interface`
- `rgbd`
- `lidar`
- `csi`
- `command`
- `fixed_lidar_frame`

---

## Teaching material found

Path:

`6_teaching/3_Robotics/`

Skill progressions found:

- `sp0_play`
- `sp1_task_automation`
- `sp2_surveying/l1_self_localization`
- `sp3_pick_and_place`
- `sp4_kinematic_manipulation`
- `sp5_velocity_manipulation`
- `sp6_visual_manipulation`

For QBot Platform, the most useful teaching areas are likely:

- `sp0_play`: basic operation / play / observer-style interaction
- `sp1_task_automation`: movement task automation
- `sp2_surveying/l1_self_localization`: localization concepts

---

## Recommended custom project architecture

```text
QBot-Platform-Testing/
├── src/
│   └── qbot_platform_testing/
│       ├── __init__.py
│       ├── models.py              # QBotState, LidarScan, CameraFrame, MotorCommand
│       ├── constants.py           # wheel base, wheel radius, ports, camera names
│       ├── interfaces.py          # abstract QBotPlatformInterface
│       ├── virtual_qvl.py         # wraps qvl.qbot_platform.QLabsQBotPlatform
│       ├── digital_twin_pal.py    # wraps pal.products.qbot_platform in localhost mode
│       ├── hardware_pal.py        # later wrapper for real QBot hardware
│       ├── sensors.py             # camera/lidar normalization helpers
│       ├── kinematics.py          # body velocity <-> wheel speed conversions
│       └── safety.py              # clamp speeds, stop, timeout/watchdog helpers
├── examples/
│   ├── virtual_spawn_and_drive.py
│   ├── virtual_read_camera.py
│   ├── virtual_read_lidar.py
│   ├── digital_twin_manual_drive.py
│   └── stop_robot.py
├── tests/
│   ├── test_kinematics.py
│   ├── test_packet_shapes.py
│   ├── test_state_models.py
│   └── test_safety.py
└── docs/
    ├── quanser_scrape_inventory.md
    └── api_design_notes.md
```

---

## First wrapper API proposal

```python
from dataclasses import dataclass
import numpy as np

@dataclass
class QBotState:
    x: float
    y: float
    z: float
    yaw: float
    gyro_z: float
    encoder_left: int | float
    encoder_right: int | float
    bumper_front: bool = False
    bumper_left: bool = False
    bumper_right: bool = False

@dataclass
class LidarScan:
    angles_rad: np.ndarray
    distances_m: np.ndarray

class QBotPlatformInterface:
    def connect(self) -> None: ...
    def reset_pose(self, x: float, y: float, yaw_rad: float) -> None: ...
    def set_wheel_speeds(self, left_mps: float, right_mps: float) -> QBotState: ...
    def set_body_velocity(self, v_mps: float, omega_radps: float) -> QBotState: ...
    def read_state(self) -> QBotState: ...
    def read_lidar(self, samples: int = 400) -> LidarScan: ...
    def read_camera(self, camera: str = "rgb") -> np.ndarray: ...
    def stop(self) -> None: ...
    def close(self) -> None: ...
```

---

## Key design decisions for our project

1. **Make virtual the default.**
   Start with QLabs/QVL because testing on real Linux hardware is harder.

2. **Do not expose Quanser's right-wheel-first command ordering.**
   Our wrapper should use normal left/right order and convert internally.

3. **Separate simulation transport from robot logic.**
   Algorithms should depend on `QBotPlatformInterface`, not on QLabs or PAL directly.

4. **Normalize all state into dataclasses.**
   This avoids returning large ambiguous tuples like Quanser's API.

5. **Keep body velocity and wheel velocity support.**
   QBot supports body-mode and wheel-mode ideas, so our wrapper should support both.

6. **Use safety clamps from day one.**
   Even in simulation, clamp speed and implement `stop()` cleanly.

7. **Create mock tests before real QLabs tests.**
   We can test kinematics, packet shapes, and state conversion without running Quanser software.

---

## Immediate next implementation step

Build only this first:

```text
src/qbot_platform_testing/
├── models.py
├── constants.py
├── kinematics.py
├── interfaces.py
└── virtual_qvl.py
```

Then create one example:

```text
examples/virtual_spawn_drive_square.py
```

The first test should only prove:

1. QLabs launches/spawns QBot.
2. We can set pose.
3. We can command forward movement.
4. We can read state.
5. We can stop.
6. We can close cleanly.
