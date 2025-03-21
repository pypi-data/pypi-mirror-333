#
# Copyright 2018-2025 Fragment Contributors
# SPDX-License-Identifier: Apache-2.0
#
import logging

# Configure the default logger
# The life-cycle handler will configure this
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())
