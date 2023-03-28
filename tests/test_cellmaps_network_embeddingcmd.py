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

    def test_setup_logging(self):
        """ Tests logging setup"""
        try:
            cellmaps_network_embeddingcmd._setup_logging(None)
            self.fail('Expected AttributeError')
        except AttributeError:
            pass

        # args.logconf is None
        res = cellmaps_network_embeddingcmd._parse_arguments('hi',
                                                             ['outdir',
                                                              '--input',
                                                              'somefile'])
        cellmaps_network_embeddingcmd._setup_logging(res)

        # args.logconf set to a file
        try:
            temp_dir = tempfile.mkdtemp()

            logfile = os.path.join(temp_dir, 'log.conf')
            with open(logfile, 'w') as f:
                f.write("""[loggers]
keys=root

[handlers]
keys=stream_handler

[formatters]
keys=formatter

[logger_root]
level=DEBUG
handlers=stream_handler

[handler_stream_handler]
class=StreamHandler
level=DEBUG
formatter=formatter
args=(sys.stderr,)

[formatter_formatter]
format=%(asctime)s %(name)-12s %(levelname)-8s %(message)s""")

            res = cellmaps_network_embeddingcmd._parse_arguments('hi', ['--logconf',
                                                                        logfile,
                                                                        'outdir',
                                                                        '--input',
                                                                        'somefile'])
            cellmaps_network_embeddingcmd._setup_logging(res)

        finally:
            shutil.rmtree(temp_dir)

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
