# SPDX-FileCopyrightText: 2025-present Chris O'Neill <chris@purplejay.io>
#
# SPDX-License-Identifier: MIT

from .models import *
from .emass_service import (
    get_http_client,
    make_initial_test_connection,
    get_systems,
    generate_api_key,
    get_dashboard_payload,
    load_all_dashboard_data_in_batches,
)
from .settings import EmassSettings, init_settings, get_settings

__all__ = [
    "get_http_client",
    "make_initial_test_connection",
    "get_systems",
    "generate_api_key",
    "get_dashboard_payload",
    "load_all_dashboard_data_in_batches",
    "EmassSettings",
    "init_settings",
    "get_settings",
] + models.__all__

from loguru import logger

logger.disable("pjdev_va_ois_emass_api_client")
