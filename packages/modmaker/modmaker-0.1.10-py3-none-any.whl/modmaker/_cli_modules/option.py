"""
This is the basic skeleton for this module. The class name will become options for the binary locate in the bin dir
"""

import logging

LOG = logging.getLogger(__name__)


class Option:
    """
    No Commands defined
    """

    def __init__(self):
        self.description = "Option"
        LOG.info("... ")
