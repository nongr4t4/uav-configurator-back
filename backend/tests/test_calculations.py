from backend.domain.calculations import (
    calc_required_thrust,
    calc_required_power,
    calc_propeller_speed,
    calc_flight_time_electric,
    calc_flight_time_ICE,
)


def test_required_thrust():
    assert calc_required_thrust(rho=1.225, V=20, S=0.7, Cd=0.05) > 0


def test_required_power():
    thrust = 15
    speed = 20
    assert calc_required_power(thrust, speed) == thrust * speed


def test_propeller_speed():
    speed = calc_propeller_speed(10, 3000)
    assert speed > 0


def test_flight_time_electric():
    t = calc_flight_time_electric(500, 0.9, 200)
    assert t > 0


def test_flight_time_ice():
    t = calc_flight_time_ICE(2, 0.7, 5, 250)
    assert t > 0
