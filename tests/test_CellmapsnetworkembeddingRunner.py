#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_network_embedding` package."""

import os
import unittest
import tempfile
import shutil
import csv
from cellmaps_network_embedding.runner import CellMapsNetworkEmbeddingRunner
from cellmaps_network_embedding.exceptions import CellMapsNetworkEmbeddingError


class TestCellmapsNetworkEmbeddingRunner(unittest.TestCase):
    """Tests for `cellmaps_network_embedding` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_constructor(self):
        """Tests constructor"""
        myobj = CellMapsNetworkEmbeddingRunner()

        self.assertIsNotNone(myobj)

    def test_run_no_outdir(self):
        """ Tests run()"""
        myobj = CellMapsNetworkEmbeddingRunner()
        try:
            myobj.run()
            self.fail('Expected exception')
        except CellMapsNetworkEmbeddingError as ce:
            self.assertEqual('outdir must be set', str(ce))

    def test_run_no_edgelist(self):
        try:
            temp_dir = tempfile.mkdtemp()
            myobj = CellMapsNetworkEmbeddingRunner(outdir=temp_dir)
            myobj.run()
            self.fail('Expected exception')
        except CellMapsNetworkEmbeddingError as ce:
            self.assertEqual('edgelist must be set to a file', str(ce))
        finally:
            shutil.rmtree(temp_dir)

    def test_run_edgelist_not_a_file(self):
        try:
            temp_dir = tempfile.mkdtemp()
            myobj = CellMapsNetworkEmbeddingRunner(outdir=temp_dir, edgelist='foo')
            myobj.run()
            self.fail('Expected exception')
        except CellMapsNetworkEmbeddingError as ce:
            self.assertEqual('edgelist foo is not a file', str(ce))
        finally:
            shutil.rmtree(temp_dir)

    def test_run_success(self):
        try:
            temp_dir = tempfile.mkdtemp()
            e_file = os.path.join(temp_dir, 'edgelist.tsv')
            with open(e_file, 'w') as f:
                f.write('geneA\tgeneB\n')
                f.write('ABC\tDEF\n')
            myobj = CellMapsNetworkEmbeddingRunner(outdir=temp_dir,
                                                   edgelist=e_file)
            self.assertEqual(0, myobj.run())
            apms_emd = os.path.join(temp_dir, 'apms_emd.tsv')
            self.assertTrue(os.path.isfile(apms_emd))
            with open(apms_emd, 'r') as f:
                reader = csv.reader(f, delimiter='\t')
                resmap = {}
                for row in reader:
                    resmap[row[0]] = row[1:]

                for g in ['ABC', 'DEF']:
                    self.assertTrue(g in resmap)
                    self.assertEqual(1024, len(resmap[g]))
        finally:
            shutil.rmtree(temp_dir)
