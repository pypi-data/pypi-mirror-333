# Python Airobot API client

A simple Python API client for interacting with [Airobot smart thermostats](https://airobothome.com/en/smart-thermostat/). 

## Installing

Install with pip
```
pip install airobot_api_client
```

## Usage

There are two versions of the client available. Synchronous and asynchrounous.

### Sync version

```
from airobot_api_client.api import AirobotAPI
from airobot_api_client.models import ThermostatSettingsUpdateInput

api = AirobotAPI(<THERMOSTAT_IP>, <USERNAME>, <PASSWORD>)

settings = api.get_settings()
status = api.get_status()

new_settings = ThermostatSettingsUpdateInput(BOOST=True)
updated_settings = api.set_settings(new_settings)
```

### Async version

```
import asyncio
from airobot_api_client.async_api import AsyncAirobotAPI
from airobot_api_client.models import ThermostatSettingsUpdateInput

async def async_main():
    async with AsyncAirobotAPI(<THERMOSTAT_IP>, <USERNAME>, <PASSWORD>) as api:

        settings = await api.get_settings()
        status = await api.get_status()

        new_settings = ThermostatSettingsUpdateInput(BOOST=True)
        updated_settings = await api.set_settings(new_settings)

asyncio.run(async_main())
```