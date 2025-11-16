import math


def calc_required_thrust(rho: float, V: float, S: float, Cd: float) -> float:
    """
    Необхідна тяга для горизонтального польоту:
    T = D = 0.5 * rho * V^2 * S * Cd
    """
    return 0.5 * rho * (V ** 2) * S * Cd


def calc_required_power(thrust: float, V: float) -> float:
    """
    Необхідна потужність:
    P = T * V
    """
    return thrust * V


def calc_propeller_speed(pitch_in: float, rpm: float) -> float:
    """
    Теоретична швидкість від пропелера.

    Беремо формулу з документа:
    V_max ≈ (Pitch × RPM × 0.8) / 63360  [в милях/год]

    Ми конвертуємо результат у м/с:
    1 mph ≈ 0.44704 м/с
    """
    v_mph = (pitch_in * rpm * 0.8) / 63360.0
    v_mps = v_mph * 0.44704
    return v_mps


def calc_flight_time_electric(battery_capacity_wh: float, efficiency: float, power_required: float) -> float:
    """
    Час польоту для електричної системи:
    t = (E * η) / P, де:
    E — ємність батареї у Wh,
    η — ККД системи,
    P — споживана потужність у W.
    Повертаємо t у годинах.
    """
    if power_required <= 0:
        return 0.0
    available_energy_wh = battery_capacity_wh * efficiency
    return available_energy_wh / power_required


def calc_flight_time_ICE(fuel_mass: float, prop_eff: float, engine_power_kw: float, bsfc_g_per_kwh: float) -> float:
    """
    Час польоту для ДВЗ.

    Використовуємо BSFC у г/(кВт·год).

    Спочатку переводимо BSFC у кг/(кВт·год):
        bsfc_kg = bsfc_g / 1000

    Витрата палива:
        fuel_flow = bsfc_kg * engine_power_kw  [кг/год]

    Час польоту:
        t = fuel_mass / fuel_flow
    """
    if fuel_mass <= 0 or engine_power_kw <= 0 or bsfc_g_per_kwh <= 0:
        return 0.0

    bsfc_kg_per_kwh = bsfc_g_per_kwh / 1000.0
    fuel_flow_kg_per_h = bsfc_kg_per_kwh * engine_power_kw

    if fuel_flow_kg_per_h <= 0:
        return 0.0

    return fuel_mass / fuel_flow_kg_per_h
