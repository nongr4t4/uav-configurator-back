from backend.domain.calculations import (
    calc_required_thrust,
    calc_required_power,
    calc_propeller_speed,
    calc_flight_time_electric,
    calc_flight_time_ICE,
)
from backend.domain.entities import UAVInput, UAVResponse
from backend.domain.validators import validate_main_fields, validate_propulsion


def configure_uav(data: dict) -> dict:
    """
    Основна сервісна функція:
    - парсить вхідні дані у UAVInput
    - валідуює
    - рахує тягу, потужність, теоретичну швидкість пропелера
    - рахує час польоту (електрика / ДВЗ)
    - формує структуровану відповідь UAVResponse
    """

    req = UAVInput(**data)

    # Валідація
    validate_main_fields(req)
    validate_propulsion(req)

    # 1) Тяга та потужність
    thrust = calc_required_thrust(
        rho=req.air_density,
        V=req.cruise_speed,
        S=req.wing_area,
        Cd=req.drag_coefficient,
    )

    power = calc_required_power(thrust, req.cruise_speed)

    # 2) Теоретична швидкість повітря від пропелера
    prop_speed = calc_propeller_speed(req.prop_pitch, req.rpm)

    # 3) Час польоту
    flight_time_electric = None
    flight_time_ice = None
    flight_time_explained = "Час польоту не розраховано для даного типу системи."

    if req.system_type == "electric":
        flight_time_electric = calc_flight_time_electric(
            battery_capacity_wh=req.battery_capacity,
            efficiency=req.system_efficiency,
            power_required=power,
        )
        flight_time_explained = (
            f"Очікуваний час польоту (електросистема): {flight_time_electric:.2f} год, "
            f"на основі ємності батареї {req.battery_capacity} Wh, "
            f"ККД системи {req.system_efficiency:.2f} та споживаної потужності {power:.1f} Вт."
        )

    if req.system_type == "ice":
        flight_time_ice = calc_flight_time_ICE(
            fuel_mass=req.fuel_mass,
            prop_eff=req.prop_efficiency,
            engine_power_kw=req.engine_power_kw,
            bsfc_g_per_kwh=req.bsfc,
        )
        flight_time_explained = (
            f"Очікуваний час польоту (ДВЗ): {flight_time_ice:.2f} год, "
            f"на основі маси палива {req.fuel_mass} кг, "
            f"питомої витрати палива BSFC {req.bsfc} г/(кВт·год) "
            f"та номінальної потужності двигуна {req.engine_power_kw} кВт."
        )

    # 4) Описові пояснення
    thrust_explained = (
        f"Необхідна тяга для подолання аеродинамічного опору на крейсерській швидкості: {thrust:.2f} Н "
        f"(розраховано за формулою T = 0.5 · ρ · V² · S · Cd)."
    )

    power_explained = (
        f"Необхідна потужність для підтримки крейсерської швидкості: {power:.2f} Вт "
        f"(P = T · V)."
    )

    prop_speed_explained = (
        f"Теоретична швидкість потоку повітря, створюваного гвинтом, становить {prop_speed:.2f} м/с, "
        f"розраховано на основі кроку {req.prop_pitch}'' та обертів {req.rpm} RPM."
    )

    result = UAVResponse(
        required_thrust=thrust,
        required_power=power,
        prop_theoretical_speed=prop_speed,
        flight_time_electric=flight_time_electric,
        flight_time_ice=flight_time_ice,
        thrust_explained=thrust_explained,
        power_explained=power_explained,
        prop_speed_explained=prop_speed_explained,
        flight_time_explained=flight_time_explained,
    )

    return result.dict()
