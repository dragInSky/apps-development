from __future__ import annotations

from datetime import date
from typing import Any, Dict, List

from LR3.repositories.report_repository import ReportRepository


class ReportService:
    def __init__(self, report_repository: ReportRepository):
        self.report_repository = report_repository

    async def get_by_date(self, report_at: date) -> List[Dict[str, Any]]:
        return await self.report_repository.get_by_date(report_at)
