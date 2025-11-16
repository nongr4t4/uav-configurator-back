from backend.utils.exceptions import ValidationError
from backend.domain.entities import UAVInput


def validate_main_fields(req: UAVInput) -> None:
    """
    Додаткова ручна валідація базових полів
    (поверх обмежень у Field, але з більш інформативними повідомленнями).
    """

    if req.cruise_speed <= 0 or req.cruise_speed > 200:
        raise ValidationError("Крейсерська швидкість має бути в межах 0–200 м/с.")

    if req.wing_area <= 0 or req.wing_area > 50:
        raise ValidationError("Площа крила повинна бути в межах 0–50 м².")

    if not (0.01 <= req.drag_coefficient <= 2.0):
        raise ValidationError("Коефіцієнт опору Cd має бути в межах 0.01–2.0.")

    if req.air_density <= 0.5 or req.air_density >= 2.0:
        raise ValidationError("Густина повітря повинна бути в межах 0.5–2.0 кг/м³.")

    if req.prop_pitch <= 0:
        raise ValidationError("Крок пропелера має бути більшим за нуль.")

    if req.rpm <= 0:
        raise ValidationError("RPM має бути більшим за нуль.")


def validate_propulsion(req: UAVInput) -> None:
    """
    Перевірка залежно від типу силової установки.
    """

    if req.system_type == "electric":
        if req.battery_capacity is None or req.battery_capacity <= 0:
            raise ValidationError("Для електричної системи потрібно вказати battery_capacity > 0.")
        if req.system_efficiency is None or not (0.1 <= req.system_efficiency <= 1.0):
            raise ValidationError("Для електричної системи потрібно вказати system_efficiency у межах 0.1–1.0.")

    elif req.system_type == "ice":
        if req.fuel_mass is None or req.fuel_mass <= 0:
            raise ValidationError("Для ДВЗ потрібно вказати fuel_mass > 0.")
        if req.prop_efficiency is None or not (0.1 <= req.prop_efficiency <= 1.0):
            raise ValidationError("Для ДВЗ потрібно вказати prop_efficiency у межах 0.1–1.0.")
        if req.engine_power_kw is None or req.engine_power_kw <= 0:
            raise ValidationError("Для ДВЗ потрібно вказати engine_power_kw > 0.")
        if req.bsfc is None or req.bsfc <= 0:
            raise ValidationError("Для ДВЗ потрібно вказати BSFC > 0 (г/кВт·год).")

    else:
        raise ValidationError("Невідомий тип системи. Дозволені значення: 'electric' або 'ice'.")
