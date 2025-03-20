
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class DescriptionColumn:
    """Description - default length 120 characters, searchable.

    ``description``
    """

    __searchable_columns__ = ("description",)
    _description_length__ = 120
    _description_show__ = True

    description: Mapped[str] = mapped_column(
        String(_description_length__), default="", sort_order=1000, doc="dDescription of item"
    )

    def _inner_str(self) -> str:
        return f"description='{self.description}'" if self._description_show__ else ""

    def validate(self, value: str) -> None:
        if len(value) > self._description_length__:
            raise ValueError(f"Description exceeds maximum length {self._description_length__}")
        if not len(value.strip()):
            raise ValueError("Description must not be empty")
