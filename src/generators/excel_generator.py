from typing import List
from io import BytesIO
from openpyxl import Workbook

from models.subscriber import Subscriber


class ExcelGenerator:
    """Generates Excel file with subscribers."""

    def generate(self, subscribers: List[Subscriber]):
        wb = Workbook()
        ws = wb.active
        ws.title = "Subscribers"

        ws.append([
            "User ID",
            "Name",
            "First Message Date"
        ])

        for s in subscribers:
            ws.append([
                s.user_id,
                s.username,
                s.first_message_date.isoformat() if s.first_message_date else "",
            ])

        buffer = BytesIO()
        wb.save(buffer)

        return buffer.getvalue(), "subscribers.xlsx"