# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

import warnings
from enum import Enum
from importlib.metadata import entry_points

from ..traits import MaybeBackend


def _discover_backends() -> dict[str, MaybeBackend]:
    backends: dict[str, MaybeBackend] = {"NONE": None}
    entrypoints = entry_points(group="arrakis-server-backend")
    for backend_name in entrypoints.names:
        try:
            backends[backend_name.upper()] = entrypoints[backend_name].load()
        except ImportError:
            warnings.warn(
                f"{backend_name} backend could not be loaded",
                category=ImportWarning,
            )
    return backends


BackendType = Enum("BackendType", _discover_backends())  # type: ignore[misc]
