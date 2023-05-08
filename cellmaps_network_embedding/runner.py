#! /usr/bin/env python

import os

import time
import logging
import csv
import networkx as nx
from node2vec import Node2Vec
import cellmaps_network_embedding
from cellmaps_utils import logutils
from cellmaps_network_embedding.exceptions import CellMapsNetworkEmbeddingError


logger = logging.getLogger(__name__)


class EmbeddingGenerator(object):
    """
    Base class for implementations that generate
    network embeddings
    """
    def __init__(self, dimensions=1024):
        """
        Constructor
        """
        self._dimensions = dimensions

    def get_dimensions(self):
        """
        Gets number of dimensions this embedding will generate

        :return: number of dimensions aka vector length
        :rtype: int
        """
        return self._dimensions

    def get_next_embedding(self):
        """
        Generator method for getting next embedding.
        Caller should implement with ``yield`` operator

        :raises: NotImplementedError: Subclasses should implement this
        :return: Embedding
        :rtype: list
        """
        raise NotImplementedError('Subclasses should implement')


class Node2VecEmbeddingGenerator(EmbeddingGenerator):
    """

    """
    def __init__(self, nx_network, p=2, q=1, dimensions=1024,
                 walk_length=80, num_walks=80, workers=8):
        """
        Constructor
        """
        super().__init__(dimensions=dimensions)
        self._nx_network = nx_network
        self._p = p
        self._q = q
        self._walk_length = walk_length
        self._num_walks = num_walks
        self._workers = workers

    def _remove_header_edge_from_network(self):
        """
        Removes edge named geneA geneB which is actually the
        header of the edge list file

        """
        # remove geneA geneB edge cause it is the header of file
        try:
            self._nx_network.remove_edge('geneA', 'geneB')
        except nx.NetworkXError as ne:
            logger.debug('No edge named geneA -> geneB to remove' + str(ne))

        self._nx_network.remove_nodes_from(['geneA', 'geneB'])

    def get_next_embedding(self):
        """

        :return:
        """
        if self._nx_network is None:
            raise CellMapsNetworkEmbeddingError('network is None')

        self._remove_header_edge_from_network()

        n2v_obj = Node2Vec(self._nx_network, dimensions=self._dimensions,
                           walk_length=self._walk_length,
                           num_walks=self._num_walks,
                           workers=self._workers, q=self._q, p=self._p)

        # Embed nodes
        model = n2v_obj.fit(window=10, min_count=0, sg=1, epochs=1)
        for key in model.wv.index_to_key:
            row = [key]
            row.extend(model.wv[key].tolist())
            yield row


class CellMapsNetworkEmbeddingRunner(object):
    """
    Class to run algorithm
    """
    def __init__(self, outdir=None,
                 embedding_generator=None,
                 skip_logging=False,
                 misc_info_dict=None):
        """

        :param skip_logging:
        :param misc_info_dict:
        """
        self._start_time = int(time.time())
        self._end_time = -1
        self._misc_info_dict = misc_info_dict
        self._outdir = outdir
        self._embedding_generator = embedding_generator

        if skip_logging is None:
            self._skip_logging = False
        else:
            self._skip_logging = skip_logging

        logger.debug('In constructor')

    @staticmethod
    def get_apms_edgelist_file(input_dir=None,
                               edgelist_filename='ppi_edgelist.tsv'):
        """

        :param input_dir:
        :return:
        """
        return os.path.join(input_dir, edgelist_filename)

    def _write_task_start_json(self):
        """
        Writes task_start.json file with information about
        what is to be run

        """
        data = {}

        if self._misc_info_dict is not None:
            data.update(self._misc_info_dict)

        logutils.write_task_start_json(outdir=self._outdir,
                                       start_time=self._start_time,
                                       version=cellmaps_network_embedding.__version__,
                                       data=data)

    def run(self):
        """
        Run node2vec to create embeddings


        :return:
        """
        logger.debug('In run method')
        try:
            exitcode = 99

            if self._outdir is None:
                raise CellMapsNetworkEmbeddingError('outdir must be set')

            if not os.path.isdir(self._outdir):
                os.makedirs(self._outdir, mode=0o755)

            if self._skip_logging is False:
                logutils.setup_filelogger(outdir=self._outdir,
                                          handlerprefix='cellmaps_network_embedding')
                self._write_task_start_json()

            with open(os.path.join(self._outdir, 'ppi_emd.tsv'), 'w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                header_line = ['']
                header_line.extend([x for x in range(1, self._embedding_generator.get_dimensions())])
                writer.writerow(header_line)
                for row in self._embedding_generator.get_next_embedding():
                    writer.writerow(row)

            exitcode = 0
            return exitcode
        finally:
            self._end_time = int(time.time())
            if self._skip_logging is False:
                # write a task finish file
                logutils.write_task_finish_json(outdir=self._outdir,
                                                start_time=self._start_time,
                                                end_time=self._end_time,
                                                status=exitcode)
