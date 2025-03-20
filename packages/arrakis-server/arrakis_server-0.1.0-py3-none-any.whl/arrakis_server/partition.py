import bisect
import math
import random
import string
from collections import Counter, defaultdict
from collections.abc import Iterator
from typing import Any

import numpy

from .channel import Channel


def generate_partition_id(channel: Channel, producer_id: str) -> str:
    alphanum = string.ascii_uppercase + string.digits
    rand_id = "".join(random.SystemRandom().choice(alphanum) for _ in range(6))
    alpha_id = channel.name.split(":")[1][:3]  # first 3 characters
    return f"{channel.domain}_{producer_id}_{alpha_id}_{rand_id}"


def grouped(items: list[Any], n: int) -> Iterator[list[Any]]:
    for i in range(0, len(items), n):
        yield items[i : i + n]


def partition_channels(
    channels: list[Channel],
    max_channels: int,
    producer_id: str,
    partitions: dict[str, Channel] | None = None,
    partition_fraction: float = 0.8,
) -> dict[str, Channel]:
    if not partitions:
        partitions = {}

    # map channels to dtypes
    channels_by_dtype: dict[numpy.dtype | None, list[Channel]] = {}
    for channel in channels:
        channels_by_dtype.setdefault(channel.data_type, []).append(channel)

    # filter channels that aren't matched to an ID
    # handle each data type separately
    for subblock in channels_by_dtype.values():
        # filter channels that aren't matched to an ID
        subblock_group = {channel.name for channel in subblock}
        subpartitions = {
            channel: meta.partition_id
            for channel, meta in partitions.items()
            if channel in subblock_group
        }
        unmatched = [
            channel for channel in subblock if channel.name not in subpartitions
        ]
        part_count = Counter(subpartitions.values())
        ordered = sorted(list(subpartitions.keys()))

        # determine where channel would go in sorted order
        insert_pt = defaultdict(list)
        for channel in unmatched:
            idx = bisect.bisect_left(ordered, channel.name)
            insert_pt[idx].append(channel)

        # assign unmatched into existing or new partitions
        max_partition_size = int(math.floor(partition_fraction * max_channels))
        for idx, adjacent in insert_pt.items():
            insert_idx = min(idx, len(ordered) - 1)
            if insert_idx == -1:
                # no initial partitions
                partition_id = generate_partition_id(adjacent[0], producer_id)
            else:
                id_ = partitions[ordered[insert_idx]].partition_id
                assert isinstance(id_, str)
                partition_id = id_
            if part_count[partition_id] + len(adjacent) > max_channels:
                # assign to new partition
                for group in grouped(adjacent, max_partition_size):
                    partition_id = generate_partition_id(group[0], producer_id)
                    for channel in group:
                        partitions[channel.name] = Channel(
                            channel.name,
                            data_type=channel.data_type,
                            sample_rate=channel.sample_rate,
                            partition_id=partition_id,
                        )
                    part_count[partition_id] += len(group)
            else:
                # assign to existing partition
                for channel in adjacent:
                    partitions[channel.name] = Channel(
                        channel.name,
                        data_type=channel.data_type,
                        sample_rate=channel.sample_rate,
                        partition_id=partition_id,
                    )
                part_count[partition_id] += len(adjacent)

    return partitions
