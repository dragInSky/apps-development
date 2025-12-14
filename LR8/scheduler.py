from __future__ import annotations

import json
import logging
import os
from datetime import date

from sqlalchemy import text
from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_aio_pika import AioPikaBroker

from LR3.app.dependencies import async_session_factory, configure_engine, init_db

logger = logging.getLogger("lr8.scheduler")
_level_name = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, _level_name, logging.INFO))

broker = AioPikaBroker(
    os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/local"),
    exchange_name="report",
    queue_name="cmd_order",
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)

_db_ready = False


async def _ensure_db_ready() -> None:
    global _db_ready
    if _db_ready:
        return
    db_url = os.getenv("DATABASE_URL")
    if db_url:
        configure_engine(db_url)
    await init_db()
    _db_ready = True


@broker.task(
    schedule=[
        {
            "cron": "*/1 * * * *",
            "args": ["Cron_User"],
            "schedule_id": "order_report_every_minute",
        }
    ]
)
async def my_scheduled_task(name: str) -> str:
    await _ensure_db_ready()

    report_at = date.today()
    async with async_session_factory() as session:
        result = await session.execute(
            text(
                """
                SELECT report_at, order_id, count_product
                FROM order_report
                WHERE report_at = :report_at
                ORDER BY order_id
                """
            ),
            {"report_at": report_at},
        )
        rows = [dict(row) for row in result.mappings().all()]

    payload = {"name": name, "report_at": report_at.isoformat(), "rows": rows}
    logger.info("order_report generated report_at=%s rows=%s", report_at, len(rows))
    return json.dumps(payload, ensure_ascii=False, default=str)

