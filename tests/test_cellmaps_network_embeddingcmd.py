#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_network_embedding` package."""

import os
import tempfile
import shutil

import unittest
from cellmaps_network_embedding import cellmaps_network_embeddingcmd


class TestCellmapsNetworkEmbedding(unittest.TestCase):
    """Tests for `cellmaps_network_embedding` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_parse_arguments(self):
        """Tests parse arguments"""
        res = cellmaps_network_embeddingcmd._parse_arguments('hi',
                                                             ['outdir',
                                                              '--input',
                                                              'somefile'])

        self.assertEqual(0, res.verbose, 0)
        self.assertEqual('outdir', res.outdir)
        self.assertEqual('somefile', res.inputdir)
        self.assertEqual(2, res.p)
        self.assertEqual(1, res.q)
        self.assertEqual(1024, res.dimensions)
        self.assertEqual(None, res.logconf)

        someargs = ['-vv', '--logconf', 'hi', 'outdir',
                    '--inputdir', 'somefile']
        res = cellmaps_network_embeddingcmd._parse_arguments('hi', someargs)

        self.assertEqual(2, res.verbose)
        self.assertEqual('hi', res.logconf)

    def test_main(self):
        """Tests main function"""

        # try where loading config is successful
        try:
            temp_dir = tempfile.mkdtemp()
            res = cellmaps_network_embeddingcmd.main(['myprog.py',
                                                      'outdir',
                                                      '--input',
                                                      'somefile'])
            self.assertEqual(res, 2)
        finally:
            shutil.rmtree(temp_dir)
