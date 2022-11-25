import pytz

from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4


@dataclass(frozen=True)
class EntityID:
    id: str = None

    @classmethod
    def generate(cls):
        _id = str(uuid4())

        return cls(id=_id)

    @classmethod
    def from_text(cls, raw_id):
        if not isinstance(raw_id, str):
            raise ValueError("Invalid uuid")

        return cls(id=raw_id)


@dataclass
class Entity:
    created_at: str = None
    updated_at: str = None

    def calculate_created_at(self):
        date_time_obj = datetime.utcnow()
        date_time_obj = date_time_obj.astimezone(pytz.timezone('America/Lima'))
        time_stamp_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        self.created_at = time_stamp_str
        self.updated_at = time_stamp_str

    def calculate_updated_at(self):
        date_time_obj = datetime.utcnow()
        date_time_obj = date_time_obj.astimezone(pytz.timezone('America/Lima'))
        time_stamp_str = date_time_obj.strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = time_stamp_str
