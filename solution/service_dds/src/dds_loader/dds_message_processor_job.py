from datetime import datetime
from logging import Logger
from lib.kafka_connect.kafka_connectors import KafkaConsumer, KafkaProducer
from dds_loader.repository.dds_repository import DdsRepository, OrderDdsBuilder


class DdsMessageProcessor:
    def __init__(self,
                 consumer: KafkaConsumer,
                 producer: KafkaProducer,
                 dds_repository: DdsRepository,
                 batch_size: int,
                 logger: Logger) -> None:
        self._consumer = consumer
        self._producer = producer
        self._dds_repository = dds_repository
        self._logger = logger
        self._batch_size = batch_size

    def run(self) -> None:
        self._logger.info(f"{datetime.utcnow()}: START")

        for _ in range(self._batch_size):
            msg = self._consumer.consume()
            self._logger.info(msg)
            if msg is None:
                break
            if msg.get("object_id"):
                order_dds_buider = OrderDdsBuilder(msg)
                self._dds_repository.h_user_insert(order_dds_buider.h_user())
                for product in order_dds_buider.h_product():
                    self._dds_repository.h_product_insert(product)
                for category in order_dds_buider.h_category():
                    self._dds_repository.h_category_insert(category)
                self._dds_repository.h_restaurant_insert(order_dds_buider.h_restaurant())
                self._dds_repository.h_order_insert(order_dds_buider.h_order())
                for l_order_product in order_dds_buider.l_order_product():
                    self._dds_repository.l_order_product_insert(l_order_product)
                for l_product_restaurant in order_dds_buider.l_product_restaurant():
                    self._dds_repository.l_product_restaurant_insert(l_product_restaurant)
                for l_product_category in order_dds_buider.l_product_category():
                    self._dds_repository.l_product_category_insert(l_product_category)
                self._dds_repository.l_order_user_insert(order_dds_buider.l_order_user())
                self._dds_repository.s_user_names_insert(order_dds_buider.s_user_names())
                for s_product_names in order_dds_buider.s_product_names():
                    self._dds_repository.s_product_names_insert(s_product_names)
                self._dds_repository.s_restaurant_names_insert(order_dds_buider.s_restaurant_names())
                self._dds_repository.s_order_cost_insert(order_dds_buider.s_order_cost())
                self._dds_repository.s_order_status_insert(order_dds_buider.s_order_status())

                for product in msg["payload"]["products"]:
                    message_user_product_counters = {
                        "type": "user_product_counters",
                        "user_id": msg["payload"]["user"]["id"],
                        "product_id": product["id"],
                        "product_name": product["name"]
                    }
                    self._producer.produce(message_user_product_counters)

                    message_user_category_counters = {
                        "type": "user_category_counters",
                        "user_id": msg["payload"]["user"]["id"],
                        "category_name": product["category"]
                    }
                    self._producer.produce(message_user_category_counters)

        self._logger.info(f"{datetime.utcnow()}: FINISH")