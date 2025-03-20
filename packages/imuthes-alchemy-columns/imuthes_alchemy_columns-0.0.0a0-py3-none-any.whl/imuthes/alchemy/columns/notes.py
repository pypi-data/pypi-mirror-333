from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column


class NotesColumn:
    """Notes - character blob, searchable.

    ``notes``
    """

    __searchable_columns__ = ("notes",)
    _notes_show__ = False

    notes: Mapped[str] = mapped_column(Text, default="", sort_order=1001, doc="nDetailed information")

    def _inner_str(self) -> str:
        return f"notes='{self.notes}'" if self._notes_show__ else ""

    def validate(self, value: str) -> None:
        pass
