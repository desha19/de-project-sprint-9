from datetime import datetime

from logging import Logger

from lib.kafka_connect.kafka_connectors import KafkaConsumer, KafkaProducer 
from lib.redis.redis_client import RedisClient
from stg_loader.repository.stg_repository import StgRepository, OrderStgBuilder

class StgMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 redis: RedisClient,
                 stg_repository: StgRepository,
                 batch_size: int,
                 logger: Logger) -> None:
        self._logger = logger
        self._consumer = consumer
        self._producer = producer
        self._redis = redis
        self._stg_repository = stg_repository
        self._batch_size = batch_size

    # функция, которая будет вызываться по расписанию.
    def run(self) -> None:
        # Пишем в лог, что джоб был запущен.
        self._logger.info(f"{datetime.utcnow()}: START")

        # Имитация работы. Здесь будет реализована обработка сообщений.
        for _ in range(self._batch_size):
            msg = self._consumer.consume()

            if msg is None:
                break
            if "object_id" in msg:
                self._logger.info(msg)
                msg_insert_db = OrderStgBuilder(msg).order_events()
                self._stg_repository.order_events_insert(msg_insert_db)
                user_id = msg["payload"]["user"]["id"]
                user_data = self._redis.get(user_id)
                restaurant_id = msg["payload"]["restaurant"]["id"]
                restaurant_data = self._redis.get(restaurant_id)
                products = []
                for product in msg["payload"]["order_items"]:
                    product["category"] = [x["category"] for x in restaurant_data["menu"] if x["_id"]==product["id"]][0]
                    products.append(product)

                next_message = {
                    "object_id": msg["object_id"],
                    "object_type": msg["object_type"],
                    "payload": {
                        "id": msg["object_id"],
                        "date": msg["payload"]["date"],
                        "cost": msg["payload"]["cost"],
                        "payment": msg["payload"]["payment"],
                        "status": msg["payload"]["final_status"],
                        "restaurant": {
                            "id": restaurant_data["_id"],
                            "name": restaurant_data["name"],
                        },
                        "user": {"id": user_data["_id"], 
                                 "name": user_data["name"],
                                 "login": user_data["login"]},
                        "products": products
                    }
                }

                self._logger.info(next_message)
                self._producer.produce(next_message)


        # Пишем в лог, что джоб успешно завершен.
        self._logger.info(f"{datetime.utcnow()}: FINISH")