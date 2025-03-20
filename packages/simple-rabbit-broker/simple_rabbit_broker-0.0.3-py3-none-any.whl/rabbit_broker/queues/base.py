import logging
from abc import ABC, abstractmethod

from rabbit_broker.settings import RABBIT_URL

logger = logging.getLogger(__name__)


class AsyncAbstractMessageQueue(ABC):
    MessageQueue: str = ""

    def __init__(self):
        self.broker_url = RABBIT_URL
        self.connection = None
        self.client_properties = None
        logger.debug("%s.%s: Initialized", self.__class__.__name__, self.__init__.__name__)

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def register_tasks(self, routing_key, worker):
        pass

    @abstractmethod
    async def consume(self):
        pass

    @abstractmethod
    async def post_message(self):
        pass
