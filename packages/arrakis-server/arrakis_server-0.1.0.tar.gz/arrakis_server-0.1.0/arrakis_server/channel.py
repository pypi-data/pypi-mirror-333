# Copyright (c) 2025, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-python/-/raw/main/LICENSE

"""Server-specific channel information."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

from arrakis.channel import Channel as BaseChannel


@dataclass(frozen=True, order=True)
class Channel(BaseChannel):
    """Metadata associated with a channel.

    Channels have the form {domain}:{subsystem}-*.

    Parameters
    ----------
    name : str
        The name associated with this channel.
    data_type : numpy.dtype
        The data type associated with this channel.
    sample_rate : float
        The sampling rate associated with this channel.
    time : int, optional
        The timestamp when this metadata became active.
    publisher : str
        The publisher associated with this channel.
    partition_id : str, optional
        The partition ID associated with this channel.

    """

    def validate(self) -> None:
        components = self.name.split(":")
        if len(components) != 2 or "-" not in self.name:
            raise ValueError(
                "channel is malformed, needs to be in the form {domain}:{subsystem}-*"
            )

    @cached_property
    def subsystem(self) -> str:
        """The subsystem associated with a given channel."""
        _, rest = self.name.split(":")
        return rest.split("-")[0]


def extract_channel_scope(channel: str) -> tuple[str, str]:
    """Given a channel name, extracts the channel's scope.

    Parameters
    ----------
    channel : str
        The channel with the form {domain}:{subsystem}-*.

    Returns
    -------
    tuple[str, str]
        The domain and the subsystem, respectively.
    """
    components = channel.split(":")
    if len(components) != 2 or "-" not in channel:
        raise ValueError(
            "channel is malformed, needs to be in the form {domain}:{subsystem}-*"
        )

    domain, rest = components
    subsystem = rest.split("-")[0]

    return domain, subsystem
