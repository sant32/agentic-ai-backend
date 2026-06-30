from taskiq_aio_pika import AioPikaBroker

broker = AioPikaBroker(
    "amqp://guest:guest@localhost:5672/"
)