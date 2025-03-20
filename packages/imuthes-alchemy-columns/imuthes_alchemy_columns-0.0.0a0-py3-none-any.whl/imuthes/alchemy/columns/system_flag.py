from sqlalchemy.orm import Mapped, mapped_column


class SystemFlagColumn:
    """Column that indicated that record is used for internal purpose. Usually not displayed in lists

    ``system_flag_``

    Only one record per table can be flagged as default.

    This is enforced by setting the column as UNIQUE, but allow NULL.
    """

    system_flag_: Mapped[bool] = mapped_column(default=False, sort_order=9999)

    def _inner_str(self) -> str:
        return "IS_SYSTEM" if self.system_flag_ else ""
