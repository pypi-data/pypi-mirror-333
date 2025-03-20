from aiohttp import ClientSession, BasicAuth

from .models import ThermostatSettings, ThermostatStatus, ThermostatSettingsUpdateInput, ThermostatSettingsUpdateResponse


class AsyncAirobotAPI:
    session: ClientSession

    def __init__(self, addr: str, username: str, password: str):
        auth = BasicAuth(login=username, password=password)

        self.session = ClientSession(addr, auth=auth)
    
    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.session.close()

    async def authenticate(self) -> bool:
        async with self.session.get("/api/thermostat/getSettings") as res:
            return res.ok
    
    async def get_settings(self) -> ThermostatSettings:
        async with self.session.get("/api/thermostat/getSettings") as res:
            res.raise_for_status()
            res_json = await res.json()
            for flags in res_json["SETTING_FLAGS"]:
                for key, value in flags.items():
                    res_json[key] = value

            return ThermostatSettings(**res_json)
    
    async def set_settings(self, input: ThermostatSettingsUpdateInput) -> ThermostatSettingsUpdateResponse:
        inp = input.model_dump(exclude_defaults=True, exclude_unset=True)
        async with self.session.post("/api/thermostat/setSettings", json=inp) as res:
            res.raise_for_status()
            res_json = await res.json()
            return ThermostatSettingsUpdateResponse(**res_json)
    
    async def get_status(self) -> ThermostatStatus:
        async with self.session.get("/api/thermostat/getStatuses") as res:
            res.raise_for_status()
            res_json = await res.json()
            for flags in res_json["STATUS_FLAGS"]:
                for key, value in flags.items():
                    res_json[key] = value

            return ThermostatStatus(**res_json)
