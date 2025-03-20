import requests
from urllib.parse import urljoin

from .models import ThermostatSettings, ThermostatStatus, ThermostatSettingsUpdateInput, ThermostatSettingsUpdateResponse


class AirobotAPI:
    username: str
    password: str
    thermostat_addr: str


    def __init__(self, addr: str, username: str, password: str):
        self.thermostat_addr = addr
        self.username = username
        self.password = password
    
    def authenticate(self) -> bool:
        settings_url = urljoin(self.thermostat_addr, "/api/thermostat/getSettings")
        res = requests.get(settings_url, auth=(self.username, self.password))
        
        return res.ok

    def get_settings(self) -> ThermostatSettings:
        settings_url = urljoin(self.thermostat_addr, "/api/thermostat/getSettings")
        res = requests.get(settings_url, auth=(self.username, self.password))
        
        res.raise_for_status()
        
        res_json = res.json()
        for flags in res_json["SETTING_FLAGS"]:
            for key, value in flags.items():
                res_json[key] = value

        return ThermostatSettings(**res_json)
    
    def set_settings(self, input: ThermostatSettingsUpdateInput) -> ThermostatSettingsUpdateResponse:
        settings_url = urljoin(self.thermostat_addr, "/api/thermostat/setSettings")

        inp = input.model_dump(exclude_defaults=True, exclude_unset=True)
        res = requests.post(settings_url, json=inp, auth=(self.username, self.password))

        res.raise_for_status()

        return ThermostatSettingsUpdateResponse(**res.json())
    
    def get_status(self) -> ThermostatStatus:
        statuses_url = urljoin(self.thermostat_addr, "/api/thermostat/getStatuses")
        res = requests.get(statuses_url, auth=(self.username, self.password))

        res.raise_for_status()

        res_json = res.json()
        for flags in res_json["STATUS_FLAGS"]:
            for key, value in flags.items():
                res_json[key] = value


        return ThermostatStatus(**res_json)
