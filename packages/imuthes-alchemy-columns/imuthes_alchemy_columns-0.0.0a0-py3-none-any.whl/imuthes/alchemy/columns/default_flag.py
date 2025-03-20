import inspect
from typing import Optional

import hakisto._severity
from hakisto import Logger

logger = Logger("imuthes.alchemy.columns")
logger.severity = hakisto.severity.ERROR
Logger.register_excluded_source_file(inspect.currentframe().f_code.co_filename)


from sqlalchemy import select

from sqlalchemy.orm import Mapped, mapped_column

from imuthes.alchemy.exceptions import DefaultRecordNotFoundError


class DefaultFlagColumn:
    """Column that indicated that a specific record should be used as default.

    ``default_flag_``

    Only one record per table can be flagged as default.

    This is enforced by setting the column as UNIQUE, but allow NULL.
    """

    default_flag_: Mapped[Optional[bool]] = mapped_column(unique=True, sort_order=9998)

    @classmethod
    def get_default__(cls, session):
        logger.debug(f"{cls.__name__}.get_default__()")
        record = session.scalar(select(cls).where(cls.default_flag_ == True))
        if record is None:
            raise DefaultRecordNotFoundError(cls)
        return record

    def _inner_str(self) -> str:
        return "IS_DEFAULT" if self.default_flag_ else ""
