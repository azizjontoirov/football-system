from abc import ABC, abstractmethod
from typing import Callable, Type

from app.domain.events.football_events import DomainEvent

EventHandler = Callable[[DomainEvent], None]


class EventBusPort(ABC):
    """Hodisalarni nashr etish va ularga obuna bo'lish interfeysi."""

    @abstractmethod
    def subscribe(self, event_type: Type[DomainEvent], handler: EventHandler) -> None:
        pass

    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        pass