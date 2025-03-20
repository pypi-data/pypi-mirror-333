# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

from __future__ import annotations

import logging
import re
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

import numpy
import toml
from typing_extensions import Self

from .channel import Channel

logger = logging.getLogger("arrakis")


class MetadataBackend(Protocol):
    def update(self, channels: Iterable[Channel]) -> None:
        """Update channel metadata.

        Parameters
        ----------
        channels : Iterable[Channel]
            Channels for which to update metadata with.

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
            Publishers to match.

        Returns
        -------
        Iterable[Channel]
            Channel objects for all channels matching query.

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

    @classmethod
    def load(cls, *args, **kwargs) -> Self:
        """Load current channel metadata snapshot."""
        ...


@dataclass(kw_only=True)
class ConfigMetadataBackend(MetadataBackend):
    """A channel metadata backend backed by configuration.

    Channel metadata is stored as a configuration file in the TOML format.

    Parameters
    ----------
    metadata : dict[str, Channel], optional
        A dictionary whose keys are channel names and values are channel objects.
    extra : dict[str, str], optional
        A dictionary whose keys are channel names and values are additional
        metadata associated with the channel.
    config_file : Path
        Where the configuration file containing the channel metadata is
        located.

    """

    metadata: dict[str, Channel] = field(default_factory=dict)
    extra: dict[str, dict[str, Any]] = field(default_factory=dict)
    config_file: Path

    @property
    def scopes(self) -> dict[str, list[dict[str, Any]]]:
        """The scopes that the set of channels span."""
        scopes: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for channel in self.metadata.values():
            scopes[channel.domain].append({"subsystem": channel.subsystem})
        return scopes

    def update(self, channels: Iterable[Channel]) -> None:
        # update in-memory channel map
        changed = set(channels) - set(self.metadata.values())
        for channel in changed:
            assert channel.publisher
            self.metadata[channel.name] = channel

        # write updated channel map to disk
        metadata = {}
        for channel_name, meta in self.metadata.items():
            metadata[channel_name] = {
                "rate": meta.sample_rate,
                "dtype": numpy.dtype(meta.data_type).name,
                "partition": meta.partition_id,
                "publisher": meta.publisher,
            }
        with self.config_file.open("w") as f:
            toml.dump(metadata, f)

    def find(
        self,
        *,
        pattern: str,
        data_type: list[str],
        min_rate: int,
        max_rate: int,
        publisher: list[str],
    ) -> Iterable[Channel]:
        expr = re.compile(pattern)
        channels = []
        dtypes = {numpy.dtype(dtype) for dtype in data_type}
        publishers = set(publisher)
        for channel in self.metadata.values():
            if expr.match(channel.name):
                rate = channel.sample_rate
                if not (rate >= min_rate and rate <= max_rate):
                    continue
                if dtypes and channel.data_type not in dtypes:
                    continue
                if publishers and channel.publisher not in publishers:
                    continue
                channels.append(channel)

        return channels

    def describe(self, *, channels: Iterable[str]) -> Iterable[Channel]:
        return [self.metadata[channel] for channel in channels]

    @classmethod
    def load(cls, config_file: Path, *paths: Path) -> Self:
        """Load current channel metadata snapshot.

        Parameters
        ----------
        config_file : Path
            Where the configuration file containing the channel metadata is
            located.
        *paths : Path
            Any additional configuration files with channel metadata to load
            in.

        """
        channel_map = {}
        extra = {}
        for path in [config_file, *paths]:
            logger.info("loading channel description file: %s", path)
            with path.open("r") as f:
                metadata = toml.load(f)
                for channel_name, meta in metadata.items():
                    logger.debug("  %s", channel_name)
                    data_type = numpy.dtype(meta.pop("dtype"))
                    channel = Channel(
                        channel_name,
                        data_type=data_type,
                        sample_rate=meta.pop("rate"),
                        partition_id=meta.pop("partition", None),
                        publisher=meta.pop("publisher", None),
                    )
                    channel_map[channel_name] = channel
                    extra[channel_name] = meta

        return cls(
            metadata=channel_map,
            extra=extra,
            config_file=config_file,
        )
