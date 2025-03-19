from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Literal, Optional

from kelvin.config.common import AppBaseConfig, AppTypes, ConfigBaseModel, ConfigError, read_schema_file
from kelvin.message import ParameterType
from kelvin.message.msg_type import PrimitiveTypes

from .manifest import (
    AppDefaults,
    AppManifest,
    DefaultsDefinition,
    Flags,
    IODatastreamMapping,
    IODefinition,
    IOWay,
    ParamDefinition,
    RuntimeUpdateFlags,
    SchemasDefinition,
)


class RuntimeUpdateConfig(ConfigBaseModel):
    configuration: bool = False
    resources: bool = False
    parameters: bool = True
    resource_properties: bool = True


class SmartAppFlags(ConfigBaseModel):
    enable_runtime_update: RuntimeUpdateConfig = RuntimeUpdateConfig()


class IOConfig(ConfigBaseModel):
    name: str
    data_type: str
    unit: Optional[str] = None


class DataIo(ConfigBaseModel):
    inputs: List[IOConfig] = []
    outputs: List[IOConfig] = []


class SmartAppParams(ConfigBaseModel):
    name: str
    data_type: Literal[PrimitiveTypes.number, PrimitiveTypes.string, PrimitiveTypes.boolean]


class SchemasConfig(ConfigBaseModel):
    configuration: Optional[str] = None
    parameters: Optional[str] = None


class DatastreamMapping(ConfigBaseModel):
    app: str
    datastream: str


class DeploymentDefaults(ConfigBaseModel):
    system: Dict = {}
    datastream_mapping: List[DatastreamMapping] = []
    configuration: Dict = {}
    parameters: Dict[str, ParameterType] = {}


class SmartAppConfig(AppBaseConfig):
    type: Literal[AppTypes.app]
    spec_version: str = "5.0.0"

    flags: SmartAppFlags = SmartAppFlags()
    data_streams: DataIo = DataIo()
    control_changes: DataIo = DataIo()
    parameters: List[SmartAppParams] = []
    ui_schemas: SchemasConfig = SchemasConfig()
    defaults: DeploymentDefaults = DeploymentDefaults()

    def to_manifest(self, read_schemas: bool = True, workdir: Path = Path(".")) -> AppManifest:
        return convert_smart_app_to_manifest(self, read_schemas=read_schemas, workdir=workdir)


def convert_smart_app_to_manifest(
    config: SmartAppConfig, read_schemas: bool = True, workdir: Path = Path(".")
) -> AppManifest:
    ios_map: Dict[str, IODefinition] = {}

    for io in config.data_streams.inputs:
        ios_map[io.name] = IODefinition(name=io.name, data_type=io.data_type, way=IOWay.input, unit=io.unit)

    for io in config.data_streams.outputs:
        if io.name in ios_map:
            raise ConfigError(f"IO {io.name} is defined as input and output")
        ios_map[io.name] = IODefinition(name=io.name, data_type=io.data_type, way=IOWay.output, unit=io.unit)

    for io in config.control_changes.inputs:
        io_exist = ios_map.get(io.name)
        if not io_exist:
            ios_map[io.name] = IODefinition(name=io.name, data_type=io.data_type, way=IOWay.input_cc, unit=io.unit)
            continue

        if io_exist.data_type != io.data_type:
            raise ConfigError(f"IO {io.name} has different data type in data streams and control changes")

        if io_exist.unit != io.unit:
            raise ConfigError(f"IO {io.name} has different unit in data streams and control changes")

        if io_exist.way == IOWay.input:
            raise ConfigError(f"IO {io.name} is defined as input and input control changes")

        if io_exist.way != IOWay.output:
            raise ConfigError(f"Unexpected configuration of IO {io.name} way. Previous way: {io_exist.way}")

        io_exist.way = IOWay.input_cc_output

    for io in config.control_changes.outputs:
        io_exist = ios_map.get(io.name)
        if not io_exist:
            ios_map[io.name] = IODefinition(name=io.name, data_type=io.data_type, way=IOWay.output_cc, unit=io.unit)
            continue

        if io_exist.data_type != io.data_type:
            raise ConfigError(f"IO {io.name} has different data type in data streams and control changes")

        if io_exist.unit != io.unit:
            raise ConfigError(f"IO {io.name} has different unit in data streams and control changes")

        if io_exist.way == IOWay.output:
            raise ConfigError(f"IO {io.name} is defined as output and output control changes")

        if io_exist.way != IOWay.input:
            raise ConfigError(f"Unexpected configuration of IO {io.name} way. Previous way: {io_exist.way}")

        io_exist.way = IOWay.input_output_cc

    io_map = [
        IODatastreamMapping(io=smart_io.app, datastream=smart_io.datastream)
        for smart_io in config.defaults.datastream_mapping
    ]

    schemas = SchemasDefinition()
    if read_schemas:
        schemas.configuration = (
            read_schema_file(workdir / config.ui_schemas.configuration) if config.ui_schemas.configuration else {}
        )
        schemas.parameters = (
            read_schema_file(workdir / config.ui_schemas.parameters) if config.ui_schemas.parameters else {}
        )

    return AppManifest(
        name=config.name,
        title=config.title,
        description=config.description,
        type=config.type,
        version=config.version,
        category=config.category,
        flags=Flags(
            spec_version=config.spec_version,
            enable_runtime_update=RuntimeUpdateFlags(
                io=config.flags.enable_runtime_update.resources,
                resource_parameters=config.flags.enable_runtime_update.parameters,
                resource_properties=config.flags.enable_runtime_update.resource_properties,
                configuration=config.flags.enable_runtime_update.configuration,
            ),
        ),
        parameters=[
            ParamDefinition(name=p.name, data_type=p.data_type, default=config.defaults.parameters.get(p.name))
            for p in config.parameters
        ],
        io=list(ios_map.values()),
        schemas=schemas,
        defaults=DefaultsDefinition(
            app=AppDefaults(configuration=config.defaults.configuration, io_datastream_mapping=io_map),
            system=config.defaults.system,
        ),
    )
