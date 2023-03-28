#! /usr/bin/env python

import os
import csv
import random
import logging

from cellmaps_network_embedding.exceptions import CellMapsNetworkEmbeddingError


logger = logging.getLogger(__name__)


class CellMapsNetworkEmbeddingRunner(object):
    """
    Class to run algorithm
    """
    def __init__(self, edgelist=None,
                 outdir=None,
                 p=None,
                 q=None,
                 dimensions=1024):
        """
        Constructor

        :param exitcode: value to return via :py:meth:`.CellMapsNetworkEmbeddingRunner.run` method
        :type int:
        """
        self._edgelist = edgelist
        self._outdir = outdir
        self._dimensions = dimensions
        logger.debug('In constructor')

    def run(self):
        """
        Fake tool that generates fake embeddings


        :return:
        """
        logger.debug('In run method')

        if self._outdir is None:
            raise CellMapsNetworkEmbeddingError('outdir must be set')

        if not os.path.isdir(self._outdir):
            os.makedirs(self._outdir, mode=0o755)

        if self._edgelist is None:
            raise CellMapsNetworkEmbeddingError('edgelist must be set to a file')

        if not os.path.isfile(self._edgelist):
            raise CellMapsNetworkEmbeddingError('edgelist ' +
                                                str(self._edgelist) +
                                                ' is not a file')

        uniq_genes = set()
        with open(self._edgelist, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                uniq_genes.add(row['geneA'])
                uniq_genes.add(row['geneB'])

        with open(os.path.join(self._outdir, 'apms_emd.tsv'), 'w') as f:
            headerline = ['']
            for x in range(1, 1025):
                headerline.append(str(x))
            f.write('\t'.join(headerline) + '\n')
            for gene in uniq_genes:
                embedding = [gene]
                for cntr in range(self._dimensions):
                    embedding.append(str(random.random()))
                f.write('\t'.join(embedding) + '\n')

        return 0
