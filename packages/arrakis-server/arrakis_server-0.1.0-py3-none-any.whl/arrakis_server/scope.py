from __future__ import annotations

import logging
import math
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any

from ruamel.yaml import YAML
from typing_extensions import Self

from . import constants
from .channel import extract_channel_scope

if TYPE_CHECKING:
    from .traits import ServerBackend

logger = logging.getLogger("arrakis")

ChannelEndpointList = list[tuple[list[str], list[str]]]


@dataclass
class ScopeMap:
    """A mapping between endpoints and the scopes they provide.

    Parameters
    ----------
    servers : dict[str, ScopeInfo], optional
        A dictionary whose keys are endpoints (server URLs) and values are
        information about the scopes they provide.
    local_endpoint : str, optional
        If provided, define which URL correspond to the local server URL.

    """

    servers: dict[str, ScopeInfo] = field(default_factory=dict)
    local_endpoint: str | None = None

    @property
    def endpoints(self) -> set[str]:
        """The set of endpoints contained within this mapping."""
        return {endpoint for endpoint in self.servers.keys()}

    @property
    def domains(self) -> set[str]:
        """The set of domains that the list of endpoints provide."""
        return {
            domain for info in self.servers.values() for domain in info.scopes.keys()
        }

    def endpoints_for_domain(self, domain: str) -> list[str]:
        """Determine all endpoints that can serve a given domain.

        Parameters
        ----------
        domain : str
            The domain to determine the endpoints for.

        Returns
        -------
        list[str]
            All endpoints that serve a given domain.

        """
        # first check if local server serves this domain
        if self.local_endpoint and self.local_endpoint in self.servers:
            if domain in self.servers[self.local_endpoint].scopes:
                return [constants.FLIGHT_REUSE_URL]

        # otherwise, find all endpoints which can serve this domain
        return [
            endpoint for endpoint, info in self.servers.items() if domain in info.scopes
        ]

    def endpoints_for_channel(self, channel: str) -> list[str]:
        """Determine all endpoints that can serve a given channel.

        Parameters
        ----------
        channel : str
            The channel to determine the endpoints for.

        Returns
        -------
        list[str]
            All endpoints that serve a given channel.

        """
        # first check if local server serves this data
        if self.local_endpoint and self.local_endpoint in self.servers:
            if self.servers[self.local_endpoint].in_scope(channel):
                return [constants.FLIGHT_REUSE_URL]

        # otherwise, find all endpoints which can serve this data
        return [
            endpoint
            for endpoint, info in self.servers.items()
            if info.in_scope(channel)
        ]

    def endpoints_for_channels(self, channels: Iterable[str]) -> ChannelEndpointList:
        """Determine the endpoints that can serve the given channels.

        Parameters
        ----------
        channels : Iterable[str]
            The channels to determine the endpoints for.

        Returns
        -------
        ChannelEndpointList
            A list of (channels, endpoints) pairs, where each grouping is a
            list of endpoints where the channels can be found at. The channels
            are disjoint such that the union of all channels returns the
            original channels requested.

        """
        # construct a bi-directional map between endpoints and channels
        endpoint_channel_map = defaultdict(set)
        channel_endpoint_map = {}
        for channel in channels:
            endpoints = self.endpoints_for_channel(channel)
            channel_endpoint_map[channel] = endpoints
            for endpoint in endpoints:
                endpoint_channel_map[endpoint].add(channel)

        # consolidate endpoints for each set of channels
        endpoints_for_channels: ChannelEndpointList = []
        remaining_channels = set(channel_endpoint_map.keys())

        # first, prioritize local endpoint
        if constants.FLIGHT_REUSE_URL in endpoint_channel_map:
            local_endpoint = constants.FLIGHT_REUSE_URL
            local_channels = endpoint_channel_map.pop(local_endpoint)
            remaining_channels -= frozenset(local_channels)
            endpoints_for_channels.append((list(local_channels), [local_endpoint]))

        # then, prioritize endpoints which serve the most channels
        while remaining_channels:
            for endpoint in endpoint_channel_map:
                endpoint_channel_map[endpoint] -= remaining_channels

            # choose one with the most channels, and select all endpoints
            # matching the set of channels it serves
            max_endpoint = max(
                endpoint_channel_map, key=lambda x: len(endpoint_channel_map[x])
            )
            max_channels = endpoint_channel_map[max_endpoint]
            endpoints = [
                endpoint
                for endpoint, channels in endpoint_channel_map.items()
                if channels == max_channels
            ]
            for endpoint in endpoints:
                endpoint_channel_map.pop(endpoint)
            endpoints_for_channels.append((list(max_channels), endpoints))
            remaining_channels -= frozenset(max_channels)

        return endpoints_for_channels

    def sync_local_map(self, backend: ServerBackend | None, endpoint: str) -> None:
        """Add local scope information to the scope map.

        This checks consistency between the scope map and the new local scope
        information that is provided. In addition, this updates the local
        endpoint accordingly to prioritize the serving of local data if this
        backend also serves data and/or metadata.

        Parameters
        ----------
        backend : ServerBackend
            The local backend in which to update the scope map with.
        endpoint : str
            The endpoint associated with the local server.

        """

        self.local_endpoint = endpoint
        # check consistency with the scope map and what's in the backend
        if backend:
            if endpoint in self.servers:
                for domain in backend.scope_info.domains:
                    if domain not in self.servers[endpoint].scopes:
                        logger.warning("domain %s not in global scope map", domain)
                    elif backend.scope_info.scopes != self.servers[endpoint]:
                        logger.warning(
                            "local scope info is inconsistent with global scope map"
                        )

            self.servers[endpoint] = backend.scope_info

    def filter(self, live: bool = True) -> Self:
        """Filter the scope map by whether endpoints serve live or historical data.

        Parameters
        ----------
        live : bool, optional
            Whether to filter by live or non-live data. Default is live.

        Returns
        -------
        SourceMap
            The filtered scope map.

        """
        servers = {}
        for endpoint, info in self.servers.items():
            if (not info.retention.is_historical_only and live) or (
                not info.retention.is_live_only and not live
            ):
                servers[endpoint] = info
        return type(self)(servers, self.local_endpoint)

    @classmethod
    def load(cls, scope_map_file: Path) -> Self:
        """Load a configuration-based scope map from disk.

        Parameters
        ----------
        scope_map_file : Path
            The path to the scope map configuration file

        Returns
        -------
        SourceMap
            The loaded scope map.

        """
        servers = {}
        with open(scope_map_file, "r") as f:
            for endpoint, info in YAML(typ="safe").load(f).items():
                servers[endpoint] = ScopeInfo(
                    scopes=info["scopes"],
                    retention=Retention(**info["retention"]),
                )
        return cls(servers)


@dataclass
class ScopeInfo:
    """Information about the scopes and retention a server provides.

    Parameters
    ----------
    scopes : dict[str, list[dict[str, Any]]]
        The scopes that a server provide for each domain. The keys are
        domains and the values are lists of key-value pairs indicating how the
        domains are scoped. These could be subsystems, specific channels, etc.
    retention : Retention
        The range of time available (from now) that is accessible to query.

    """

    scopes: dict[str, list[dict[str, Any]]]
    retention: Retention

    @property
    def domains(self) -> set[str]:
        return set(self.scopes.keys())

    def in_scope(self, channel: str) -> bool:
        """Check whether the channel is served by this endpoint."""
        domain, subsystem = extract_channel_scope(channel)
        if domain not in self.scopes:
            return False
        served_subsystems = {scope["subsystem"] for scope in self.scopes[domain]}
        return subsystem in served_subsystems


@dataclass
class Retention:
    """Information about the time retention that can be queried from a server.

    This is used to inform what range of data backends can serve and how
    incoming requests can take a range of times and delegate them to various
    servers.

    The times specified here are in seconds all relative to 'now', i.e. 0
    corresponds to serving live data, while 3600 corresponds to '1 hour ago'.

    Live-only data sources have both 'newest' and 'oldest' set to 0, and can
    be created using the class method Retention.from_live_only().

    Parameters
    ----------
    newest : float, optional
        The most recent time from now that can be queried. Defaults to 0, or
        'now'.
    oldest : float, optional
        The oldest time from now that can be queried. Defaults to inf, or
        infinite lookback.

    """

    newest: float = 0
    oldest: float = math.inf

    @property
    def is_live(self) -> bool:
        """Determine whether this backend can serve live data."""
        return self.newest == 0

    @property
    def is_live_only(self) -> bool:
        """Determine whether this backend can only serve live data."""
        return self.newest == 0 and self.oldest == 0

    @property
    def is_historical_only(self) -> bool:
        """Determine whether this backend can only serve historical data."""
        return self.newest > 0

    @classmethod
    def from_live_only(cls) -> Self:
        """Create a retention that can only serve live data."""
        return cls(newest=0, oldest=0)
