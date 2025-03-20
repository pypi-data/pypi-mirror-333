import json
import logging
from abc import ABC, abstractmethod
from typing import Union

import aio_pika

from rabbit_broker.queues.models import PersistentQueueModel
from rabbit_broker.settings import RABBIT_URL

logger = logging.getLogger(__name__)


class AsyncAbstractPersistentQueue(ABC):
    def __init__(self, properties: PersistentQueueModel = None):
        self.broker_url = RABBIT_URL
        self.connection = None
        self.properties = properties or PersistentQueueModel()
        logger.debug("%s.%s: Initialized", self.__class__.__name__, self.__init__.__name__)

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def post_message(self):
        pass


class AsyncPersistentQueue(AsyncAbstractPersistentQueue):
    async def __aenter__(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.broker_url)
            logger.info("%s.%s: Created robust connection", self.__class__.__name__, self.__aenter__.__name__)
            self.channel = await self.connection.channel()

            for queue_name in self.properties.queues_to_declare:
                await self.channel.declare_queue(queue_name, durable=True)
                await self.channel.declare_queue(queue_name, durable=True)

        return self

    async def __aexit__(self, *args, **kwargs):
        await self.connection.close()
        await self.channel.close()

    async def post_message(self, queue_name: str, data: dict) -> None:
        json_body = json.dumps(data).encode("utf-8")
        message = aio_pika.Message(body=json_body, delivery_mode=aio_pika.DeliveryMode.PERSISTENT)
        await self.channel.default_exchange.publish(message, routing_key=queue_name)

    async def peek_message(self, queue_name) -> Union[str, None]:
        queue = await self.channel.get_queue(queue_name)
        message = await queue.get(no_ack=False)

        decoded_message = None

        if message:
            decoded_message = message.body.decode("utf-8")
            await message.nack(requeue=True)

        return decoded_message
