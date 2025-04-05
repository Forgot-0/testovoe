from dataclasses import dataclass
from taskiq import AsyncBroker

from app.core.services.queue.task import BaseTask


@dataclass
class TaskiqQueuedDecorator:
    broker: AsyncBroker

    def __call__(self, cls: type[BaseTask]) -> type[BaseTask]:

        if cls.get_schedule() is not None:
            schedule_cron = cls.get_schedule()
            self.broker.register_task(
                func=cls().run,
                task_name=cls.get_name(),
                schedule=[{"cron": schedule_cron}],
            )
            return cls

        self.broker.register_task(func=cls().run, task_name=cls.get_name())
        return cls