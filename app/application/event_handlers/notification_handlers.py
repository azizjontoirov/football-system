from app.domain.events.football_events import MatchFinishedEvent, TeamRegisteredEvent


class NotificationFeedHandler:
    """Hodisalarni qabul qilib, tizim bildirishnomalari lentasiga yozuvchi obunachi."""

    def __init__(self, store: list[dict]):
        self.store = store

    def on_team_registered(self, event: TeamRegisteredEvent) -> None:
        message = (
            f"Yangi jamoa ro'yxatdan o'tdi: '{event.team_name}' ({event.city}, ID={event.team_id})"
        )
        self.store.append(
            {
                "event_type": "TeamRegisteredEvent",
                "message": message,
                "occurred_at": event.occurred_at.isoformat(),
            }
        )
        print(f"[EVENT] {message}")

    def on_match_finished(self, event: MatchFinishedEvent) -> None:
        message = (
            f"Uchrashuv #{event.match_id} yakunlandi (Turnir #{event.tournament_id}): "
            f"Jamoa #{event.home_team_id} {event.home_score}:{event.away_score} Jamoa #{event.away_team_id}. "
            f"Turnir jadvali yangilandi."
        )
        self.store.append(
            {
                "event_type": "MatchFinishedEvent",
                "message": message,
                "occurred_at": event.occurred_at.isoformat(),
            }
        )
        print(f"[EVENT] {message}")