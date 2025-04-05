from taskiq import AsyncBroker, InMemoryBroker, TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import ListQueueBroker, RedisAsyncResultBackend, RedisScheduleSource

from app.core.configs.app import app_config

broker: AsyncBroker


if app_config.ENVIRONMENT == 'testing':
    broker = InMemoryBroker()
else:
    broker = ListQueueBroker(url=app_config.QUEUE_REDIS_BROKER_URL)
    broker.with_result_backend(RedisAsyncResultBackend(app_config.QUEUE_REDIS_RESULT_BACKEND))

    redis_schedule_source = RedisScheduleSource(
        url=app_config.QUEUE_REDIS_BROKER_URL,
    )

    scheduler_taksiq = TaskiqScheduler(
        broker=broker,
        sources=[redis_schedule_source, LabelScheduleSource(broker=broker)],
    )
