import os
import logging

from pydantic_settings import BaseSettings
from kafka import KafkaProducer, KafkaConsumer

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s - %(funcName)s - %(message)s",
)

basedir = os.path.abspath(os.path.dirname(__file__))


class Settings(BaseSettings):
    DEBUG: bool = False
    DEVELOPMENT: bool = False
    TESTING: bool = False
    KAFKA_URL: str = os.getenv("KAFKA_URL", "localhost:9092")


settings = Settings()

producer_config = {
    "bootstrap_servers": settings.KAFKA_URL,
    "value_serializer": lambda v: v.encode("utf-8"),
}

camera_producer = KafkaProducer(**producer_config)
camera99_consumer = KafkaConsumer(
    "camera-40547499", bootstrap_servers=[settings.KAFKA_URL]
)
camera27_consumer = KafkaConsumer(
    "camera-40579627", bootstrap_servers=[settings.KAFKA_URL]
)
camera55_consumer = KafkaConsumer(
    "camera-40580655", bootstrap_servers=[settings.KAFKA_URL]
)

camera99_yolo_consumer = KafkaConsumer(
    "camera-40547499-yolo", bootstrap_servers=[settings.KAFKA_URL]
)
camera27_yolo_consumer = KafkaConsumer(
    "camera-40579627-yolo", bootstrap_servers=[settings.KAFKA_URL]
)
camera55_yolo_consumer = KafkaConsumer(
    "camera-40580655-yolo", bootstrap_servers=[settings.KAFKA_URL]
)
