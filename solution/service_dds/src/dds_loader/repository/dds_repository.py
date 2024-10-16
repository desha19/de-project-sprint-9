import uuid
from datetime import datetime
from typing import Any, Dict, List

from lib.pg import PgConnect
from pydantic import BaseModel


class H_User(BaseModel):
    h_user_pk: uuid.UUID
    user_id: str
    load_dt: datetime
    load_src: str

class H_Product(BaseModel):
    h_product_pk: uuid.UUID
    product_id: str
    load_dt: datetime
    load_src: str

class H_Category(BaseModel):
    h_category_pk: uuid.UUID
    category_name: str
    load_dt: datetime
    load_src: str

class H_Restaurant(BaseModel):
    h_restaurant_pk: uuid.UUID
    restaurant_id: str
    load_dt: datetime
    load_src: str

class H_Order(BaseModel):
    h_order_pk: uuid.UUID
    order_id: int
    order_dt: datetime
    load_dt: datetime
    load_src: str

class L_OrderProduct(BaseModel):
    hk_order_product_pk: uuid.UUID
    order_id: int
    product_id: str
    load_dt: datetime
    load_src: str

class L_ProductRestaurant(BaseModel):
    hk_product_restaurant_pk: uuid.UUID
    product_id: str
    restaurant_id: str
    load_dt: datetime
    load_src: str

class L_ProductCategory(BaseModel):
    hk_product_category_pk: uuid.UUID
    product_id: str
    category_name: str
    load_dt: datetime
    load_src: str

class L_OrderUser(BaseModel):
    hk_order_user_pk: uuid.UUID
    order_id: int
    user_id: str
    load_dt: datetime
    load_src: str

class S_UserNames(BaseModel):
    user_id: str
    username: str
    userlogin: str
    load_dt: datetime
    load_src: str
    hk_user_names_hashdiff: uuid.UUID

class S_ProductNames(BaseModel):
    product_id: str
    name: str
    load_dt: datetime
    load_src: str
    hk_product_names_hashdiff: uuid.UUID

class S_RestaurantNames(BaseModel):
    restaurant_id: str
    name: str
    load_dt: datetime
    load_src: str
    hk_restaurant_names_hashdiff: uuid.UUID

class S_OrderCost(BaseModel):
    order_id: int
    cost: float
    payment: float
    load_dt: datetime
    load_src: str
    hk_order_cost_hashdiff: uuid.UUID

class S_OrderStatus(BaseModel):
    order_id: int
    status: str
    load_dt: datetime
    load_src: str
    hk_order_status_hashdiff: uuid.UUID

class OrderDdsBuilder:
    def __init__(self, dict: Dict) -> None:
        self._dict = dict
        self.source_system = "orders-system-kafka"
        self.order_ns_uuid = uuid.UUID('88888888-4444-4444-4444-121221121212')

    def _uuid(self, obj: Any) -> uuid.UUID:
        return uuid.uuid5(namespace=self.order_ns_uuid, name=str(obj))
    
    def h_user(self) -> H_User:
        user_id = self._dict["payload"]["user"]["id"]
        return H_User(
            h_user_pk=self._uuid(user_id),
            user_id=user_id,
            load_dt=datetime.utcnow(),
            load_src=self.source_system
        )
    
    def h_product(self) -> List[H_Product]:
        products = []
        for prod_dict in self._dict["payload"]["products"]:
            prod_id = prod_dict["id"]
            products.append(
                H_Product(
                    h_product_pk=self._uuid(prod_id),
                    product_id=prod_id,
                    load_dt=datetime.utcnow(),
                    load_src=self.source_system
                )
            )
        return products
    
    def h_category(self) -> List[H_Category]:
        categories = []
        for prod_dict in self._dict["payload"]["products"]:
            category = prod_dict["category"]
            categories.append(
                H_Category(
                    h_category_pk=self._uuid(category),
                    category_name=category,
                    load_dt=datetime.utcnow(),
                    load_src=self.source_system
                )
            )
        return categories
    
    def h_restaurant(self) -> H_Restaurant:
        restaurant_id = self._dict["payload"]["restaurant"]["id"]
        return H_Restaurant(
            h_restaurant_pk=self._uuid(restaurant_id),
            restaurant_id=restaurant_id,
            load_dt=datetime.utcnow(),
            load_src=self.source_system
        )
    
    def h_order(self) -> H_Order:
        order_id = self._dict["payload"]["id"]
        order_dt = self._dict["payload"]["date"]
        return H_Order(
            h_order_pk=self._uuid(str(order_id) + str(order_dt)),
            order_id=order_id,
            order_dt=order_dt,
            load_dt=datetime.utcnow(),
            load_src=self.source_system
        )
    
    def l_order_product(self) -> List[L_OrderProduct]:
        order_id = self._dict["payload"]["id"]
        order_dt = self._dict["payload"]["date"]
        l_order_products = []
        for prod_dict in self._dict["payload"]["products"]:
            prod_id = prod_dict["id"]
            l_order_products.append(
                L_OrderProduct(
                    hk_order_product_pk=self._uuid(str(order_id) + str(order_dt)+prod_id),
                    order_id=order_id,
                    product_id=prod_id,
                    load_dt=datetime.utcnow(),
                    load_src=self.source_system
                )
            )
        return l_order_products
    
    def l_product_restaurant(self) -> List[L_ProductRestaurant]:
        restaurant_id = self._dict["payload"]["restaurant"]["id"]
        l_product_restaurants = []
        for prod_dict in self._dict["payload"]["products"]:
            prod_id = prod_dict["id"]
            l_product_restaurants.append(
                L_ProductRestaurant(
                    hk_product_restaurant_pk=self._uuid(restaurant_id + prod_id),
                    product_id=prod_id,
                    restaurant_id=restaurant_id,
                    load_dt=datetime.utcnow(),
                    load_src=self.source_system
                )
            )
        return l_product_restaurants
    
    def l_product_category(self) -> List[L_ProductCategory]:
        l_product_categories = []
        for prod_dict in self._dict["payload"]["products"]:
            prod_id = prod_dict["id"]
            category = prod_dict["category"]
            l_product_categories.append(
                L_ProductCategory(
                    hk_product_category_pk=self._uuid(category + prod_id),
                    product_id=prod_id,
                    category_name=category,
                    load_dt=datetime.utcnow(),
                    load_src=self.source_system
                )
            )
        return l_product_categories
    
    def l_order_user(self) -> L_OrderUser:
        user_id = self._dict["payload"]["user"]["id"]
        order_id = self._dict["payload"]["id"]
        return L_OrderUser(
            hk_order_user_pk=self._uuid(str(order_id) + user_id),
            user_id=user_id,
            order_id=order_id,
            load_dt=datetime.utcnow(),
            load_src=self.source_system
        )
    
    def s_user_names(self) -> S_UserNames:
        user_id = self._dict["payload"]["user"]["id"]
        name = self._dict["payload"]["user"]["name"]
        login = self._dict["payload"]["user"]["login"]
        return S_UserNames(
            user_id=user_id,
            username=name,
            userlogin=login,
            load_dt=datetime.utcnow(),
            load_src=self.source_system,
            hk_user_names_hashdiff=self._uuid(name + login + user_id)
        )
    
    def s_product_names(self) -> List[S_ProductNames]:
        s_product_names = []
        for prod_dict in self._dict["payload"]["products"]:
            prod_id = prod_dict["id"]
            name = prod_dict["name"]
            s_product_names.append(
                S_ProductNames(
                    product_id=prod_id,
                    name=name,
                    load_dt=datetime.utcnow(),
                    load_src=self.source_system,
                    hk_product_names_hashdiff = self._uuid(name + prod_id)
                )
            )
        return s_product_names
    
    def s_restaurant_names(self) -> S_RestaurantNames:
        restaurant_id = self._dict["payload"]["restaurant"]["id"]
        name = self._dict["payload"]["restaurant"]["name"]
        return S_RestaurantNames(
            restaurant_id=restaurant_id,
            name=name,
            load_dt=datetime.utcnow(),
            load_src=self.source_system,
            hk_restaurant_names_hashdiff=self._uuid(name + restaurant_id)
        )
    
    def s_order_cost(self) -> S_OrderCost:
        order_id = self._dict["payload"]["id"]
        cost = self._dict["payload"]["cost"]
        payment = self._dict["payload"]["payment"]
        return S_OrderCost(
            order_id=order_id,
            cost=cost,
            payment=payment,
            load_dt=datetime.utcnow(),
            load_src=self.source_system,
            hk_order_cost_hashdiff=self._uuid(str(cost) + str(payment) + str(order_id))
        )
    
    def s_order_status(self) -> S_OrderStatus:
        order_id = self._dict["payload"]["id"]
        status = self._dict["payload"]["status"]
        return S_OrderStatus(
            order_id=order_id,
            status=status,
            load_dt=datetime.utcnow(),
            load_src=self.source_system,
            hk_order_status_hashdiff=self._uuid(status + str(order_id))
        )


class DdsRepository:
    def __init__(self, db: PgConnect) -> None:
        self._db = db

    def h_user_insert(self, user:H_User) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.h_user (h_user_pk, user_id, load_dt, load_src)
                        VALUES (%(h_user_pk)s, %(user_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (user_id) DO NOTHING;
                        """,
                        {
                            'h_user_pk': user.h_user_pk,
                            'user_id': user.user_id,
                            'load_dt': user.load_dt,
                            'load_src': user.load_src
                        }
                    )
    
    def h_product_insert(self, product:H_Product) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.h_product (h_product_pk, product_id, load_dt, load_src)
                        VALUES (%(h_product_pk)s, %(product_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (product_id) DO NOTHING;
                        """,
                        {
                            'h_product_pk': product.h_product_pk,
                            'product_id': product.product_id,
                            'load_dt': product.load_dt,
                            'load_src': product.load_src
                        }
                    )
    
    def h_category_insert(self, category:H_Category) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.h_category (h_category_pk, category_name, load_dt, load_src)
                        VALUES (%(h_category_pk)s, %(category_name)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (category_name) DO NOTHING;
                        """,
                        {
                            'h_category_pk': category.h_category_pk,
                            'category_name': category.category_name,
                            'load_dt': category.load_dt,
                            'load_src': category.load_src
                        }
                    )

    def h_restaurant_insert(self, restaurant: H_Restaurant) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.h_restaurant (h_restaurant_pk, restaurant_id, load_dt, load_src)
                        VALUES (%(h_restaurant_pk)s, %(restaurant_id)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (restaurant_id) DO NOTHING;
                        """,
                        {
                            'h_restaurant_pk': restaurant.h_restaurant_pk,
                            'restaurant_id': restaurant.restaurant_id,
                            'load_dt': restaurant.load_dt,
                            'load_src': restaurant.load_src
                        }
                    )
    
    def h_order_insert(self, order: H_Order) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.h_order (h_order_pk, order_id, order_dt, load_dt, load_src)
                        VALUES (%(h_order_pk)s, %(order_id)s, %(order_dt)s, %(load_dt)s, %(load_src)s)
                        ON CONFLICT (order_id, order_dt) DO NOTHING;
                        """,
                        {
                            'h_order_pk': order.h_order_pk,
                            'order_id': order.order_id,
                            'order_dt': order.order_dt,
                            'load_dt': order.load_dt,
                            'load_src': order.load_src
                        }
                    )
    
    def l_order_product_insert(self, l_order_product: L_OrderProduct) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.l_order_product (hk_order_product_pk, h_order_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_order_product_pk)s, 
                                (select h_order_pk from dds.h_order where order_id=%(order_id)s limit 1), 
                                (select h_product_pk from dds.h_product where product_id=%(product_id)s limit 1), 
                                %(load_dt)s, 
                                %(load_src)s)
                        ON CONFLICT (h_order_pk, h_product_pk) DO NOTHING;
                        """,
                        {
                            'hk_order_product_pk': l_order_product.hk_order_product_pk,
                            'order_id': l_order_product.order_id,
                            'product_id': l_order_product.product_id,
                            'load_dt': l_order_product.load_dt,
                            'load_src': l_order_product.load_src
                        }
                    )

    def l_product_restaurant_insert(self, l_product_restaurant: L_ProductRestaurant) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.l_product_restaurant (hk_product_restaurant_pk, h_restaurant_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_product_restaurant_pk)s, 
                                (select h_restaurant_pk from dds.h_restaurant where restaurant_id=%(restaurant_id)s limit 1), 
                                (select h_product_pk from dds.h_product where product_id=%(product_id)s limit 1), 
                                %(load_dt)s, 
                                %(load_src)s)
                        ON CONFLICT (h_restaurant_pk, h_product_pk) DO NOTHING;
                        """,
                        {
                            'hk_product_restaurant_pk': l_product_restaurant.hk_product_restaurant_pk,
                            'restaurant_id': l_product_restaurant.restaurant_id,
                            'product_id': l_product_restaurant.product_id,
                            'load_dt': l_product_restaurant.load_dt,
                            'load_src': l_product_restaurant.load_src
                        }
                    )
    
    def l_product_category_insert(self, l_product_category: L_ProductCategory) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.l_product_category (hk_product_category_pk, h_category_pk, h_product_pk, load_dt, load_src)
                        VALUES (%(hk_product_category_pk)s, 
                                (select h_category_pk from dds.h_category where category_name=%(category_name)s limit 1), 
                                (select h_product_pk from dds.h_product where product_id=%(product_id)s limit 1), 
                                %(load_dt)s, 
                                %(load_src)s)
                        ON CONFLICT (h_category_pk, h_product_pk) DO NOTHING;
                        """,
                        {
                            'hk_product_category_pk': l_product_category.hk_product_category_pk,
                            'category_name': l_product_category.category_name,
                            'product_id': l_product_category.product_id,
                            'load_dt': l_product_category.load_dt,
                            'load_src': l_product_category.load_src
                        }
                    )
    
    def l_order_user_insert(self, l_order_user: L_OrderUser) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.l_order_user (hk_order_user_pk, h_order_pk, h_user_pk, load_dt, load_src)
                        VALUES (%(hk_order_user_pk)s, 
                                (select h_order_pk from dds.h_order where order_id=%(order_id)s limit 1), 
                                (select h_user_pk from dds.h_user where user_id=%(user_id)s limit 1), 
                                %(load_dt)s, 
                                %(load_src)s)
                        ON CONFLICT (h_order_pk, h_user_pk) DO NOTHING;
                        """,
                        {
                            'hk_order_user_pk': l_order_user.hk_order_user_pk,
                            'order_id': l_order_user.order_id,
                            'user_id': l_order_user.user_id,
                            'load_dt': l_order_user.load_dt,
                            'load_src': l_order_user.load_src
                        }
                    )

    def s_user_names_insert(self, user: S_UserNames) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.s_user_names (h_user_pk, username, userlogin, load_dt, load_src, hk_user_names_hashdiff)
                        VALUES ((SELECT h_user_pk FROM dds.h_user WHERE user_id=%(user_id)s LIMIT 1),
                                %(username)s,
                                %(userlogin)s,
                                %(load_dt)s, 
                                %(load_src)s,
                                %(hk_user_names_hashdiff)s
                                )
                        ON CONFLICT (h_user_pk) DO UPDATE
                        SET
                            username = EXCLUDED.username,
                            userlogin = EXCLUDED.userlogin,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_user_names_hashdiff = EXCLUDED.hk_user_names_hashdiff;
                        """,
                        {
                            'user_id': user.user_id,
                            'username': user.username,
                            'userlogin': user.userlogin,
                            'load_dt': user.load_dt,
                            'load_src': user.load_src,
                            'hk_user_names_hashdiff': user.hk_user_names_hashdiff
                        }
                    )
    
    def s_product_names_insert(self, product: S_ProductNames) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.s_product_names (h_product_pk, name, load_dt, load_src, hk_product_names_hashdiff)
                        VALUES ((SELECT h_product_pk FROM dds.h_product WHERE product_id=%(product_id)s LIMIT 1),
                                %(name)s,
                                %(load_dt)s, 
                                %(load_src)s,
                                %(hk_product_names_hashdiff)s
                                )
                        ON CONFLICT (h_product_pk) DO UPDATE
                        SET
                        name = EXCLUDED.name,
                        load_dt = EXCLUDED.load_dt,
                        load_src = EXCLUDED.load_src,
                        hk_product_names_hashdiff = EXCLUDED.hk_product_names_hashdiff;
                        """,
                        {
                            'product_id': product.product_id,
                            'name': product.name,
                            'load_dt': product.load_dt,
                            'load_src': product.load_src,
                            'hk_product_names_hashdiff': product.hk_product_names_hashdiff
                        }
                    )

    def s_restaurant_names_insert(self, s_restaurant_names: S_RestaurantNames) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.s_restaurant_names (h_restaurant_pk, name, load_dt, load_src, hk_restaurant_names_hashdiff)
                        VALUES ((SELECT h_restaurant_pk FROM dds.h_restaurant WHERE restaurant_id=%(restaurant_id)s),
                                %(name)s,
                                %(load_dt)s, 
                                %(load_src)s,
                                %(hk_restaurant_names_hashdiff)s
                                )
                        ON CONFLICT (h_restaurant_pk) DO UPDATE
                        SET
                            name = EXCLUDED.name,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_restaurant_names_hashdiff = EXCLUDED.hk_restaurant_names_hashdiff;
                        """,
                        {
                            'restaurant_id': s_restaurant_names.restaurant_id,
                            'name': s_restaurant_names.name,
                            'load_dt': s_restaurant_names.load_dt,
                            'load_src': s_restaurant_names.load_src,
                            'hk_restaurant_names_hashdiff': s_restaurant_names.hk_restaurant_names_hashdiff
                        }
                    )

    def s_order_cost_insert(self, s_order_cost: S_OrderCost) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.s_order_cost (h_order_pk, cost, payment, load_dt, load_src, hk_order_cost_hashdiff)
                        VALUES ((SELECT h_order_pk FROM dds.h_order WHERE order_id=%(order_id)s LIMIT 1),
                                %(cost)s,
                                %(payment)s,
                                %(load_dt)s, 
                                %(load_src)s,
                                %(hk_order_cost_hashdiff)s
                                )
                        ON CONFLICT (h_order_pk) DO UPDATE
                        SET
                        cost = EXCLUDED.cost,
                        payment = EXCLUDED.payment,
                        load_dt = EXCLUDED.load_dt,
                        load_src = EXCLUDED.load_src,
                        hk_order_cost_hashdiff = EXCLUDED.hk_order_cost_hashdiff;
                        """,
                        {
                            'order_id': s_order_cost.order_id,
                            'cost': s_order_cost.cost,
                            'payment': s_order_cost.payment,
                            'load_dt': s_order_cost.load_dt,
                            'load_src': s_order_cost.load_src,
                            'hk_order_cost_hashdiff': s_order_cost.hk_order_cost_hashdiff
                        }
                    )

    def s_order_status_insert(self, s_order_status: S_OrderStatus) -> None:
        with self._db.connection() as conn:
            with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO dds.s_order_status (h_order_pk, status, load_dt, load_src, hk_order_status_hashdiff)
                        VALUES ((SELECT h_order_pk FROM dds.h_order WHERE order_id=%(order_id)s LIMIT 1),
                                %(status)s,
                                %(load_dt)s, 
                                %(load_src)s,
                                %(hk_order_status_hashdiff)s
                                )
                        ON CONFLICT (h_order_pk) DO UPDATE
                        SET
                        status = EXCLUDED.status,
                            load_dt = EXCLUDED.load_dt,
                            load_src = EXCLUDED.load_src,
                            hk_order_status_hashdiff = EXCLUDED.hk_order_status_hashdiff;
                        """,
                        {
                            'order_id': s_order_status.order_id,
                            'status': s_order_status.status,
                            'load_dt': s_order_status.load_dt,
                            'load_src': s_order_status.load_src,
                            'hk_order_status_hashdiff': s_order_status.hk_order_status_hashdiff
                        }
                    )