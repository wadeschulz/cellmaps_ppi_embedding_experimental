#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_network_embedding` package."""


import unittest
from cellmaps_network_embedding.runner import CellmapsnetworkembeddingRunner


class TestCellmapsnetworkembeddingrunner(unittest.TestCase):
    """Tests for `cellmaps_network_embedding` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_constructor(self):
        """Tests constructor"""
        myobj = CellmapsnetworkembeddingRunner(0)

        self.assertIsNotNone(myobj)

    def test_run(self):
        """ Tests run()"""
        myobj = CellmapsnetworkembeddingRunner(4)
        self.assertEqual(4, myobj.run())
