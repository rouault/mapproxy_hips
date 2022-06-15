# SPDX-License-Identifier: MIT
# Copyright (C) 2021-2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

import pkg_resources
from mapproxy.service.demo import get_template as mapproxy_get_template
from mapproxy.template import template_loader

mapproxy_hips_get_template = template_loader(__name__, 'templates')

def extra_demo_server_handler(demo_server, req):

    """ Called by mapproxy when an incoming request comes to the /demo service """

    if 'hips_layer' in req.args:
        return _render_hips_layer_template(req)
    return None


def extra_demo_substitution_handler(demo_server, req, substitutions):

    """ Called by mapproxy when rendering the /demo main HTML page """

    if 'hips' in demo_server.services:
        hips_layer_names = []
        for layer_name, layer in demo_server.layers.items():
            hips_md = layer.md.get('hips', None)
            if hips_md is None:
                hips_md = {}
            enabled = hips_md.get('enabled', True)
            if enabled:
                _, _, _, allsky_available, _ = _hips_info(req, layer_name)
                hips_layer_names.append([layer_name, allsky_available])

        template = mapproxy_hips_get_template('demo/demo_hips_template.html')
        hips_html = template.substitute(hips_layer_names=hips_layer_names)
        substitutions['extra_services_html_beginning'] += hips_html


def _hips_info(req, layer_name):
    hips_internal_url = req.server_script_url + '/hips/' + layer_name

    hips_order_max = 5
    hips_tile_format = 'png'
    hips_frame = 'planet'

    # Download the /properties document to get a few metadata we
    # need: hips_order_max, hips_tile_format and hips_frame
    from mapproxy.client.http import HTTPClient, HTTPClientError
    resp = HTTPClient(hips_internal_url).open(hips_internal_url + "/properties")

    from mapproxy_hips.util.hips import parse_properties

    properties = parse_properties(resp.read().decode('utf-8'))
    if 'hips_order' in properties: # Mandatory element
        hips_order_max = int(properties['hips_order'])

    if 'hips_tile_format' in properties: # Mandatory element
        tile_format = None
        value = properties['hips_tile_format']
        for x in value.split(' '):
            if x in ('jpeg', 'png'):
                tile_format = 'png' if x == 'png' else 'jpg'
                break
        if tile_format is None:
            return Exception(f'hips_tile_format = {value} does not contain jpeg or png')
        hips_tile_format = tile_format

    if 'hips_frame' in properties:
        hips_frame = properties['hips_frame']

    # Check if the /Norder3/Allsky.png/.jpg file is already pregenerated.
    try:
        allsky_ext = 'png' if hips_tile_format == 'png' else 'jpg'
        allsky_file = hips_internal_url + "/Norder3/Allsky." + allsky_ext
        HTTPClient(hips_internal_url).open(allsky_file, method='HEAD')
        allsky_available = True
    except HTTPClientError:
        allsky_available = False

    return hips_order_max, hips_tile_format, hips_frame, allsky_available, allsky_file


def _render_hips_layer_template(req):

    hips_layer = req.args['hips_layer']
    hips_url = req.script_url + '/hips/' + hips_layer

    hips_order_max, hips_tile_format, hips_frame, allsky_available, allsky_file = _hips_info(req, hips_layer)

    allsky_msg = ''
    if not allsky_available:
        allsky_msg = f'<p><b>WARNING</b>: {allsky_file} does not exist. It should be pregenerated with "mapproxy-util hips-allsky -f path_to_mapproxy.yaml -l {hips_layer} -o 3 -c $(nproc)"</p>'

    template_filename = pkg_resources.resource_filename(__name__, 'templates/demo/hips_demo.html')
    # We use mapproxy_get_template() and not mapproxy_hips_get_template()
    # because demo/static.html is a resource of mapproxy, and not mapproxy_hips
    template = mapproxy_get_template(template_filename, default_inherit="demo/static.html")
    return template.substitute(hips_url=hips_url,
                               hips_layer=hips_layer,
                               hips_frame=hips_frame,
                               hips_order_max=hips_order_max,
                               hips_tile_format=hips_tile_format,
                               allsky_msg=allsky_msg)
