from pydantic import AfterValidator, BaseModel, field_serializer
from enum import Enum
from typing import Optional
from typing_extensions import Annotated


def int_to_float_10(input: Optional[int]):
    return int_to_float(input, 10)

def int_to_float(input: Optional[int], divider: int) -> Optional[float]:
    if input is None:
        return input
    return input / divider

def float_to_int_10(input: Optional[float]) -> Optional[int]:
    return float_to_int(input, 10)

def float_to_int(input: Optional[float], multiplier: int) -> Optional[int]:
    if input is None:
        return input
    return int(input * multiplier)

def int_to_bool(input: Optional[int]) -> Optional[bool]:
    if input is None:
        return input
    if input > 1 or input < 0:
        raise ValueError("Value must be either 0 or 1")
    return input == 1

class ThermostatStatus(BaseModel):
    DEVICE_ID: str
    HW_VERSION: str
    FW_VERSION: str
    TEMP_AIR: Annotated[float, AfterValidator(int_to_float_10)]
    HUM_AIR: Annotated[float, AfterValidator(int_to_float_10)]
    TEMP_FLOOR: Annotated[float, AfterValidator(int_to_float_10)]
    CO2: int
    AQI: int
    DEVICE_UPTIME: int
    HEATING_UPTIME: int
    ERRORS: int
    SETPOINT_TEMP: Annotated[float, AfterValidator(int_to_float_10)]
    WINDOW_OPEN_DETECTED: Annotated[bool, AfterValidator(int_to_bool)]
    HEATING_ON: Annotated[bool, AfterValidator(int_to_bool)]


class WorkingMode(Enum):
    HOME=1
    AWAY=2


class ThermostatSettings(BaseModel):
    DEVICE_ID: str
    MODE: WorkingMode
    SETPOINT_TEMP: Annotated[float, AfterValidator(int_to_float_10)]
    SETPOINT_TEMP_AWAY: Annotated[float, AfterValidator(int_to_float_10)]
    HYSTERESIS_BAND: Annotated[float, AfterValidator(int_to_float_10)]
    DEVICE_NAME: str
    REBOOT: Annotated[bool, AfterValidator(int_to_bool)]
    ACTUATOR_EXERCISE_DISABLED: Annotated[bool, AfterValidator(int_to_bool)]
    RECALIBRATE_CO2: Annotated[bool, AfterValidator(int_to_bool)]
    CHILDLOCK_ENABLED: Annotated[bool, AfterValidator(int_to_bool)]
    BOOST_ENABLED: Annotated[bool, AfterValidator(int_to_bool)]

def hysteresis_validate(input: float) -> float:
    if input > 5.0 or input < -5.0:
        raise ValueError("Input must be between -5.0 and 5.0")
    
    return input

class ThermostatSettingsUpdateInput(BaseModel):
    MODE: Optional[WorkingMode] = None
    SETPOINT_TEMP: Optional[float] = None
    SETPOINT_TEMP_AWAY: Optional[float] = None
    HYSTERESIS_BAND: Annotated[Optional[float], AfterValidator(hysteresis_validate)] = None
    DEVICE_NAME: Optional[str] = None
    REBOOT: Optional[bool] = None
    ACTUATOR_EXERCISE_DISABLED: Optional[bool] = None
    RECALIBRATE_CO2: Optional[bool] = None
    CHILDLOCK_ENABLED: Optional[bool] = None
    BOOST_ENABLED: Optional[bool] = None

    @field_serializer('MODE')
    def serialize_mode(self, mode: Optional[WorkingMode], _info):
        if mode is None:
            return mode
        return mode.value
    
    @field_serializer('SETPOINT_TEMP')
    def serialize_setpoint(self, setpoint: Optional[float], _info):
        if setpoint is None:
            return setpoint
        return int(setpoint * 10)
    
    @field_serializer('SETPOINT_TEMP_AWAY')
    def serialize_setpoint_away(self, setpoint: Optional[float], _info):
        if setpoint is None:
            return setpoint
        return int(setpoint * 10)
    
    @field_serializer('HYSTERESIS_BAND')
    def serialize_hysteresis(self, hysteresis: Optional[float], _info):
        if hysteresis is None:
            return hysteresis
        return int(hysteresis * 10)
    
    @field_serializer('REBOOT')
    def serialize_reboot(self, reboot: Optional[bool], _info):
        if reboot is None:
            return reboot
        return 1 if reboot else 0
    
    @field_serializer('ACTUATOR_EXERCISE_DISABLED')
    def serialize_actuator(self, actuator: Optional[bool], _info):
        if actuator is None:
            return actuator
        return 1 if actuator else 0
    
    @field_serializer('RECALIBRATE_CO2')
    def serialize_co2_cal(self, co2_cal: Optional[bool], _info):
        if co2_cal is None:
            return co2_cal
        return 1 if co2_cal else 0
    
    @field_serializer('CHILDLOCK_ENABLED')
    def serialize_child_lock(self, child_lock: Optional[bool], _info):
        if child_lock is None:
            return child_lock
        return 1 if child_lock else 0
    
    @field_serializer('BOOST_ENABLED')
    def serialize_boost(self, boost: Optional[bool], _info):
        if boost is None:
            return boost
        return 1 if boost else 0


class ThermostatSettingsUpdateResponse(BaseModel):
    MODE: Optional[WorkingMode] = None
    SETPOINT_TEMP: Annotated[Optional[float], AfterValidator(int_to_float_10)] = None
    SETPOINT_TEMP_AWAY: Annotated[Optional[float], AfterValidator(int_to_float_10)] = None
    HYSTERESIS_BAND: Annotated[Optional[float], AfterValidator(int_to_float_10)] = None
    DEVICE_NAME: Optional[str] = None
    REBOOT: Annotated[Optional[bool], AfterValidator(int_to_bool)] = None
    ACTUATOR_EXERCISE_DISABLED: Annotated[Optional[bool], AfterValidator(int_to_bool)] = None
    RECALIBRATE_CO2: Annotated[Optional[bool], AfterValidator(int_to_bool)] = None
    CHILDLOCK_ENABLED: Annotated[Optional[bool], AfterValidator(int_to_bool)] = None
    BOOST_ENABLED: Annotated[Optional[bool], AfterValidator(int_to_bool)] = None