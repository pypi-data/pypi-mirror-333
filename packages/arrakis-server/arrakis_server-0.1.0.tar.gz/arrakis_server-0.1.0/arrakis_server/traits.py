# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

from __future__ import annotations

import argparse
import threading
from collections.abc import Iterable, Iterator
from typing import Protocol, runtime_checkable

from arrakis import SeriesBlock
from typing_extensions import TypeGuard

from .channel import Channel
from .scope import Retention, ScopeInfo


@runtime_checkable
class ServerBackend(Protocol):
    scope_info: ScopeInfo

    def __str__(self):
        return f"<{self.__class__.__name__} domains: {self.domains}>"

    @property
    def domains(self) -> set[str]:
        return self.scope_info.domains

    @property
    def retention(self) -> Retention:
        return self.scope_info.retention

    @classmethod
    def from_args(cls, args: argparse.Namespace) -> ServerBackend:
        """Instantiate a backend from an argparse Namespace"""
        ...

    def stream(
        self, *, channels: Iterable[str], start: int, end: int
    ) -> Iterator[SeriesBlock]:
        """Stream timeseries data.

        Parameters
        ----------
        channels : Iterable[str]
            Channels to request.
        start : int
            GPS start time.
        end : int
            GPS end time.

        Yields
        ------
        SeriesBlock
            Dictionary-like object containing all requested channel data.

        Setting neither start nor end begins a live stream starting
        from now.

        """
        ...

    def describe(self, *, channels: Iterable[str]) -> Iterable[Channel]:
        """Get channel metadata for channels requested.

        Parameters
        ----------
        channels : Iterable[str]
            Channels to request.

        Returns
        -------
        Channel
            Channel objects, one per channel requested.

        """
        ...

    def find(
        self,
        *,
        pattern: str,
        data_type: list[str],
        min_rate: int,
        max_rate: int,
        publisher: list[str],
    ) -> Iterable[Channel]:
        """Find channels matching a set of conditions.

        Parameters
        ----------
        pattern : str
            Channel pattern to match channels with, using regular expressions.
        data_type : list[str]
            Data types to match.
        min_rate : int
            Minimum sampling rate for channels.
        max_rate : int
            Maximum sampling rate for channels.
        publisher : list[str]
            Sources to match.

        Returns
        -------
        Iterable[Channel]
            Channel objects for all channels matching query.

        """
        ...

    def count(
        self,
        *,
        pattern: str,
        data_type: list[str],
        min_rate: int,
        max_rate: int,
        publisher: list[str],
    ) -> int:
        """Count channels matching a set of conditions.

        Parameters
        ----------
        pattern : str
            Channel pattern to match channels with, using regular expressions.
        data_type : list[str]
            Data types to match.
        min_rate : int
            Minimum sampling rate for channels.
        max_rate : int
            Maximum sampling rate for channels.
        publisher : list[str]
            Sources to match.

        Returns
        -------
        int
            The number of channels matching query.

        """
        metadata = self.find(
            pattern=pattern,
            data_type=data_type,
            min_rate=min_rate,
            max_rate=max_rate,
            publisher=publisher,
        )
        return sum(1 for _ in metadata)


@runtime_checkable
class PublishServerBackend(ServerBackend, Protocol):
    _lock: threading.Lock = threading.Lock()

    def publish(self, *, publisher_id: str) -> dict[str, str]:
        """Return producer-based connection info needed to publish data.

        Parameters
        ----------
        publisher_id : str
            The ID assigned to the publisher.

        Returns
        -------
        dict[str, str]
            A dictionary containing producer-based connection info.

        """
        ...

    def partition(
        self, *, publisher_id: str, channels: Iterable[Channel]
    ) -> Iterable[Channel]:
        """Return producer-based connection info needed to publish data.

        Parameters
        ----------
        publisher_id : str
            The ID assigned to the producer.
        channels : Iterable[Channel]
            Channel objects, one for each channel needing to have their
            partitions assigned.

        Returns
        -------
        Iterable[Channel]
            Channel objects with their partition IDs set.

        """
        ...


MaybeBackend = ServerBackend | None


def can_publish(
    backend: ServerBackend | PublishServerBackend | None,
) -> TypeGuard[PublishServerBackend]:
    """Determine if a server backend supports publish-like functionality."""
    # Note this is actually a "protocol" check, essentially a duck
    # type check, rather than an check that the class is explicitly an
    # instance of the specified protocol being compared against.  See:
    # https://typing.readthedocs.io/en/latest/spec/protocol.html
    return isinstance(backend, PublishServerBackend)
