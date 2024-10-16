import uuid
from typing import Any, Dict

from lib.pg import PgConnect
from pydantic import BaseModel


class UserProductCounters(BaseModel):
    user_id: uuid.UUID
    product_id: uuid.UUID
    product_name: str

class UserCategoryCounters(BaseModel):
    user_id: uuid.UUID
    category_id: uuid.UUID
    category_name: str

class OrderCdmBuilder:
    def __init__(self, dict: Dict) -> None:
        self._dict = dict
        self.order_ns_uuid = uuid.UUID('88888888-4444-4444-4444-121221121212')

    def _uuid(self, obj: Any) -> uuid.UUID:
        return uuid.uuid5(namespace=self.order_ns_uuid, name=str(obj))
    
    def user_product_counters(self) -> UserProductCounters:
        user_id = self._dict["user_id"]
        product_id = self._dict["product_id"]
        product_name = self._dict["product_name"]
        return UserProductCounters(
            user_id=self._uuid(user_id),
            product_id=self._uuid(product_id),
            product_name=product_name
        )
    
    def user_category_counters(self) -> UserCategoryCounters:
        user_id = self._dict["user_id"]
        category_name = self._dict["category_name"]
        return UserCategoryCounters(
            user_id=self._uuid(user_id),
            category_id=self._uuid(category_name),
            category_name=category_name
        )


class CdmRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db
    
    def user_product_counters_insert(self, user_product_counters: UserProductCounters) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO cdm.user_product_counters AS c (user_id, product_id, product_name, order_cnt)
                        VALUES (%(user_id)s, %(product_id)s, %(product_name)s, 1)
                        ON CONFLICT (user_id, product_id) DO UPDATE
                        SET
                            product_name = EXCLUDED.product_name,
                            order_cnt = c.order_cnt + EXCLUDED.order_cnt;
                        """,
                        {
                            'user_id': user_product_counters.user_id,
                            'product_id': user_product_counters.product_id,
                            'product_name': user_product_counters.product_name
                        }
                    )

    def user_category_counters_insert(self, user_category_counters: UserCategoryCounters) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO cdm.user_category_counters AS c (user_id, category_id, category_name, order_cnt)
                        VALUES (%(user_id)s, %(category_id)s, %(category_name)s, 1)
                        ON CONFLICT (user_id, category_id) DO UPDATE
                        SET
                            category_name = EXCLUDED.category_name,
                            order_cnt = c.order_cnt + EXCLUDED.order_cnt;
                        """,
                        {
                            'user_id': user_category_counters.user_id,
                            'category_id': user_category_counters.category_id,
                            'category_name': user_category_counters.category_name
                        }
                    )