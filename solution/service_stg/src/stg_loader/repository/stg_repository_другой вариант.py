import os
from datetime import datetime
import json

from pydantic import BaseModel
from typing import Dict

from lib.pg import PgConnect


class OrderEvents(BaseModel):
    object_id: int
    object_type: str
    sent_dttm: datetime
    payload: str

class OrderStgBuilder:
    def __init__(self, dict: Dict) -> None:
        self._dict = dict
    def order_events(self) -> OrderEvents:
        return OrderEvents(
            object_id=self._dict["object_id"],
            object_type=self._dict["object_type"],
            sent_dttm=self._dict["sent_dttm"],
            payload=json.dumps(self._dict["payload"])
        )

class StgRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def order_events_insert(self,
                            order_events: OrderEvents
                            ) -> None:

        with self._db.connection() as conn:
            with conn.cursor() as cur:
                with open(os.path.dirname(os.path.abspath(__file__)) + "/sql/order_events_insert.sql", "r") as script:
                    cur.execute(
                        script.read(),
                        {
                            'object_id': order_events.object_id,
                            'object_type': order_events.object_type,
                            'sent_dttm': order_events.sent_dttm,
                            'payload': order_events.payload
                        }
                    )