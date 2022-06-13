mapproxy-hips
*************

mapproxy-hips is a plugin for MapProxy (https://mapproxy.org/) providing extensions
for interoperability between OGC services (WMS, WMTS, ...) and the HiPS protocol
(https://www.ivoa.net/documents/HiPS/) from IVOA.

The plugin requires a mapproxy version from master repository (more recent than
2022-06-13) which incorporates the plugin architecture used by mapproxy-hips.

Quickstart
----------

.. code-block:: shell

    python3 -m venv myvenv
    source myvenv/bin/activate
    pip install git+https://github.com/mapproxy/mapproxy
    pip install git+https://github.com/rouault/mapproxy_hips

    git clone https://github.com/rouault/mapproxy_hips
    mapproxy-util serve-develop mapproxy_hips/hips_examples/ogc_as_hips/mapproxy.yaml &
    curl http://localhost:8080/hips/mars_tiled_geodetic/properties

Credits
-------

Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr
