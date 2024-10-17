#! /usr/bin/env python

import argparse
import json
import sys
import logging
import logging.config
import networkx as nx
from cellmaps_utils import logutils
from cellmaps_utils import constants
import cellmaps_ppi_embedding
from cellmaps_ppi_embedding.runner import Node2VecEmbeddingGenerator, EmbeddingGenerator
from cellmaps_ppi_embedding.runner import CellMapsPPIEmbedder
from cellmaps_ppi_embedding.runner import FakeEmbeddingGenerator

logger = logging.getLogger(__name__)


def _parse_arguments(desc, args):
    """
    Parses command line arguments

    :param desc: description to display on command line
    :type desc: str
    :param args: command line arguments usually :py:func:`sys.argv[1:]`
    :type args: list
    :return: arguments parsed by :py:mod:`argparse`
    :rtype: :py:class:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(description=desc,
                                     formatter_class=constants.ArgParseFormatter)
    parser.add_argument('outdir', help='Output directory')
    parser.add_argument('--inputdir', required=True,
                        help='Directory where ppi_edgelist.tsv file resides')
    parser.add_argument('--dimensions', type=int, default=EmbeddingGenerator.DIMENSIONS,
                        help='Size of embedding to generate')
    parser.add_argument('--walk_length', type=int, default=Node2VecEmbeddingGenerator.WALK_LENGTH,
                        help='Walk Length')
    parser.add_argument('--num_walks', type=int, default=Node2VecEmbeddingGenerator.NUM_WALKS,
                        help='Num walks')
    parser.add_argument('--workers', type=int, default=Node2VecEmbeddingGenerator.WORKERS,
                        help='Number of workers')
    parser.add_argument('--p', type=int, default=Node2VecEmbeddingGenerator.P_DEFAULT,
                        help='--p value to pass to node2vec')
    parser.add_argument('--q', type=int, default=Node2VecEmbeddingGenerator.Q_DEFAULT,
                        help='--q value to pass to node2vec')
    parser.add_argument('--fake_embedder', action='store_true',
                        help='If set, generate fake embedding')
    parser.add_argument('--provenance',
                        help='Path to file containing provenance '
                             'information about input files in JSON format. '
                             'This is required if inputdir does not contain '
                             'ro-crate-metadata.json file.')
    parser.add_argument('--name',
                        help='Name of this run, needed for FAIRSCAPE. If '
                             'unset, name value from specified '
                             'by --inputdir directory or provenance file will be used')
    parser.add_argument('--organization_name',
                        help='Name of organization running this tool, needed '
                             'for FAIRSCAPE. If unset, organization name specified '
                             'in --inputdir directory or provenance file will be used')
    parser.add_argument('--project_name',
                        help='Name of project running this tool, needed for '
                             'FAIRSCAPE. If unset, project name specified '
                             'in --input directory or provenance file will be used')
    parser.add_argument('--skip_logging', action='store_true',
                        help='If set, output.log, error.log '
                             'files will not be created')
    parser.add_argument('--logconf', default=None,
                        help='Path to python logging configuration file in '
                             'this format: https://docs.python.org/3/library/'
                             'logging.config.html#logging-config-fileformat '
                             'Setting this overrides -v parameter which uses '
                             ' default logger. (default None)')
    parser.add_argument('--verbose', '-v', action='count', default=1,
                        help='Increases verbosity of logger to standard '
                             'error for log messages in this module. Messages are '
                             'output at these python logging levels '
                             '-v = WARNING, -vv = INFO, '
                             '-vvv = DEBUG, -vvvv = NOTSET (default ERROR '
                             'logging)')
    parser.add_argument('--version', action='version',
                        version=('%(prog)s ' +
                                 cellmaps_ppi_embedding.__version__))

    return parser.parse_args(args)


def main(args):
    """
    Main entry point for program

    :param args: arguments passed to command line usually :py:func:`sys.argv[1:]`
    :type args: list

    :return: return value of :py:meth:`cellmaps_ppi_embedding.runner.CellMapsPPIEmbedder.run`
             or ``2`` if an exception is raised
    :rtype: int
    """
    desc = """
    Version {version}

    Invokes run() method on CellMapsPPIEmbedder

    """.format(version=cellmaps_ppi_embedding.__version__)
    theargs = _parse_arguments(desc, args[1:])
    theargs.program = args[0]
    theargs.version = cellmaps_ppi_embedding.__version__

    if theargs.provenance is not None:
        with open(theargs.provenance, 'r') as f:
            json_prov = json.load(f)
    else:
        json_prov = None

    try:
        logutils.setup_cmd_logging(theargs)
        if theargs.fake_embedder is True:
            gen = FakeEmbeddingGenerator(theargs.inputdir,
                                         dimensions=theargs.dimensions)
        else:
            gen = Node2VecEmbeddingGenerator(nx_network=nx.read_edgelist(CellMapsPPIEmbedder.get_apms_edgelist_file(theargs.inputdir),
                                                                         delimiter='\t'),
                                             dimensions=theargs.dimensions,
                                             p=theargs.p,
                                             q=theargs.q,
                                             walk_length=theargs.walk_length,
                                             num_walks=theargs.num_walks,
                                             workers=theargs.workers)

        return CellMapsPPIEmbedder(outdir=theargs.outdir,
                                   embedding_generator=gen,
                                   skip_logging=theargs.skip_logging,
                                   name=theargs.name,
                                   organization_name=theargs.organization_name,
                                   project_name=theargs.project_name,
                                   inputdir=theargs.inputdir,
                                   provenance=json_prov,
                                   input_data_dict=theargs.__dict__).run()
    except Exception as e:
        logger.exception('Caught exception: ' + str(e))
        return 2
    finally:
        logging.shutdown()


if __name__ == '__main__':  # pragma: no cover
    sys.exit(main(sys.argv))
