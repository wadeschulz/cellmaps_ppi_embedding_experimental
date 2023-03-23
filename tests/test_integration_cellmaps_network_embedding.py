#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Integration Tests for `cellmaps_network_embedding` package."""

import os

import unittest
from cellmaps_network_embedding import {{ cookiecutter.project_slug }}cmd

SKIP_REASON = 'CELLMAPS_NETWORK_EMBEDDING_INTEGRATION_TEST ' \
              'environment variable not set, cannot run integration ' \
              'tests'

@unittest.skipUnless(os.getenv('CELLMAPS_NETWORK_EMBEDDING_INTEGRATION_TEST') is not None, SKIP_REASON)
class TestIntegrationCellmaps_network_embedding(unittest.TestCase):
    """Tests for `cellmaps_network_embedding` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_something(self):
        """Tests parse arguments"""
        self.assertEqual(1, 1)
