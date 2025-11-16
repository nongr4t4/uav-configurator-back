import pytest
from backend.domain.entities import UAVInput
from backend.domain.validators import validate_main_fields, validate_propulsion
from backend.utils.exceptions import ValidationError


def test_main_fields_validation_ok():
    inp = UAVInput(
        air_density=1.2,
        cruise_speed=30,
        wing_area=0.8,
        drag_coefficient=0.05,
        prop_pitch=10,
        rpm=5000,
        system_type="electric",
        battery_capacity=500,
        system_efficiency=0.8,
        fuel_mass=None,
        prop_efficiency=None,
        engine_power_kw=None,
        bsfc=None
    )
    validate_main_fields(inp)


def test_wrong_system_type():
    inp = UAVInput(
        air_density=1.2,
        cruise_speed=30,
        wing_area=0.8,
        drag_coefficient=0.05,
        prop_pitch=10,
        rpm=5000,
        system_type="incorrect",
        battery_capacity=None,
        system_efficiency=None,
        fuel_mass=None,
        prop_efficiency=None,
        engine_power_kw=None,
        bsfc=None
    )
    with pytest.raises(ValidationError):
        validate_propulsion(inp)
