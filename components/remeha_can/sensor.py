import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import sensor
from esphome.const import CONF_ID
from . import RemehaCANComponent, CONF_REMEHACAN_ID, sensors_for_types

AUTO_LOAD = [ "remeha_can" ]

schema = { cv.GenerateID(CONF_REMEHACAN_ID): cv.use_id(RemehaCANComponent) }

for entry in sensors_for_types('U8', 'U16', 'U32', 'I8', 'I16', 'I32'):
    schema[cv.Optional(entry['name'])] = sensor.sensor_schema(
        unit_of_measurement = entry.get('unit', ''),
        accuracy_decimals   = 2,
    )

CONFIG_SCHEMA = cv.Schema(schema)

async def to_code(config):
    component = await cg.get_variable(config[CONF_REMEHACAN_ID])

    for name, conf in config.items():
        if not isinstance(conf, dict):
            continue
        id = conf[CONF_ID]
        if id and id.type == sensor.Sensor:
            sens = await sensor.new_sensor(conf)
            cg.add(component.add_sensor(name, sens))
            cg.add_define(f'rem_{name}') # enable OD entry in remeha-can-od-data.h
