from collections import defaultdict
from typing import Type

from app.domain.events.football_events import DomainEvent
from app.domain.ports.event_bus import EventBusPort, EventHandler


class InMemoryEventBus(EventBusPort):
    """Xabarlarni ichki xotira orqali obunachilarga tarqatuvchi Event Bus."""

    def __init__(self):
        self._subscribers: dict[Type[DomainEvent], list[EventHandler]] = defaultdict(list)

    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event: DomainEvent) -> None:
        handlers = self._subscribers.get(type(event), [])
        for handler in handlers:
            handler(event)