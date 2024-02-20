#! /usr/bin/env python

import os
import numpy as np
import time
from datetime import date
import logging
import csv
import networkx as nx
from node2vec import Node2Vec
from cellmaps_utils import constants
from cellmaps_utils import logutils
from cellmaps_utils.provenance import ProvenanceUtil
import warnings


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


class FakeEmbeddingGenerator(EmbeddingGenerator):
    """
    Fakes PPI embedding
    """
    def __init__(self, ppi_downloaddir,  dimensions=1024):
        """
        Constructor

        :param dimensions: Desired size of output embedding
        :type dimensions: int
        """
        super().__init__(dimensions=dimensions)

        self._ppi_downloaddir = ppi_downloaddir
        self._gene_list = self._get_gene_list()

        warnings.warn(constants.PPI_EMBEDDING_FILE +
                      ' contains FAKE DATA!!!!\n'
                      'You have been warned\nHave a nice day\n')
        logger.error(constants.PPI_EMBEDDING_FILE +
                     ' contains FAKE DATA!!!! '
                     'You have been warned. Have a nice day')

    def _get_gene_list(self):

        ppi_gene_node_attrs_file = os.path.join(self._ppi_downloaddir, constants.PPI_GENE_NODE_ATTR_FILE)
        gene_list = []

        with open(ppi_gene_node_attrs_file, 'r') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                gene_list.append(row['name'])
        return gene_list

    def get_next_embedding(self):
        """
        Generator method for getting next embedding.
        Caller should implement with ``yield`` operator

        :raises: NotImplementedError: Subclasses should implement this
        :return: Embedding
        :rtype: list
        """
        for g in self._gene_list:
            row = [g]
            row.extend(np.random.normal(size=self.get_dimensions())) # sample normal distribution
            yield row


class CellMapsPPIEmbedder(object):
    """
    Class to run algorithm
    """
    def __init__(self, outdir=None,
                 embedding_generator=None,
                 inputdir=None,
                 skip_logging=True,
                 name=None,
                 organization_name=None,
                 project_name=None,
                 provenance_utils=ProvenanceUtil(),
                 input_data_dict=None):
        """
        Constructor

        :param outdir: directory where ppi embeddings will be saved
        :type outdir: str
        :param embedding_generator
        :type embedding_generator
        :param inputdir
        :type inputdir: str
        :param skip_logging: If ``True`` skip logging, if ``None`` or ``False`` do NOT skip logging
        :type skip_logging: bool
        :param provenance:
        :type provenance: dict
        :param input_data_dict:
        :type input_data_dict: dict
        """
        if outdir is None:
            raise CellMapsPPIEmbeddingError('outdir is None')

        self._outdir = os.path.abspath(outdir)
        self._inputdir = inputdir
        self._start_time = int(time.time())
        self._end_time = -1
        self._input_data_dict = input_data_dict
        self._embedding_generator = embedding_generator
        self._name = name
        self._project_name = project_name
        self._organization_name = organization_name
        self._keywords = None
        self._description = None
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

    def _update_provenance_fields(self):
        """

        :return:
        """
        prov_attrs = self._provenance_utils.get_merged_rocrate_provenance_attrs(self._inputdir,
                                                                                override_name=self._name,
                                                                                override_project_name=self._project_name,
                                                                                override_organization_name=self._organization_name,
                                                                                extra_keywords=['AP-MS Embedding',
                                                                                                'AP-MS',
                                                                                                'embedding'])

        self._name = prov_attrs.get_name()
        self._organization_name = prov_attrs.get_organization_name()
        self._project_name = prov_attrs.get_project_name()
        self._keywords = prov_attrs.get_keywords()
        self._description = prov_attrs.get_description()

    def _create_run_crate(self):
        """
        Creates rocrate for output directory

        :raises CellMapsProvenanceError: If there is an error
        """
        logger.debug('Registering rocrate with FAIRSCAPE')

        try:
            self._provenance_utils.register_rocrate(self._outdir,
                                                    name=self._name,
                                                    organization_name=self._organization_name,
                                                    project_name=self._project_name,
                                                    description=self._description,
                                                    keywords=self._keywords)
        except TypeError as te:
            raise CellMapsPPIEmbeddingError('Invalid provenance: ' + str(te))
        except KeyError as ke:
            raise CellMapsPPIEmbeddingError('Key missing in provenance: ' + str(ke))

    def _register_software(self):
        """
        Registers this tool

        :raises CellMapsImageEmbeddingError: If fairscape call fails
        """
        logger.debug('Registering software with FAIRSCAPE')
        software_keywords = self._keywords
        software_keywords.extend(['tools', cellmaps_ppi_embedding.__name__])
        software_description = self._description + ' ' + \
                               cellmaps_ppi_embedding.__description__
        self._softwareid = self._provenance_utils.register_software(self._outdir,
                                                                    name=cellmaps_ppi_embedding.__name__,
                                                                    description=software_description,
                                                                    author=cellmaps_ppi_embedding.__author__,
                                                                    version=cellmaps_ppi_embedding.__version__,
                                                                    file_format='py',
                                                                    keywords=software_keywords,
                                                                    url=cellmaps_ppi_embedding.__repo_url__)

    def _register_computation(self):
        """
        # Todo: added in used dataset, software and what is being generated
        :return:
        """
        logger.debug('Getting id of input rocrate')
        input_dataset_id = self._provenance_utils.get_id_of_rocrate(self._inputdir)

        logger.debug('Registering computation with FAIRSCAPE')
        keywords = self._keywords
        keywords.extend(['computation'])
        description = self._description + ' run of ' + cellmaps_ppi_embedding.__name__
        self._provenance_utils.register_computation(self._outdir,
                                                    name=cellmaps_ppi_embedding.__computation_name__,
                                                    run_by=str(self._provenance_utils.get_login()),
                                                    command=str(self._input_data_dict),
                                                    description=description,
                                                    keywords=keywords,
                                                    used_software=[self._softwareid],
                                                    used_dataset=[input_dataset_id],
                                                    generated=[self._embedding_file_id])

    def _register_embedding_file(self):
        """
        Registers embedding file as a dataset

        :return: id of datafile dataset
        :rtype: str
        """
        logger.debug('Registering embedding file with FAIRSCAPE')
        description = self._description
        description += ' file'
        keywords = self._keywords
        keywords.extend(['file'])
        data_dict = {'name': cellmaps_ppi_embedding.__name__ + ' output file',
                     'description': description,
                     'keywords': keywords,
                     'data-format': 'tsv',
                     'author': cellmaps_ppi_embedding.__name__,
                     'version': cellmaps_ppi_embedding.__version__,
                     'schema': 'https://raw.githubusercontent.com/fairscape/cm4ai-schemas/main/v0.1.0/cm4ai_schema_apms_embedding.json',
                     'date-published': date.today().strftime(self._provenance_utils.get_default_date_format_str())}
        self._embedding_file_id = self._provenance_utils.register_dataset(self._outdir,
                                                                          source_file=self.get_ppi_embedding_file(),
                                                                          data_dict=data_dict)

    def get_ppi_embedding_file(self):
        """
        Gets PPI embedding file in output directory

        :return:
        :rtype: str
        """
        return os.path.join(self._outdir, constants.PPI_EMBEDDING_FILE)

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

            self._update_provenance_fields()

            self._create_run_crate()

            self._register_software()

            with open(self.get_ppi_embedding_file(), 'w', newline='') as f:
                writer = csv.writer(f, delimiter='\t')
                header_line = ['']
                header_line.extend([x for x in range(1, self._embedding_generator.get_dimensions())])
                writer.writerow(header_line)
                for row in self._embedding_generator.get_next_embedding():
                    writer.writerow(row)

            self._register_embedding_file()
            self._register_computation()

            exitcode = 0

        finally:
            self._end_time = int(time.time())
            # write a task finish file
            logutils.write_task_finish_json(outdir=self._outdir,
                                            start_time=self._start_time,
                                            end_time=self._end_time,
                                            status=exitcode)
        return exitcode
