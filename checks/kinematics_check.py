from qbot.constants import WHEEL_BASE_M
from qbot.kinematics import body_to_wheel_speeds, wheel_to_body_speeds


def almost_equal(a, b, eps=1e-9):
    return abs(a - b) <= eps


def main():
    left, right = body_to_wheel_speeds(0.2, 0.0)
    assert almost_equal(left, 0.2)
    assert almost_equal(right, 0.2)

    left, right = body_to_wheel_speeds(0.0, 1.0)
    assert almost_equal(left, -WHEEL_BASE_M / 2.0)
    assert almost_equal(right, WHEEL_BASE_M / 2.0)

    left, right = body_to_wheel_speeds(0.15, 0.4)
    forward, turn = wheel_to_body_speeds(left, right)
    assert almost_equal(forward, 0.15)
    assert almost_equal(turn, 0.4)

    print("kinematics_check passed")


if __name__ == "__main__":
    main()
