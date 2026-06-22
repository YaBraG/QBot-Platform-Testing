import time

from qbot.mover import QBotMover


def main():
    qbot = QBotMover(force_mode="mock")
    assert qbot.mode == "mock"
    assert qbot.backend.__class__.__name__ == "MockBackend"

    qbot.connect()
    qbot.set_body_velocity(0.1, 0.0)
    time.sleep(0.02)
    state = qbot.read_state()
    assert state.x_m > 0.0

    qbot.stop()
    state = qbot.read_state()
    assert state.forward_mps == 0.0
    assert state.turn_radps == 0.0

    qbot.close()
    print("mock_backend_check passed")


if __name__ == "__main__":
    main()
