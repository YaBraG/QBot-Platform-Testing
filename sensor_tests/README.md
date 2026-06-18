# QBot Sensor Tests

These scripts are temporary comparison tools for testing the QBot Platform sensors in pure Python.

No ROS is used here.

## What this tests

| Script | Purpose | Quanser dependency |
|---|---|---|
| `quanser_csi_test.py` | Test the QBot downward CSI camera through Quanser PAL | Yes |
| `quanser_lidar_test.py` | Test the QBot LIDAR through Quanser PAL | Yes |
| `realsense_alignment_test.py` | Test Intel RealSense directly with aligned depth-to-color frames | No Quanser |
| `environment_check.py` | Print whether the machine looks like physical QBot hardware | No Quanser |

## Install basic Python dependencies

On Windows:

```powershell
py -3.12 -m pip install numpy opencv-python pyrealsense2
```

On Linux:

```bash
python3 -m pip install numpy opencv-python pyrealsense2
```

The Quanser CSI and LIDAR tests also require Quanser's Python libraries to be installed or available on `PYTHONPATH`.

## Virtual QBot notes

For Quanser virtual CSI/LIDAR tests, QLabs and the correct QBot Platform digital twin streams must already be running. These scripts do not start QLabs, real-time models, or the host peripheral client automatically.

## Physical QBot notes

On the physical QBot, run the scripts directly on the QBot computer. Quanser PAL decides whether to use physical devices or virtual TCP streams based on the platform.

## Run tests

### Check environment

```powershell
py -3.12 sensor_tests/environment_check.py
```

### Quanser CSI camera

```powershell
py -3.12 sensor_tests/quanser_csi_test.py --duration 10 --show --save
```

### Quanser LIDAR

```powershell
py -3.12 sensor_tests/quanser_lidar_test.py --duration 10 --save
```

### RealSense direct alignment test

```powershell
py -3.12 sensor_tests/realsense_alignment_test.py --duration 10 --show --save
```

## Output files

Saved files go to:

```text
sensor_tests/output/
```

The RealSense test saves color images, aligned depth visualization, raw depth, and depth in meters. The Quanser LIDAR test saves angle/distance samples as CSV and NPZ files.
