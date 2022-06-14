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
    pip install git+https://github.com/rouault/mapproxy_hips

    git clone https://github.com/rouault/mapproxy_hips
    mapproxy-util serve-develop mapproxy_hips/hips_examples/ogc_as_hips/mapproxy.yaml &
    curl http://localhost:8080/hips/mars_tiled_geodetic/properties

Credits
-------

Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr
