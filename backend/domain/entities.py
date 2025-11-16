from pydantic import BaseModel, Field
from typing import Optional, Literal


class UAVInput(BaseModel):
    """
    Вхідні дані для розрахунку ГМГ БПЛА.
    """

    # Аеродинамічні параметри
    air_density: float = Field(
        ...,
        gt=0.5,
        lt=2.0,
        description="Густина повітря, кг/м³ (типово 1.225 на рівні моря)",
    )
    cruise_speed: float = Field(
        ...,
        gt=0,
        lt=200,
        description="Крейсерська швидкість, м/с",
    )
    wing_area: float = Field(
        ...,
        gt=0,
        lt=50,
        description="Еквівалентна площа крила або проекція, м²",
    )
    drag_coefficient: float = Field(
        ...,
        gt=0.01,
        lt=2.0,
        description="Коефіцієнт лобового опору Cd",
    )

    # Пропелер
    prop_pitch: float = Field(
        ...,
        gt=1,
        lt=50,
        description="Крок пропелера у дюймах",
    )
    rpm: float = Field(
        ...,
        gt=100,
        lt=20000,
        description="Оберти гвинта, RPM",
    )

    # Тип силової установки
    system_type: Literal["electric", "ice"] = Field(
        ...,
        description="Тип силової системи: 'electric' (електрика) або 'ice' (ДВЗ)",
    )

    # 🔌 Для електричної системи
    battery_capacity: Optional[float] = Field(
        None,
        gt=0,
        lt=50000,
        description="Ємність батареї, Вт·год",
    )
    system_efficiency: Optional[float] = Field(
        None,
        gt=0.1,
        lt=1.0,
        description="Загальний ККД електросистеми (0–1)",
    )

    # ⛽ Для системи з ДВЗ
    fuel_mass: Optional[float] = Field(
        None,
        gt=0,
        lt=100,
        description="Маса палива, кг",
    )
    prop_efficiency: Optional[float] = Field(
        None,
        gt=0.1,
        lt=1.0,
        description="Ефективність пропелера (0–1)",
    )
    engine_power_kw: Optional[float] = Field(
        None,
        gt=0.1,
        lt=500,
        description="Номінальна потужність ДВЗ, кВт",
    )
    bsfc: Optional[float] = Field(
        None,
        gt=50,
        lt=500,
        description="Питома витрата палива BSFC, г/(кВт·год)",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "air_density": 1.225,
                "cruise_speed": 25,
                "wing_area": 0.8,
                "drag_coefficient": 0.32,
                "prop_pitch": 12,
                "rpm": 8000,
                "system_type": "electric",
                "battery_capacity": 16000,
                "system_efficiency": 0.85,
                "fuel_mass": None,
                "prop_efficiency": None,
                "engine_power_kw": None,
                "bsfc": None,
            }
        }


class UAVResponse(BaseModel):
    """
    Результати розрахунку ГМГ + пояснення.
    """

    # Основні результати
    required_thrust: float
    required_power: float
    prop_theoretical_speed: float

    # Час польоту (залежить від типу системи)
    flight_time_electric: Optional[float]
    flight_time_ice: Optional[float]

    # Текстові пояснення (для UI / інженерної документації)
    thrust_explained: str
    power_explained: str
    prop_speed_explained: str
    flight_time_explained: str

    class Config:
        json_schema_extra = {
            "example": {
                "required_thrust": 12.5,
                "required_power": 310.2,
                "prop_theoretical_speed": 43.8,
                "flight_time_electric": 1.8,
                "flight_time_ice": None,
                "thrust_explained": "Необхідна тяга для подолання опору на крейсерській швидкості: 12.5 Н.",
                "power_explained": "Необхідна потужність для підтримки крейсерської швидкості: 310 Вт.",
                "prop_speed_explained": "Теоретична швидкість потоку повітря, створюваного гвинтом: 43.8 м/с.",
                "flight_time_explained": "Очікуваний час польоту для заданої конфігурації (електрична система): 1.8 год.",
            }
        }
