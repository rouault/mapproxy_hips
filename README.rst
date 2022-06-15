mapproxy-hips
*************

mapproxy-hips is a plugin for MapProxy (http://mapproxy.github.io/mapproxy/) providing extensions
for interoperability between OGC services (WMS, WMTS, ...) and the HiPS protocol
(https://www.ivoa.net/documents/HiPS/) from IVOA.

The plugin requires MapProxy >= 1.15 which incorporates the plugin architecture
(http://mapproxy.github.io/mapproxy/plugins.html) used by mapproxy-hips.

Quickstart
----------

.. code-block:: shell

    python3 -m venv myvenv
    source myvenv/bin/activate
    pip install mapproxy_hips

    git clone https://github.com/rouault/mapproxy_hips
    mapproxy-util serve-develop mapproxy_hips/hips_examples/ogc_as_hips/mapproxy.yaml &
    curl http://localhost:8080/hips/mars_tiled_geodetic/properties

Adding a HIPS service
---------------------

Exposing a HIPS service (that is HIPS as output of MapProxy) requires to declare
a ``hips`` item under ``services`` in the MapProxy configuration file.

.. code-block:: yaml

    services:
      hips:
        #resampling_method: nearest_neighbour
        resampling_method: bilinear
        #resampling_method: bicubic
        # populate_cache: false

And you generally need to customize HIPS metadata for each exposed layer:

.. code-block:: yaml

    layers:
      - name: my_layer_name
        title: my title
        sources: [my_source]
        md:
            hips:
                # enabled: false
                creator_did: ivo://unknown.authority/some_id
                obs_title: Some title
                # foo: bar
                # hips_tile_width: 512
                # hips_order: 5

See https://github.com/rouault/mapproxy_hips/blob/master/hips_examples/ogc_as_hips/mapproxy.yaml
for a full example.

Utilities
---------

The ``hips-allsky`` command of the ``mapproxy-util`` script can be used to
generate the allsky file needed by some HIPS consumers.

.. code-block:: shell

    Usage: mapproxy-util hips-allsky [options] -f mapproxy_conf -l layer

    Options:
      -h, --help            show this help message and exit
      -f MAPPROXY_CONF, --mapproxy-conf=MAPPROXY_CONF
                            MapProxy configuration.
      -l LAYER, --layer=LAYER
                            Layer
      -o NORDER, --norder=NORDER
                            Order
      -c CONCURRENCY, --concurrency=CONCURRENCY
                            number of parallel processes



The ``hips-seed`` command of the ``mapproxy-util`` script can be used to
generate to pre-generate HIPS tiles.

.. code-block:: shell

    Usage: mapproxy-util hips-seed [options] -f mapproxy_conf -l layer

    Options:
      -h, --help            show this help message and exit
      -f MAPPROXY_CONF, --mapproxy-conf=MAPPROXY_CONF
                            MapProxy configuration.
      -l LAYER, --layer=LAYER
                            Layer
      -o NORDER, --norder=NORDER
                            Order
      -c CONCURRENCY, --concurrency=CONCURRENCY
                            number of parallel processes

Adding a HIPS source
--------------------

Adding a HIPS source (that is HIPS as input of MapProxy) requires to
specify ``type: hips`` in a source declaration, and specifying the URL and image format
of the HIPS service.

.. code-block:: yaml

    sources:
      mars_hips_source:
        type: hips
        image:
          format: image/jpeg
        resampling_method: bilinear
        url: http://alasky.u-strasbg.fr/Planets/Mars_MOLA
        # cache_hips_tiles: false

See https://github.com/rouault/mapproxy_hips/blob/master/hips_examples/hips_source/mapproxy.yaml
for a full example.

Credits
-------

Funded by Centre National d'Etudes Spatiales (CNES, https://cnes.fr) within the
framework of the "Pôle de Données et Services Surfaces Planétaires" (PDSSP) project.
