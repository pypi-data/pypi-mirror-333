# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

"""Arrow Flight schema definitions."""

from collections.abc import Iterable

import pyarrow
from arrakis import Channel


def stream(channels: Iterable[Channel]) -> pyarrow.Schema:
    """Create an Arrow Flight schema for `stream`.

    Parameters
    ----------
    channels : Iterable[Channel]
        The list of channels for the stream request.

    Returns
    -------
    pyarrow.Schema
        The stream schema.

    """
    columns = [pyarrow.field("time", pyarrow.int64(), nullable=False)]
    for channel in channels:
        dtype = pyarrow.from_numpy_dtype(channel.data_type)
        field = pyarrow.field(channel.name, pyarrow.list_(dtype)).with_metadata(
            {"rate": str(channel.sample_rate)}
        )
        columns.append(field)
    return pyarrow.schema(columns)


def describe() -> pyarrow.Schema:
    """Create an Arrow Flight schema for `describe`.

    Returns
    -------
    pyarrow.Schema
        The describe schema.

    """
    return find()


def find() -> pyarrow.Schema:
    """Create an Arrow Flight schema for `find`.

    Returns
    -------
    pyarrow.Schema
        The find schema.

    """
    return pyarrow.schema(
        [
            pyarrow.field("channel", pyarrow.string(), nullable=False),
            pyarrow.field("data_type", pyarrow.string(), nullable=False),
            pyarrow.field("sample_rate", pyarrow.int32(), nullable=False),
            pyarrow.field("partition_id", pyarrow.string()),
            pyarrow.field("publisher", pyarrow.string()),
        ]
    )


def count() -> pyarrow.Schema:
    """Create an Arrow Flight schema for `count`.

    Returns
    -------
    pyarrow.Schema
        The count schema.

    """
    return pyarrow.schema([pyarrow.field("count", pyarrow.int64())])


def partition() -> pyarrow.Schema:
    """Create an Arrow Flight schema for `partition`.

    Returns
    -------
    pyarrow.Schema
        The partition schema.

    """
    return pyarrow.schema(
        [
            pyarrow.field("channel", pyarrow.string(), nullable=False),
            pyarrow.field("data_type", pyarrow.string(), nullable=False),
            pyarrow.field("sample_rate", pyarrow.int32(), nullable=False),
            pyarrow.field("partition_id", pyarrow.string()),
        ]
    )


def publish() -> pyarrow.Schema:
    """Create an Arrow Flight schema for `publish`.

    Returns
    -------
    pyarrow.Schema
        The publish schema.

    """
    dtype = pyarrow.map_(pyarrow.string(), pyarrow.string())
    return pyarrow.schema([pyarrow.field("properties", dtype, nullable=False)])
