# SPDX-License-Identifier: MIT
# Copyright (C) 2021-2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

import os

from mapproxy.config.loader import SourceConfiguration
from mapproxy.config.spec import image_opts
from mapproxy.util.ext.dictspec.spec import required
from mapproxy.util.py import memoize

import logging
log = logging.getLogger('mapproxy.hips')

class HIPSSourceConfiguration(SourceConfiguration):
    source_type = ('hips',)

    @memoize
    def cache_dir(self):
        cache_dir = self.conf.get('cache', {}).get('directory')
        if cache_dir:
            if self.conf.get('cache_dir'):
                log.warning('found cache.directory and cache_dir option for %s, ignoring cache_dir',
                self.conf['name'])
            return self.context.globals.abspath(cache_dir)

        return self.context.globals.get_path('cache_dir', self.conf,
            global_key='cache.base_dir')

    def lock_dir(self):
        lock_dir = self.context.globals.get_path('cache.tile_lock_dir', self.conf)
        if not lock_dir:
            lock_dir = os.path.join(self.cache_dir(), 'tile_locks')
        return lock_dir

    def source(self, params=None):
        from mapproxy_hips.source.hips import HIPSSource

        url = self.conf['url']
        http_client, url = self.http_client(url)

        coverage = self.coverage()
        image_opts = self.image_opts()

        resampling_method = self.conf.get('resampling_method', 'bicubic')
        if resampling_method not in ('nearest_neighbour', 'bilinear', 'bicubic'):
            raise ValueError(f'unsupported resampling_method = {resampling_method}')

        source = HIPSSource(http_client, url, resampling_method, coverage=coverage, image_opts=image_opts)

        cache_hips_tiles = self.conf.get('cache_hips_tiles', True)
        if cache_hips_tiles:
            from mapproxy.cache.base import TileLocker
            from mapproxy.cache.file import FileCache

            cache_dir = os.path.join(self.cache_dir(), self.conf['name'], 'hips_tiles')
            cache = FileCache(cache_dir, 'jpg' if source.hips_tile_format == 'jpeg' else 'png')

            lock_timeout = self.context.globals.get_value('http.client_timeout', {})
            lock_cache_id = cache.lock_cache_id
            locker = TileLocker(self.lock_dir(), lock_timeout, lock_cache_id)

            source.locker = locker
            source.cache = cache

        return source


def hips_source_yaml_spec():
    """ Chunk to add to mapproxy.config.spec.mapproxy_yaml_spec under the ["sources"]["hips"]
        node to validate HIPS sources in a mapproxy.yml file """
    spec = {
        required('url'): str(),
        'resampling_method': str(),
        'image': image_opts,
    }
    return spec
