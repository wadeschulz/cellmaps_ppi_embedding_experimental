#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cellmaps_network_embedding` package."""


import unittest
from cellmaps_network_embedding.runner import {{ cookiecutter.project_slug.replace('_','').capitalize() }}Runner


class Test{{ Cookiecutter.project_slug.replace('_','').capitalize() }}runner(unittest.TestCase):
    """Tests for `cellmaps_network_embedding` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_constructor(self):
        """Tests constructor"""
        myobj = {{ cookiecutter.project_slug.replace('_','').capitalize() }}Runner(0)

        self.assertIsNotNone(myobj)

    def test_run(self):
        """ Tests run()"""
        myobj = {{ cookiecutter.project_slug.replace('_','').capitalize() }}Runner(4)
        self.assertEqual(4, myobj.run())
