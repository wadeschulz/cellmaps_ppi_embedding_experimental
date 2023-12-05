=====
Usage
=====

The tool `cellmaps_ppi_embeddingcmd.py` provides functionalities for embedding protein-protein interactions (PPIs).
By default, it employs the Node2Vec algorithm for generating embeddings but can also produce fake embeddings for testing purposes.

In a project
--------------

To use cellmaps_ppi_embedding in a project::

    import cellmaps_ppi_embedding

On the command line
---------------------

For information invoke :code:`cellmaps_ppi_embeddingcmd.py -h`


**Usage**

.. code-block::

  cellmaps_ppi_embeddingcmd.py [outdir] [--inputdir PPIDOWNLOADER_OUT_DIR] [OPTIONS]

**Arguments**

- ``outdir``
    The directory where the output will be written to.

*Required*

- ``--inputdir``:
    Directory with the `ppi_edgelist.tsv` file. Output of the cellmaps_ppidownloader package.

*Optional*

- ``--dimensions``:
    The size of the embedding to generate. Default value is 1024.

- ``--walk_length``:
    The length of the walk for Node2Vec. Default is 80.

- ``--num_walks``:
    The number of walks for Node2Vec. Default is 10.

- ``--workers``:
    The number of worker threads to use. Default is 8.

- ``--p``:
    The p value to pass to Node2Vec. Default is 2.

- ``--q``:
    The q value to pass to Node2Vec. Default is 1.

- ``--fake_embedder``:
    If set, the script will generate a fake embedding.

- ``--skip_logging``:
    If set, certain log files will not be created.

- ``--logconf``:
    Path to the python logging configuration file.

- ``-v`` or ``--verbose``:
    Increases verbosity of the logger to standard error for log messages in the module. `-v` sets logging to ERROR, `-vv` to WARNING, `-vvv` to INFO, `-vvvv` to DEBUG, and `-vvvvv` to NOTSET.

- ``--version``:
    Displays the version of the script.

**Example usage**

The output directory for the PPI download is required (see `Cell Maps PPI Downloader <https://github.com/idekerlab/cellmaps_ppidownloader/>`__).

.. code-block::

   cellmaps_ppi_embeddingcmd.py ./cellmaps_ppi_embedding_outdir --inputdir ./cellmaps_ppidownloader_outdir

Via Docker
---------------

**Example usage**


.. code-block::

   Coming soon...

