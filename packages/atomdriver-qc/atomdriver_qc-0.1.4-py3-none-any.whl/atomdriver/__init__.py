#
# Copyright 2018-2024 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import logging

__version__ = "0.0.1"

# Configure the default logger
# The life-cycle handler will configure this
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
