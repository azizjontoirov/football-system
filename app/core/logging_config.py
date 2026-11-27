import json
import logging
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"


class JsonFormatter(logging.Formatter):
    """Log yozuvlarini strukturalangan JSON formatiga o'tkazadi."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        extra_fields = ("request_id", "method", "path", "status_code", "duration_ms", "client_ip")
        for field in extra_fields:
            if hasattr(record, field):
                log_data[field] = getattr(record, field)
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging() -> logging.Logger:
    """Ilova uchun konsol va faylga (RotatingFileHandler) JSON log yozishni sozlaydi."""
    LOG_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger("football_system")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = JsonFormatter()

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(
            LOG_FILE,
            maxBytes=2 * 1024 * 1024,
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger