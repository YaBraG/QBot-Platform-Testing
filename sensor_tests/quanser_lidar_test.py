"""Temporary QBot Platform LIDAR test using Quanser PAL.

This script intentionally uses Quanser's QBotPlatformLidar wrapper so we can
judge whether the Quanser LIDAR path is good enough to keep.

No ROS is used.
"""

from __future__ import annotations

import argparse
import csv
import math
import time
from pathlib import Path

import numpy as np


OUTPUT_DIR = Path(__file__).resolve().parent / "output"


def import_quanser_lidar():
    try:
        from pal.products.qbot_platform import QBotPlatformLidar
    except ImportError as exc:
        raise SystemExit(
            "Could not import pal.products.qbot_platform.QBotPlatformLidar.\n"
            "Make sure Quanser Python libraries are installed or that "
            "Quanser_Academic_Resources/0_libraries/python is on PYTHONPATH.\n"
            f"Original error: {exc}"
        ) from exc

    return QBotPlatformLidar


def summarize_scan(angles: np.ndarray, distances: np.ndarray) -> dict[str, float]:
    finite_mask = np.isfinite(distances)
    positive_mask = finite_mask & (distances > 0.0)

    if not np.any(positive_mask):
        return {
            "valid_points": 0,
            "min_m": math.nan,
            "max_m": math.nan,
            "mean_m": math.nan,
            "angle_span_rad": math.nan,
        }

    valid_distances = distances[positive_mask]
    valid_angles = angles[positive_mask]

    return {
        "valid_points": int(valid_distances.size),
        "min_m": float(np.min(valid_distances)),
        "max_m": float(np.max(valid_distances)),
        "mean_m": float(np.mean(valid_distances)),
        "angle_span_rad": float(np.max(valid_angles) - np.min(valid_angles)),
    }


def save_scan_csv(path: Path, angles: np.ndarray, distances: np.ndarray) -> None:
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["index", "angle_rad", "distance_m"])
        for index, (angle, distance) in enumerate(zip(angles, distances)):
            writer.writerow([index, float(angle), float(distance)])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Test QBot LIDAR through Quanser PAL.")
    parser.add_argument("--duration", type=float, default=10.0, help="Test duration in seconds.")
    parser.add_argument("--measurements", type=int, default=1680, help="Requested LIDAR measurements.")
    parser.add_argument("--save", action="store_true", help="Save last scan to sensor_tests/output.")
    parser.add_argument("--print-every", type=int, default=10, help="Print every N valid scans.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    QBotPlatformLidar = import_quanser_lidar()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    lidar = None
    scan_count = 0
    missed_count = 0
    last_angles = None
    last_distances = None
    start_time = time.perf_counter()

    print("Starting Quanser LIDAR test")
    print(f"Requested measurements: {args.measurements}")

    try:
        lidar = QBotPlatformLidar(numMeasurements=args.measurements)

        while True:
            elapsed = time.perf_counter() - start_time
            if elapsed >= args.duration:
                break

            new_scan = lidar.read()

            if new_scan:
                angles = np.asarray(getattr(lidar, "angles", []), dtype=np.float64)
                distances = np.asarray(getattr(lidar, "distances", []), dtype=np.float64)

                if angles.size > 0 and distances.size > 0 and angles.size == distances.size:
                    scan_count += 1
                    last_angles = angles.copy()
                    last_distances = distances.copy()

                    if args.print_every > 0 and scan_count % args.print_every == 0:
                        stats = summarize_scan(angles, distances)
                        print(
                            f"scan={scan_count} "
                            f"points={stats['valid_points']} "
                            f"min={stats['min_m']:.3f}m "
                            f"max={stats['max_m']:.3f}m "
                            f"mean={stats['mean_m']:.3f}m"
                        )
                else:
                    missed_count += 1
            else:
                missed_count += 1

        total_time = max(time.perf_counter() - start_time, 1e-9)
        measured_hz = scan_count / total_time

        print("\nQuanser LIDAR test result")
        print("-------------------------")
        print(f"Scans received: {scan_count}")
        print(f"Missed/no-scan reads: {missed_count}")
        print(f"Measured scan rate: {measured_hz:.2f} Hz")

        if last_angles is not None and last_distances is not None:
            stats = summarize_scan(last_angles, last_distances)
            print(f"Last scan points: {last_angles.size}")
            print(f"Valid positive points: {stats['valid_points']}")
            print(f"Min distance: {stats['min_m']:.3f} m")
            print(f"Max distance: {stats['max_m']:.3f} m")
            print(f"Mean distance: {stats['mean_m']:.3f} m")
            print(f"Angle span: {stats['angle_span_rad']:.3f} rad")

            if args.save:
                csv_path = OUTPUT_DIR / "quanser_lidar_last_scan.csv"
                npz_path = OUTPUT_DIR / "quanser_lidar_last_scan.npz"
                save_scan_csv(csv_path, last_angles, last_distances)
                np.savez(npz_path, angles_rad=last_angles, distances_m=last_distances)
                print(f"Saved: {csv_path}")
                print(f"Saved: {npz_path}")
        else:
            print("No valid LIDAR scan was captured.")

    finally:
        if lidar is not None:
            lidar.terminate()


if __name__ == "__main__":
    main()
