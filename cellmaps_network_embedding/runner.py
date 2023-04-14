#! /usr/bin/env python

import os
import sys
import csv
import random
import logging
import subprocess

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
                 dimensions=1024,
                 pythonbinary='/opt/conda/bin/python',
                 node2vec='/opt/node2vec/src/main.py'):
        """
        Constructor

        :param exitcode: value to return via :py:meth:`.CellMapsNetworkEmbeddingRunner.run` method
        :type int:
        """
        self._edgelist = edgelist
        self._outdir = outdir
        self._dimensions = dimensions
        self._p = p
        self._q = q
        self._node2vec = node2vec
        self._pythonbinary = pythonbinary
        logger.debug('In constructor')

    def _run_cmd(self, cmd):
        """
        Runs hidef command as a command line process
        :param cmd_to_run: command to run as list
        :type cmd_to_run: list
        :return: (return code, standard out, standard error)
        :rtype: tuple
        """
        p = subprocess.Popen(cmd,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        out, err = p.communicate()

        return p.returncode, out, err

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
        name_to_id = {}
        id_to_name = {}
        idcounter = 0

        numeric_edgelist = os.path.join(self._outdir, 'node2vec_input_edgelist.tsv')

        with open(numeric_edgelist, 'w') as f:
            with open(self._edgelist, 'r') as inputf:
                reader = csv.DictReader(inputf, delimiter='\t')
                for row in reader:
                    for entry in [row['geneA'], row['geneB']]:
                        if entry not in name_to_id:
                            name_to_id[entry] = idcounter
                            id_to_name[idcounter] = entry
                            idcounter += 1
                    f.write(str(name_to_id[row['geneA']]) + '\t' + str(name_to_id[row['geneB']]) + '\n')
                    uniq_genes.add(row['geneA'])
                    uniq_genes.add(row['geneB'])
        node2vec_out = os.path.join(self._outdir, 'node2vec_out.tsv')
        returncode, out, err = self._run_cmd([self._pythonbinary, self._node2vec, '--input',
                                              numeric_edgelist,
                                              '--output',
                                              node2vec_out,
                                              '--dimensions', str(self._dimensions),
                                              '--p', str(self._p), '--q', str(self._q)])
        sys.stdout.write(out)
        sys.stderr.write(err)
        sys.stdout.write('Exit Code: ' + str(returncode))

        with open(os.path.join(self._outdir, 'apms_emd.tsv'), 'w') as f:
            headerline = ['']
            for x in range(1, self._dimensions+1):
                headerline.append(str(x))
            f.write('\t'.join(headerline) + '\n')
            with open(node2vec_out, 'r') as inputf:
                reader = csv.reader(inputf, delimiter=' ')
                next(reader)
                for row in reader:
                    print(row)
                    f.write(id_to_name[int(row[0])] + '\t')
                    resultline = []
                    for entry in row[1:self._dimensions+1]:
                        resultline.append(str(entry))
                    f.write('\t'.join(resultline) + '\n')

        """
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
        """
        return 0
