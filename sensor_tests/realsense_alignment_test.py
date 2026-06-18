"""Temporary RealSense SDK alignment test.

This script tests Intel RealSense directly with pyrealsense2 so we can compare
it against Quanser's RealSense wrapper later.

No Quanser and no ROS are used.
"""

from __future__ import annotations

import argparse
import time
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


@dataclass
class RealSenseFrames:
    color_bgr: np.ndarray
    depth_raw: np.ndarray
    depth_meters: np.ndarray
    depth_colormap: np.ndarray


def import_realsense():
    try:
        import pyrealsense2 as rs
    except ImportError as exc:
        raise SystemExit(
            "Could not import pyrealsense2. Install it first.\n"
            "Windows: py -3.12 -m pip install pyrealsense2\n"
            "Linux:   python3 -m pip install pyrealsense2\n"
            f"Original error: {exc}"
        ) from exc

    return rs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test Intel RealSense depth alignment directly.")
    parser.add_argument("--duration", type=float, default=10.0, help="Test duration in seconds.")
    parser.add_argument("--width", type=int, default=640, help="Color/depth frame width.")
    parser.add_argument("--height", type=int, default=480, help="Color/depth frame height.")
    parser.add_argument("--fps", type=int, default=30, help="Frame rate.")
    parser.add_argument("--show", action="store_true", help="Show live color and aligned depth preview.")
    parser.add_argument("--save", action="store_true", help="Save last frame set to sensor_tests/output.")
    return parser.parse_args()


def create_depth_colormap(depth_raw: np.ndarray) -> np.ndarray:
    depth_8bit = cv2.convertScaleAbs(depth_raw, alpha=0.03)
    return cv2.applyColorMap(depth_8bit, cv2.COLORMAP_JET)


def save_frames(frames: RealSenseFrames) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    color_path = OUTPUT_DIR / "realsense_color_bgr.png"
    depth_visual_path = OUTPUT_DIR / "realsense_aligned_depth_colormap.png"
    depth_raw_path = OUTPUT_DIR / "realsense_aligned_depth_raw.npy"
    depth_meters_path = OUTPUT_DIR / "realsense_aligned_depth_meters.npy"

    cv2.imwrite(str(color_path), frames.color_bgr)
    cv2.imwrite(str(depth_visual_path), frames.depth_colormap)
    np.save(depth_raw_path, frames.depth_raw)
    np.save(depth_meters_path, frames.depth_meters)

    print(f"Saved: {color_path}")
    print(f"Saved: {depth_visual_path}")
    print(f"Saved: {depth_raw_path}")
    print(f"Saved: {depth_meters_path}")


def main() -> None:
    args = parse_args()
    rs = import_realsense()

    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, args.width, args.height, rs.format.z16, args.fps)
    config.enable_stream(rs.stream.color, args.width, args.height, rs.format.bgr8, args.fps)

    align_to_color = rs.align(rs.stream.color)

    frame_count = 0
    missed_count = 0
    last_frames: RealSenseFrames | None = None
    start_time = time.perf_counter()

    print("Starting RealSense direct alignment test")
    print(f"Requested: {args.width}x{args.height} @ {args.fps} fps")
    print("Depth stream will be aligned to the color stream.")
    print("Press q in the preview window to quit early.")

    profile = pipeline.start(config)

    try:
        depth_sensor = profile.get_device().first_depth_sensor()
        depth_scale = float(depth_sensor.get_depth_scale())
        print(f"Depth scale: {depth_scale} meters/unit")

        # Give auto-exposure a moment to settle.
        for _ in range(15):
            pipeline.wait_for_frames()

        while True:
            elapsed = time.perf_counter() - start_time
            if elapsed >= args.duration:
                break

            raw_frames = pipeline.wait_for_frames(timeout_ms=1000)
            aligned_frames = align_to_color.process(raw_frames)

            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()

            if not color_frame or not depth_frame:
                missed_count += 1
                continue

            color_bgr = np.asanyarray(color_frame.get_data())
            depth_raw = np.asanyarray(depth_frame.get_data())
            depth_meters = depth_raw.astype(np.float32) * depth_scale
            depth_colormap = create_depth_colormap(depth_raw)

            last_frames = RealSenseFrames(
                color_bgr=color_bgr.copy(),
                depth_raw=depth_raw.copy(),
                depth_meters=depth_meters.copy(),
                depth_colormap=depth_colormap.copy(),
            )
            frame_count += 1

            if args.show:
                stacked = np.hstack((color_bgr, depth_colormap))
                cv2.imshow("RealSense color | aligned depth", stacked)
                key = cv2.waitKey(1) & 0xFF
                if key == ord("q"):
                    break

        total_time = max(time.perf_counter() - start_time, 1e-9)
        measured_fps = frame_count / total_time

        print("\nRealSense direct alignment result")
        print("---------------------------------")
        print(f"Frames received: {frame_count}")
        print(f"Missed/no-frame reads: {missed_count}")
        print(f"Measured FPS: {measured_fps:.2f}")

        if last_frames is not None:
            valid_depth = last_frames.depth_meters[last_frames.depth_meters > 0.0]
            print(f"Color shape: {last_frames.color_bgr.shape}")
            print(f"Depth shape: {last_frames.depth_raw.shape}")
            if valid_depth.size > 0:
                print(f"Valid depth min: {float(np.min(valid_depth)):.3f} m")
                print(f"Valid depth max: {float(np.max(valid_depth)):.3f} m")
                print(f"Valid depth mean: {float(np.mean(valid_depth)):.3f} m")
            else:
                print("No positive depth values in last frame.")

            if args.save:
                save_frames(last_frames)
        else:
            print("No valid RealSense frames were captured.")

    finally:
        pipeline.stop()
        if args.show:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
