import inspect
from typing import Iterable

from hakisto import Logger
import hakisto._severity

from imuthes import DisplayColumn
from .cli import CliCrudMixin
from .. import Deferrer

logger = Logger("imuthes.ansible.intpk.status")
logger.severity = hakisto.severity.ERROR

Logger.register_excluded_source_file(inspect.currentframe().f_code.co_filename)

from sqlalchemy import ForeignKey, event, or_
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship, Session

from imuthes.alchemy.columns import DefaultFlagColumn, SystemFlagColumn, UniqueUppercaseNamedColumn
from .base import Base
from ...alchemy import Deferrer
from ..types import UnsignedSmallInteger
from .exceptions import StatusChangeNotPermittedError


class Status(
    Base,
    UniqueUppercaseNamedColumn,
    SystemFlagColumn,
    DefaultFlagColumn,
    CliCrudMixin,
):
    """Central list of possible statuses. Can be used in any table by using MixIn cls:`StatusForeignKey`.

    .. list-table::
       :header-rows: 1

       * - Column
         - Type
         - Description

       * - ``id``
         - UnsignedSmallInteger
         - **Primary Key**

       * - ``name``
         - String(20)
         - **Unique** **Uppercase**

       * - ``default_flag_``
         - Boolean
         - Only one entry can be marked as **default**

       * - ``system_flag_``
         - Boolean
         - Entry not to be used for user interaction

    Initial Content:

    .. list-table::
       :header-rows: 1

       * - id
         - name
         - default_flag
         - system_flag

       * - 1
         - ACTIVE
         - *False*
         - *None*

       * - 2
         - NEW
         - *False*
         - *None*

       * - 3
         - BLOCKED
         - *True*
         - *True*

       * -
         - INACTIVE
         - *False*
         - *None*

    """

    ID_ACTIVE: int = 1
    ID_NEW: int = 2
    ID_BLOCKED: int = 3

    CLI_LIST_COLUMNS__ = [
        DisplayColumn("name", header="Status", is_key=True),
    ]

    id: Mapped[int] = mapped_column(
        UnsignedSmallInteger,
        primary_key=True,
        sort_order=-1000,
    )

    def __str__(self):
        return self.name


class StatusForeignKey:
    """Foreign Key Mixin for :py:class:`.Status`"""

    status_id: Mapped[int] = mapped_column(
        ForeignKey("status.id"),
        default=Status.ID_NEW,
        sort_order=9000,
    )

    def change_status__(self, new_status: str) -> None:
        if new_status not in self.STATUS__[self.status.name]:
            raise StatusChangeNotPermittedError(self, new_status=new_status)
        self.change_status___(new_status=new_status)

    def get_permitted_status_change__(self) -> tuple[str]:
        """Tuple of permitted statuses to be changed to"""
        return self.STATUS__[self.status.name]

    def change_status___(self, new_status: str) -> None:
        """Override this when change of status required additional actions

        :param new_status: new status
        """
        session = self.get_session__()
        self.status = Status.get__(session=session, requirement__="1", name=new_status)

    @property
    def is_selectable(self) -> bool:
        return self.status_id == Status.ID_ACTIVE

    # noinspection PyMethodParameters
    @declared_attr
    def status(cls) -> Mapped[Status]:
        return relationship("Status")

    @classmethod
    def status_filter__(cls, session, selector, statuses: Iterable[str]):
        """Filter records with requested statuses.

        :param session: SQLAlchemy session
        :param selector:
        :param statuses: List of statuses (name)
        """
        logger.debug(f"{statuses}")
        status_lookup = Statuses(session)
        _or = [cls.status == status_lookup[i] for i in statuses]
        if _or:
            logger.debug(f"{_or}")
            if len(_or) == 1:
                selector = selector.where(_or[0])
            else:
                selector = selector.where(or_(*_or))
        return selector


class Statuses:
    """Utility to cache :py:class:`.Status` and access as Attribute or Key

    :param session: SQLAlchemy session
    """

    def __init__(self, session):
        self._session = session
        self._data = {}

    def __getitem__(self, item: str) -> "Status":
        item = item.upper()
        if item not in self._data:
            name = item.replace("_", " ")
            self._data[item] = Status.get__(self._session, requirement__="1", name=name)
        return self._data[item]

    def __getattr__(self, item: str) -> "Status":
        try:
            return self[item]
        except KeyError:
            raise AttributeError(item) from None


# noinspection PyArgumentList
def initialize_content(session):
    return (
        session.add(
            Status(id=Status.ID_ACTIVE, name="ACTIVE")
        ),  # This must be fixed to allow property 'is_selectable' in tables
        session.add(Status(id=Status.ID_NEW, name="NEW")),  # This must be fixed to allow defaulting to 'NEW'
        session.add(
            Status(id=Status.ID_BLOCKED, name="BLOCKED", system_flag_=True, default_flag_=True)
        ),  # Used for technical purposes only.
        session.add(Status(name="INACTIVE")),
    )


# noinspection PyUnusedLocal
@event.listens_for(Status.__table__, "after_create")
def defer(target, connection, **kwargs):
    deferrer = Deferrer()
    deferrer.append(initialize_content)
