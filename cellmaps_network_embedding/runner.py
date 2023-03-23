#! /usr/bin/env python

import logging


logger = logging.getLogger(__name__)


class {{ cookiecutter.project_slug.replace('_','').capitalize() }}Runner(object):
    """
    Class to run algorithm
    """
    def __init__(self, exitcode):
        """
        Constructor

        :param exitcode: value to return via :py:meth:`.{{ cookiecutter.project_slug.replace('_','').capitalize() }}Runner.run` method
        :type int:
        """
        self._exitcode = exitcode
        logger.debug('In constructor')

    def run(self):
        """
        Runs CM4AI Network Embedding Tool


        :return:
        """
        logger.debug('In run method')
        return self._exitcode
