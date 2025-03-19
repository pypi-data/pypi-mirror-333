# Copyright (c) 2022, California Institute of Technology and contributors
#
# You should have received a copy of the licensing terms for this
# software included in the file "LICENSE" located in the top-level
# directory of this package. If you did not, you can view a copy at
# https://git.ligo.org/ngdd/arrakis-python/-/raw/main/LICENSE

"""Publisher API."""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Literal

import pyarrow
from pyarrow.flight import connect

from . import constants
from .client import Client
from .flight import MultiEndpointStream, RequestType, create_descriptor, parse_url

try:
    from confluent_kafka import Producer
except ImportError:
    HAS_KAFKA = False
else:
    HAS_KAFKA = True

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import timedelta

    from .block import SeriesBlock
    from .channel import Channel


def serialize_batch(batch: pyarrow.RecordBatch):
    """Serialize a record batch to bytes.

    Parameters
    ----------
    batch : pyarrow.RecordBatch
        The batch to serialize.

    Returns
    -------
    bytes
        The serialized buffer.

    """
    sink = pyarrow.BufferOutputStream()
    with pyarrow.ipc.new_stream(sink, batch.schema) as writer:
        writer.write_batch(batch)
    return sink.getvalue()


def channel_to_dtype_name(channel: Channel) -> str:
    """Given a channel, return the data type's name."""
    assert channel.data_type is not None
    return channel.data_type.name


class Publisher:
    """Publisher to publish timeseries to Arrakis service.

    Parameters
    ----------
    url : str
        Initial Flight URL to connect to.

    """

    def __init__(self, url: str | None = None):
        if not HAS_KAFKA:
            msg = (
                "Publishing requires confluent-kafka to be installed."
                "This is provided by the 'publish' extra or it can be "
                "installed manually through pip or conda."
            )
            raise ImportError(msg)
        self._producer: Producer

        self.initial_url = parse_url(url)

        # validation checks for publishing
        self._channels: set[Channel] = set()

        # registry
        self._registered = False
        self._publisher_id: str
        self._partitions: dict[str, str]

    def register(self, publisher_id: str):
        assert not self._registered, "has already registered"

        # set up producer
        self._publisher_id = publisher_id
        properties = self._get_connection_properties(publisher_id)
        self._producer = Producer(
            {
                "message.max.bytes": 10_000_000,  # 10 MB
                "enable.idempotence": True,
                **properties,
            }
        )

        # query for the current partition mapping
        # FIXME: maybe we can just do what we need internally here
        # without needing to use the Client interface.
        self._partitions = {}
        for channel in Client(self.initial_url).find(publisher=publisher_id):
            if channel.partition_id:
                self._partitions[channel.name] = channel.partition_id

        self._registered = True

    def publish(
        self,
        block: SeriesBlock,
        timeout: timedelta = constants.DEFAULT_TIMEOUT,
    ) -> None:
        """Publish timeseries data

        Parameters
        ----------
        block : SeriesBlock
            A data block with all channels to publish.
        timeout : timedelta, optional
            The maximum time to wait to publish before timing out.
            Default is 2 seconds.

        """
        assert self._registered, "client needs to register prior to publishing data"

        # check for new metadata changes
        channels = set(block.channels.values())
        if channels != self._channels:
            changed = channels - self._channels

            # exchange to transfer metadata and get new/updated partition IDs
            if changed:
                self._update_partitions(changed)

            # update tracked metadata
            self._channels = channels

        # publish data for each data type, splitting into
        # subblocks based on a maximum channel maximum
        for partition_id, batch in block.to_row_batches(self._partitions):
            self._publish_data(partition_id, batch)

    def _publish_data(self, partition_id: str, batch: pyarrow.RecordBatch) -> None:
        """Publish data for a given data type."""
        topic = f"arrakis-{partition_id}"
        self._producer.produce(topic=topic, value=serialize_batch(batch))

    def _update_partitions(self, channels: Iterable[Channel]) -> None:
        # set up flight
        assert self._registered, "has not registered yet"
        descriptor = create_descriptor(
            RequestType.Partition,
            publisher=self._publisher_id,
        )
        # FIXME: should we not get FlightInfo first?
        with connect(self.initial_url) as client:
            writer, reader = client.do_exchange(descriptor)

        # send over list of channels to map new/updated partitions for
        dtypes = [channel_to_dtype_name(channel) for channel in channels]
        schema = pyarrow.schema(
            [
                pyarrow.field("channel", pyarrow.string(), nullable=False),
                pyarrow.field("data_type", pyarrow.string(), nullable=False),
                pyarrow.field("sample_rate", pyarrow.int32(), nullable=False),
                pyarrow.field("partition_id", pyarrow.string()),
            ]
        )
        batch = pyarrow.RecordBatch.from_arrays(
            [
                pyarrow.array(
                    [str(channel) for channel in channels],
                    type=schema.field("channel").type,
                ),
                pyarrow.array(dtypes, type=schema.field("data_type").type),
                pyarrow.array(
                    [channel.sample_rate for channel in channels],
                    type=schema.field("sample_rate").type,
                ),
                pyarrow.array(
                    [None for _ in channels],
                    type=schema.field("partition_id").type,
                ),
            ],
            schema=schema,
        )

        # send over the partitions
        writer.begin(schema)
        writer.write_batch(batch)
        writer.done_writing()

        # get back the partition IDs and update
        partitions = reader.read_all().to_pydict()
        for channel, id_ in zip(partitions["channel"], partitions["partition_id"]):
            self._partitions[channel] = id_

    def _get_connection_properties(self, producer_id: str) -> dict[str, str]:
        """Query for producer connection properties."""
        descriptor = create_descriptor(
            RequestType.Publish,
            producer_id=producer_id,
        )
        properties: dict[str, str] = {}
        with connect(self.initial_url) as client:
            flight_info = client.get_flight_info(descriptor)
            with MultiEndpointStream(flight_info.endpoints, client) as stream:
                for data in stream.unpack():
                    kv_pairs = data["properties"]
                    properties.update(dict(kv_pairs))
        return properties

    def close(self) -> None:
        with contextlib.suppress(Exception):
            self._producer.flush()

    def __enter__(self) -> Publisher:
        return self

    def __exit__(self, *exc) -> Literal[False]:
        self.close()
        return False
