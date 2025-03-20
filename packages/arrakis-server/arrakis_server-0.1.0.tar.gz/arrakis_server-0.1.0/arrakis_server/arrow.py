# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-server/-/raw/main/LICENSE

import itertools
import typing
from collections.abc import Generator, Iterable, Iterator

import pyarrow
from arrakis import Channel
from pyarrow import flight

from . import schemas

T = typing.TypeVar("T")


def batched(iterable: Iterable[T], n: int) -> Generator[Iterable[T], None, None]:
    """An implementation of python 3.12's itertools.batches.
    Taken from the python documentation for itertools recipies
    Given an Iterable object iterable, generate a series of
    Iterators that return chunks of 'n' items from iterable.
    The last batch may be smaller than n entries.
    """
    if n < 1:
        raise ValueError("n must be greater than or equal to 1")
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        yield batch


def create_metadata_batches(channels: Iterable[Channel]) -> list[pyarrow.RecordBatch]:
    """Create an array of record batch objects from channel metadata."""
    batches = []
    schema = schemas.find()
    for channel_batch in batched(channels, 1000):
        metadata = [
            (
                channel.name,
                channel.data_type.name,
                channel.sample_rate,
                channel.partition_id,
                channel.publisher,
            )
            for channel in channel_batch
        ]
        if metadata:
            names, dtypes, rates, partitions, publishers = map(list, zip(*metadata))
        else:
            names, dtypes, rates, partitions, publishers = [], [], [], [], []
        batch = pyarrow.RecordBatch.from_arrays(
            [
                pyarrow.array(names, type=schema.field("channel").type),
                pyarrow.array(dtypes, type=schema.field("data_type").type),
                pyarrow.array(rates, type=schema.field("sample_rate").type),
                pyarrow.array(partitions, type=schema.field("partition_id").type),
                pyarrow.array(publishers, type=schema.field("publisher").type),
            ],
            schema=schema,
        )
        batches.append(batch)
    return batches


def create_metadata_stream(channels: Iterable[Channel]) -> flight.RecordBatchStream:
    """Create a record batch stream from channel metadata."""
    return flight.RecordBatchStream(
        pyarrow.RecordBatchReader.from_batches(
            schemas.find(), create_metadata_batches(channels)
        )
    )


def read_all_chunks(
    reader: flight.MetadataRecordBatchReader,
) -> Iterator[pyarrow.RecordBatch]:
    while True:
        try:
            batch, _ = reader.read_chunk()
            yield batch
        except StopIteration:
            return
