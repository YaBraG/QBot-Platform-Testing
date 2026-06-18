"""Temporary QBot Platform CSI camera test using Quanser PAL.

This script intentionally uses Quanser's QBotPlatformCSICamera wrapper so we can
judge whether the Quanser CSI path is good enough to keep.

No ROS is used.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import cv2
import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def import_quanser_csi():
    try:
        from pal.products.qbot_platform import QBotPlatformCSICamera
    except ImportError as exc:
        raise SystemExit(
            "Could not import pal.products.qbot_platform.QBotPlatformCSICamera.\n"
            "Make sure Quanser Python libraries are installed or that "
            "Quanser_Academic_Resources/0_libraries/python is on PYTHONPATH.\n"
            f"Original error: {exc}"
        ) from exc

    return QBotPlatformCSICamera


def valid_frame_timestamp(timestamp) -> bool:
    """Quanser camera read methods usually return -1 when no frame is ready."""

    if timestamp is None:
        return False

    try:
        return float(timestamp) >= 0.0
    except (TypeError, ValueError):
        return bool(timestamp)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test QBot CSI camera through Quanser PAL.")
    parser.add_argument("--duration", type=float, default=10.0, help="Test duration in seconds.")
    parser.add_argument("--width", type=int, default=640, help="Requested frame width.")
    parser.add_argument("--height", type=int, default=400, help="Requested frame height.")
    parser.add_argument("--fps", type=float, default=60.0, help="Requested frame rate.")
    parser.add_argument("--exposure", type=float, default=None, help="Optional exposure value.")
    parser.add_argument("--show", action="store_true", help="Show live image preview.")
    parser.add_argument("--save", action="store_true", help="Save last frame to sensor_tests/output.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    QBotPlatformCSICamera = import_quanser_csi()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    camera = None
    frame_count = 0
    dropped_count = 0
    last_frame = None
    start_time = time.perf_counter()

    print("Starting Quanser CSI camera test")
    print(f"Requested: {args.width}x{args.height} @ {args.fps} fps")
    print("Press q in the preview window to quit early.")

    try:
        camera = QBotPlatformCSICamera(
            frameWidth=args.width,
            frameHeight=args.height,
            frameRate=args.fps,
            exposure=args.exposure,
        )

        while True:
            elapsed = time.perf_counter() - start_time
            if elapsed >= args.duration:
                break

            timestamp = camera.read()

            if valid_frame_timestamp(timestamp):
                frame = getattr(camera, "imageData", None)

                if frame is not None and isinstance(frame, np.ndarray) and frame.size > 0:
                    frame_count += 1
                    last_frame = frame.copy()

                    if args.show:
                        cv2.imshow("Quanser CSI Camera", frame)
                        key = cv2.waitKey(1) & 0xFF
                        if key == ord("q"):
                            break
                else:
                    dropped_count += 1
            else:
                dropped_count += 1

        total_time = max(time.perf_counter() - start_time, 1e-9)
        measured_fps = frame_count / total_time

        print("\nQuanser CSI test result")
        print("-----------------------")
        print(f"Frames received: {frame_count}")
        print(f"Dropped/no-frame reads: {dropped_count}")
        print(f"Measured FPS: {measured_fps:.2f}")

        if last_frame is not None:
            print(f"Last frame shape: {last_frame.shape}")
            print(f"Last frame dtype: {last_frame.dtype}")

            if args.save:
                output_path = OUTPUT_DIR / "quanser_csi_last_frame.png"
                cv2.imwrite(str(output_path), last_frame)
                print(f"Saved: {output_path}")
        else:
            print("No valid frame was captured.")

    finally:
        if camera is not None:
            camera.terminate()
        if args.show:
            cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
