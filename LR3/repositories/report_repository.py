from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from sqlalchemy import text


class ReportRepository:
    def __init__(self, session):
        self.session = session

    async def get_by_date(self, report_at: date) -> List[Dict[str, Any]]:
        result = await self.session.execute(
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
        return [dict(row) for row in result.mappings().all()]
