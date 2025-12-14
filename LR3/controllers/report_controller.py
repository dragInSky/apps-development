from typing import List

from litestar import Controller, post

from LR3.app.schemas import ReportRequest, ReportRow
from LR3.services.report_service import ReportService


class ReportController(Controller):
    path = "/report"

    @post()
    async def get_report(
        self, report_service: ReportService, data: ReportRequest
    ) -> List[ReportRow]:
        rows = await report_service.get_by_date(data.report_at)
        return [ReportRow.model_validate(row) for row in rows]
