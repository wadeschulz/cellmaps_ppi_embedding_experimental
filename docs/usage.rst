=====
Usage
=====

This page should provide information on how to use cellmaps_ppi_embedding

In a project
--------------

To use cellmaps_ppi_embedding in a project::

    import cellmaps_ppi_embedding

On the command line
---------------------

For information invoke :code:`cellmaps_ppi_embeddingcmd.py -h`

**Example usage**

The output directory for the PPI download is required (see `Cell Maps PPI Downloader <https://github.com/idekerlab/cellmaps_ppidownloader/>`__).

.. code-block::

   cellmaps_ppi_embeddingcmd.py ./cellmaps_ppi_embedding_outdir --inputdir ./cellmaps_ppidownloader_outdir 

Via Docker
---------------

**Example usage**


.. code-block::

   docker run -v `pwd`:`pwd` -w `pwd` idekerlab/cellmaps_ppi_embedding:0.1.0 cellmaps_ppi_embeddingcmd.py ./cellmaps_ppi_embedding_outdir --inputdir ./cellmaps_ppidownloader_outdir 


