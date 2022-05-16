# SPDX-License-Identifier: MIT
# Copyright (C) 2021-2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

def hips_service_creator(serviceConfiguration, conf):
    from mapproxy_hips.service.hips import HIPSServer
    root_layer = serviceConfiguration.context.wms_root_layer.wms_layer()
    tile_layers = serviceConfiguration.tile_layers(conf)
    resampling_method = conf.get('resampling_method', 'bicubic')
    if resampling_method not in ('nearest_neighbour', 'bilinear', 'bicubic'):
        raise ValueError(f'unsupported resampling_method = {resampling_method}')
    cache_dir = serviceConfiguration.context.globals.get_path('cache.base_dir', conf)
    lock_dir = serviceConfiguration.context.globals.get_path('cache.lock_dir', conf)
    timeout = serviceConfiguration.context.globals.get_value('http.client_timeout', conf)
    populate_cache = conf.get('populate_cache', True)
    return HIPSServer(cache_dir, lock_dir, timeout, populate_cache,
                      root_layer, tile_layers, resampling_method)


def hips_service_yaml_spec():
    spec = {
        'resampling_method': str(),
    }
    return spec
