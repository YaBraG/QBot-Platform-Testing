"""Handoff check for QLabs virtual QBot.

Run this only when QLabs is open and Quanser Python libraries are on PYTHONPATH.
"""

from __future__ import annotations

import argparse
import time

from qbot.mover import QBotMover


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--speed", type=float, default=0.05)
    parser.add_argument("--turn", type=float, default=0.0)
    parser.add_argument("--seconds", type=float, default=0.5)
    parser.add_argument("--connect-only", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    qbot = QBotMover(force_mode="virtual")

    try:
        print("connecting to virtual QBot...")
        qbot.connect()
        print("connected")
        print("initial state:", qbot.read_state())

        if not args.connect_only:
            print(f"running virtual command: speed={args.speed}, turn={args.turn}, seconds={args.seconds}")
            qbot.set_body_velocity(args.speed, args.turn)
            time.sleep(args.seconds)
            qbot.stop()
            print("state after command:", qbot.read_state())
        else:
            qbot.stop()

        print("virtual_qlabs_check completed")

    finally:
        qbot.close()


if __name__ == "__main__":
    main()
