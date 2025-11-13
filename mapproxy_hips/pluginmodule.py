# SPDX-License-Identifier: MIT
# Copyright (C) 2021-2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

from mapproxy.config.configuration.source import register_source_configuration
from mapproxy.config.configuration.service import register_service_configuration
from mapproxy.config.spec import add_subcategory_to_layer_md
from mapproxy.util.ext.dictspec.spec import anything
from mapproxy.script.util import register_command
from mapproxy.service.demo import register_extra_demo_server_handler, register_extra_demo_substitution_handler

from mapproxy_hips.config.hips_source_configuration import HIPSSourceConfiguration, hips_source_yaml_spec
from mapproxy_hips.config.hips_service_configuration import hips_service_creator, hips_service_yaml_spec, hips_service_json_schema
from mapproxy_hips.script.hipsallsky import hipsallsky_command
from mapproxy_hips.script.hipsseed import hipsseed_command
from mapproxy_hips.service.demo_extra import extra_demo_server_handler, extra_demo_substitution_handler

import inspect
import logging
import os

already_executed = False

log = logging.getLogger('mapproxy.hips')
log.setLevel(logging.INFO)

def register_opentelemetry():
    from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
    from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
    from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
    import sys

    class SafeLoggingHandler(LoggingHandler):
        def flush(self):
            if getattr(sys, "is_finalizing", lambda: False)():
                return
            try:
                super().flush()
            except Exception:
                pass

    log_exporter = OTLPLogExporter()
    log_provider = LoggerProvider()
    log_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))
    otel_handler = SafeLoggingHandler(logger_provider=log_provider)
    log.addHandler(otel_handler)
    return otel_handler


def plugin_entrypoint():
    """ Entry point of the plugin, called by mapproxy """

    global already_executed
    if already_executed:
        return
    already_executed = True

    otel_handler = None
    if "OTEL_EXPORTER_OTLP_ENDPOINT" in os.environ:
        if "OTEL_SERVICE_NAME" not in os.environ:
            os.environ["OTEL_SERVICE_NAME"] = "mapproxy.hips"
        otel_handler = register_opentelemetry()

    log.info('execute plugin_entrypoint')
    if otel_handler:
        otel_handler.flush()

    register_source_configuration('hips', HIPSSourceConfiguration,
                                  'hips', hips_source_yaml_spec())

    sig = inspect.signature(register_service_configuration).parameters
    if 'schema_service' in sig:
        # mapproxy > 6.0.1
        register_service_configuration('hips', hips_service_creator,
                                       'hips', hips_service_yaml_spec(),
                                       hips_service_json_schema())
    else:
        register_service_configuration('hips', hips_service_creator,
                                       'hips', hips_service_yaml_spec())

    # Add a 'hips' subcategory to layer spec to be able to define hips service
    # specific layer metadata
    add_subcategory_to_layer_md('hips', anything())

    # Register command line utilities as sub-commands of mapproxy-util
    register_command('hips-allsky', {
        'func': hipsallsky_command,
        'help': 'Generate HIPS allsky preview file.'
    })
    register_command('hips-seed', {
        'func': hipsseed_command,
        'help': 'Pre-generate HIPS tiles.'
    })

    register_extra_demo_server_handler(extra_demo_server_handler)
    register_extra_demo_substitution_handler(extra_demo_substitution_handler)
