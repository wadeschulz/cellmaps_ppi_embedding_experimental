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

        self.assertEqual(res.verbose, 0)
        self.assertEqual(res.outdir, 'outdir')
        self.assertEqual(res.input, 'somefile')
        self.assertEqual(res.p, 2)
        self.assertEqual(res.q, 1)
        self.assertEqual(res.dimensions, 1024)
        self.assertEqual(res.logconf, None)

        someargs = ['-vv', '--logconf', 'hi', 'outdir',
                    '--input', 'somefile']
        res = cellmaps_network_embeddingcmd._parse_arguments('hi', someargs)

        self.assertEqual(res.verbose, 2)
        self.assertEqual(res.logconf, 'hi')

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
