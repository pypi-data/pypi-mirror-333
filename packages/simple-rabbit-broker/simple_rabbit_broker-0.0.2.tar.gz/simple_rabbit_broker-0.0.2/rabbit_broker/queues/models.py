from typing import List, Optional

from pydantic import BaseModel, Field


class PersistentQueueModel(BaseModel):
    queues_to_declare: Optional[List[str]] = Field(
        default_factory=list, description="Queue that will be created, if not existe"
    )
