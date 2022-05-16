# SPDX-License-Identifier: MIT
# Copyright (C) 2021-2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

from mapproxy.config.loader import register_source_configuration, register_service_configuration
from mapproxy.config.spec import add_subcategory_to_layer_md
from mapproxy.util.ext.dictspec.spec import anything
from mapproxy.script.util import register_command
from mapproxy.service.demo import register_extra_demo_server_handler, register_extra_demo_substitution_handler

from mapproxy_hips.config.hips_source_configuration import HIPSSourceConfiguration, hips_source_yaml_spec
from mapproxy_hips.config.hips_service_configuration import hips_service_creator, hips_service_yaml_spec
from mapproxy_hips.script.hipsallsky import hipsallsky_command
from mapproxy_hips.script.hipsseed import hipsseed_command
from mapproxy_hips.service.demo_extra import extra_demo_server_handler, extra_demo_substitution_handler

import logging
log = logging.getLogger('mapproxy.hips')

already_executed = False

def plugin_entrypoint():
    """ Entry point of the plugin, called by mapproxy """

    global already_executed
    if already_executed:
        return
    already_executed = True

    log.info('execute plugin_entrypoint')

    register_source_configuration('hips', HIPSSourceConfiguration,
                                  'hips', hips_source_yaml_spec())

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
