#! /usr/bin/env python

import os

import time
import logging
import csv
import networkx as nx
from node2vec import Node2Vec
from cellmaps_utils import constants
from cellmaps_utils import logutils
from cellmaps_utils.provenance import ProvenanceUtil

import cellmaps_ppi_embedding
from cellmaps_ppi_embedding.exceptions import CellMapsPPIEmbeddingError


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
            raise CellMapsPPIEmbeddingError('network is None')

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


class CellMapsPPIEmbedder(object):
    """
    Class to run algorithm
    """
    def __init__(self, outdir=None,
                 embedding_generator=None,
                 skip_logging=False,
                 name=cellmaps_ppi_embedding.__name__,
                 organization_name=None,
                 project_name=None,
                 provenance_utils=ProvenanceUtil(),
                 input_data_dict=None):
        """

        :param skip_logging:
        :param misc_info_dict:
        """
        if outdir is None:
            raise CellMapsPPIEmbeddingError('outdir is None')

        self._outdir = os.path.abspath(outdir)
        self._start_time = int(time.time())
        self._end_time = -1
        self._input_data_dict = input_data_dict
        self._embedding_generator = embedding_generator
        self._name = name
        self._project_name = project_name
        self._organization_name = organization_name
        self._input_data_dict = input_data_dict
        self._provenance_utils = provenance_utils
        if skip_logging is None:
            self._skip_logging = False
        else:
            self._skip_logging = skip_logging

        logger.debug('In constructor')

    @staticmethod
    def get_apms_edgelist_file(input_dir=None,
                               edgelist_filename=constants.PPI_EDGELIST_FILE):
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
        logutils.write_task_start_json(outdir=self._outdir,
                                       start_time=self._start_time,
                                       version=cellmaps_ppi_embedding.__version__,
                                       data={'commandlineargs': self._input_data_dict})

    def _create_run_crate(self):
        """
        Creates rocrate for output directory

        :raises CellMapsProvenanceError: If there is an error
        """
        name = self._name
        if name is None:
            name = 'TODO better set this via input rocrate'

        # TODO: If organization or project name is unset need to pull from input rocrate
        org_name = self._organization_name
        if org_name is None:
            org_name = 'TODO BETTER SET THIS via input rocrate'

        proj_name = self._project_name
        if proj_name is None:
            proj_name = 'TODO BETTER SET THIS via input rocrate'
        try:
            self._provenance_utils.register_rocrate(self._outdir,
                                                    name=name,
                                                    organization_name=org_name,
                                                    project_name=proj_name)
        except TypeError as te:
            raise CellMapsPPIEmbeddingError('Invalid provenance: ' + str(te))
        except KeyError as ke:
            raise CellMapsPPIEmbeddingError('Key missing in provenance: ' + str(ke))

    def _register_software(self):
        """
        Registers this tool

        :raises CellMapsImageEmbeddingError: If fairscape call fails
        """
        self._softwareid = self._provenance_utils.register_software(self._outdir,
                                                                    name=self._name,
                                                                    description=cellmaps_ppi_embedding.__description__,
                                                                    author=cellmaps_ppi_embedding.__author__,
                                                                    version=cellmaps_ppi_embedding.__version__,
                                                                    file_format='.py',
                                                                    url=cellmaps_ppi_embedding.__repo_url__)

    def _register_computation(self):
        """
        # Todo: added inused dataset, software and what is being generated
        :return:
        """
        self._provenance_utils.register_computation(self._outdir,
                                                    name=cellmaps_ppi_embedding.__name__ + ' computation',
                                                    run_by=str(os.getlogin()),
                                                    command=str(self._input_data_dict),
                                                    description='run of ' + cellmaps_ppi_embedding.__name__,
                                                    used_software=[self._softwareid])
                                                    #used_dataset=[self._unique_datasetid, self._samples_datasetid],
                                                    #generated=[self._image_gene_attrid])

    def run(self):
        """
        Run node2vec to create embeddings


        :return:
        """
        logger.debug('In run method')
        exitcode = 99
        try:
            if not os.path.isdir(self._outdir):
                os.makedirs(self._outdir, mode=0o755)

            if self._skip_logging is False:
                logutils.setup_filelogger(outdir=self._outdir,
                                          handlerprefix='cellmaps_ppi_embedding')
                self._write_task_start_json()

            self._create_run_crate()

            # Todo: uncomment when fixed
            # register software fails due to this bug:
            # https://github.com/fairscape/fairscape-cli/issues/7
            # self._register_software()

            with open(os.path.join(self._outdir, constants.PPI_EMBEDDING_FILE), 'w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                header_line = ['']
                header_line.extend([x for x in range(1, self._embedding_generator.get_dimensions())])
                writer.writerow(header_line)
                for row in self._embedding_generator.get_next_embedding():
                    writer.writerow(row)

            # Todo: uncomment when above work
            # Above registrations need to work for this to work
            # register computation
            # self._register_computation()

            exitcode = 0

        finally:
            self._end_time = int(time.time())
            if self._skip_logging is False:
                # write a task finish file
                logutils.write_task_finish_json(outdir=self._outdir,
                                                start_time=self._start_time,
                                                end_time=self._end_time,
                                                status=exitcode)
        return exitcode
