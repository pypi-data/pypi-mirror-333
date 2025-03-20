import argparse
import logging
import pathlib
import sys

from . import __version__, traits
from .backends import BackendType
from .constants import DEFAULT_LOCATION
from .scope import ScopeMap
from .server import ArrakisFlightServer

logger = logging.getLogger("arrakis")


def get_log_level(args: argparse.Namespace) -> int:
    """Determine the log level from logging options."""
    if args.quiet:
        return logging.WARNING
    elif args.verbose:
        return logging.DEBUG
    else:
        return logging.INFO


def main() -> None:
    parser = argparse.ArgumentParser(prog="arrakis-server")
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="If set, only display warnings and errors.",
    )
    group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="If set, display additional logging messages.",
    )
    parser.add_argument(
        "-u",
        "--url",
        default=DEFAULT_LOCATION,
        help=f"Serve requests at this URL. Default: {DEFAULT_LOCATION}",
    )
    parser.add_argument(
        "-s",
        "--scope-map-file",
        type=pathlib.Path,
        help="Scope map file",
    )
    parser.add_argument(
        "-b",
        "--backend",
        type=str.upper,
        choices=BackendType.__members__,
        default="MOCK",
        help="The data backend to use. Default: MOCK",
    )
    parser.add_argument(
        "--backend-server-url",
        help=(
            "URL pointing to a running backend server. "
            "Required if using KAFKA or NDS backend."
        ),
    )
    parser.add_argument(
        "--mock-channel-file",
        action="append",
        type=pathlib.Path,
        help=(
            "Channel definition file for MOCK backend. May be specified multiple times."
        ),
    )
    args = parser.parse_args()

    # set up logger
    logger = logging.getLogger("arrakis")
    log_level = get_log_level(args)
    logger.setLevel(log_level)
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(log_level)
    formatter = logging.Formatter("%(asctime)s | arrakis : %(levelname)s : %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    backend_type = BackendType[args.backend.upper()]

    ##############################

    logger.info("Arrakis server %s", __version__)

    # load scope map
    scope_map = None
    if args.scope_map_file:
        logger.info("loading global scope map:")
        scope_map = ScopeMap.load(args.scope_map_file)
        for loc, info in scope_map.servers.items():
            logger.info("  %s: %s", loc, info.domains)

    # initialize the backend
    logger.info("initializing %s...", backend_type)
    backend: traits.MaybeBackend
    match backend_type:
        case BackendType.NONE:  # type: ignore
            backend = None
        case _:
            backend = backend_type.value.from_args(args)

    # serve requests
    logger.info("initializing flight server...")
    server = ArrakisFlightServer(
        url=args.url,
        backend=backend,
        scope_map=scope_map,
    )
    server.serve()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
