# QBot Platform Testing

Pure Python testing repo for the Quanser QBot Platform.

Current focus:

- Test QLabs / virtual QBot behavior first.
- Keep the code usable later on the physical QBot.
- Avoid ROS completely for now.
- Use Quanser libraries only where they are useful or unavoidable.

## Sensor tests

Temporary sensor comparison scripts live in:

```text
sensor_tests/
```

They currently include:

- Quanser CSI camera test
- Quanser LIDAR test
- Intel RealSense direct depth-alignment test
- Environment detection check

See [`sensor_tests/README.md`](sensor_tests/README.md) for commands.
