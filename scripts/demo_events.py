from app.application.event_handlers.notification_handlers import NotificationFeedHandler
from app.domain.events.football_events import MatchFinishedEvent, TeamRegisteredEvent
from app.infrastructure.messaging.in_memory_event_bus import InMemoryEventBus


def audit_logger_handler(event):
    print(f"[AUDIT LOG] {type(event).__name__} qayd etildi -> vaqt: {event.occurred_at.strftime('%H:%M:%S')}")


def main():
    bus = InMemoryEventBus()
    notifications: list[dict] = []
    feed_handler = NotificationFeedHandler(store=notifications)

    # Bitta hodisaga 2 ta mustaqil obunachi ulaymiz
    bus.subscribe(TeamRegisteredEvent, feed_handler.on_team_registered)
    bus.subscribe(TeamRegisteredEvent, audit_logger_handler)
    bus.subscribe(MatchFinishedEvent, feed_handler.on_match_finished)
    bus.subscribe(MatchFinishedEvent, audit_logger_handler)

    print("1. TeamRegisteredEvent e'lon qilinmoqda...")
    bus.publish(TeamRegisteredEvent(team_id=1, team_name="Samarqand United", city="Samarqand"))

    print("\n2. MatchFinishedEvent e'lon qilinmoqda...")
    bus.publish(
        MatchFinishedEvent(
            tournament_id=1, match_id=1, home_team_id=1, away_team_id=2, home_score=3, away_score=1
        )
    )

    print(f"\nJami bildirishnomalar soni: {len(notifications)}")


if __name__ == "__main__":
    main()