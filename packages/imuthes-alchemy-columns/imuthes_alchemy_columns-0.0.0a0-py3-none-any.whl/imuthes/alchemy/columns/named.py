"""Mixins to provide Unique Key"""

from sqlalchemy import String, UniqueConstraint
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from imuthes.alchemy.exceptions import NameLengthExceededError


class NamedColumn:
    """Name - default length 20 characters, searchable.

    ``name``

    Implemented as property to allow length check.
    """

    __searchable_columns__ = ("name",)
    _name_length__ = 20
    # RELATIONSHIP_KEY__ = 'name'

    # noinspection PyMethodParameters
    @declared_attr
    def _name(cls) -> Mapped[str]:
        return mapped_column("name", String(cls._name_length__), sort_order=-500)  # pragma: no cover

    @hybrid_property
    def name(self) -> str:
        return self._name

    @name.inplace.setter
    def name(self, name: str):
        self._check_name_value(name=name)
        # noinspection PyAttributeOutsideInit
        self._name = self._adapt(name)

    def _check_name_value(self, name: str) -> None:
        if len(name) > self._name_length__:
            raise NameLengthExceededError(self.__class__, name)

    @staticmethod
    def _adapt(name: str) -> str:
        return name

    def _inner_str(self) -> str:
        return f"name='{self.name}'"


class UppercaseNamedColumn(NamedColumn):
    """Name - default length 20 characters, searchable.

    ``name``

    Forces value to be uppercase.
    """

    @staticmethod
    def _adapt(name: str) -> str:
        return name.upper()

    # noinspection PyMethodParameters
    @declared_attr
    def _name(cls) -> Mapped[str]:
        return mapped_column(
            "name",
            String(cls._name_length__)
            .with_variant(String(collation="nocase"), "sqlite")
            .with_variant(String(collation="utf8mb4_general_ci"), "mysql", "mariadb")
            .with_variant(String(collation="SQL_Latin1_General_CP1_CI_AS"), "mssql"),
            sort_order=-500,
        )


class UniqueNamedColumn(NamedColumn):
    """Name - default length 20 characters, searchable.

    ``name``

    Forces value to be uppercase and sets ``name`` to be unique (to be used as an alternative primary key).
    """

    __table_args__ = (UniqueConstraint("name", name="composite_pk"),)


class UniqueUppercaseNamedColumn(UppercaseNamedColumn, UniqueNamedColumn):
    """Name - default length 20 characters, searchable.

    ``name``

    Sets ``name`` to be unique (to be used as an alternative primary key).
    """

    pass
