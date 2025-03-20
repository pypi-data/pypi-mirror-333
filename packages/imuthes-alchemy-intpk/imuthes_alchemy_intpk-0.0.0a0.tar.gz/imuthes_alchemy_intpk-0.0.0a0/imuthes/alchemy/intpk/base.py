# ------------------------------------------------------------------------------
#  Imuthes by NetLink Consulting GmbH
#
#  Copyright (c) 2025. Bernhard W. Radermacher
#
#  This program is free software: you can redistribute it and/or modify it under
#  the terms of the GNU Lesser General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option) any
#  later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
#  details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ------------------------------------------------------------------------------

import re
import sys
from typing import Iterable, Callable, Any

import hakisto._severity
from sqlalchemy import UniqueConstraint, select, inspect
from sqlalchemy.orm import MappedAsDataclass, DeclarativeBase, Mapped, mapped_column, declared_attr, Session
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.sql.elements import KeyedColumnElement

from imuthes.alchemy.types import UnsignedBigInteger
from sqlalchemy_history import make_versioned
from imuthes import class_property
from imuthes.alchemy.exceptions import ClassNotFoundError, DependentsFoundError, MultipleRecordsFoundError

from .to_snake_case import to_snake_case

from hakisto import logger

# logger.register_excluded_source_file(inspect.currentframe().f_code.co_filename)

make_versioned(user_cls=None)


class Base(DeclarativeBase):
    """Base for all tables.

    Table names in the database are derived automatically.
    """

    __cache = dict(class_lookup={})

    id: Mapped[int] = mapped_column(UnsignedBigInteger, primary_key=True, sort_order=-sys.maxsize)

    # noinspection PyMethodParameters
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """Default table name in Database is derived from Class Name"""
        return to_snake_case(cls.__name__)

    @classmethod
    def get_unique_constraint__(cls, name: str = "composite_pk") -> UniqueConstraint | None:
        mapper = inspect(cls)
        for i in mapper.mapped_table.constraints:
            logger.trace(f"{i}")
            if not isinstance(i, UniqueConstraint):
                continue
            if i.name == name:
                logger.debug(f"Unique constraint {i.name} found")
                return i

        # if not hasattr(cls, '__unique_constraints__'):
        #     cls.__unique_constraints__ = {}
        #     # noinspection PyUnresolvedReferences
        #     for i in cls.__table__.constraints:
        #         if isinstance(i, UniqueConstraint):
        #             name = '_'.join((j.name for j in i.columns)) if i.name is None else i.name
        #             cls.__unique_constraints__[name] = i
        #             logger.debug(f'{name}: {i}')
        # if len(cls.__unique_constraints__) == 1:
        #     return list(cls.__unique_constraints__.values())[0]
        # return cls.__unique_constraints__[name]

    @classmethod
    def get_identifier__(cls):
        return cls.get_unique_constraint__().columns

    # noinspection PyMethodParameters
    @class_property
    def display_name__(cls):
        if not hasattr(cls, "__display_name__"):
            # noinspection PyAttributeOutsideInit
            cls.__display_name__ = to_snake_case(cls.__name__).replace("_", " ").title()
        return cls.__display_name__

    @classmethod
    def add_dependent__(cls, dependent: str):
        """The dependent is the name of the _kids attribute that is
        mapped in the parent relationship"""
        if not hasattr(cls, "__dependents"):
            cls.__dependents = set()
        cls.__dependents.add(dependent)

    def check_dependents__(self):
        """Check if dependents exist that would either be orphaned or deleted"""
        dependents = self.get_dependents__()
        if dependents:
            raise DependentsFoundError(table_class=self.__class__, dependents=dependents)

    def get_dependents__(self):
        """Return all dependents"""
        result = []
        if hasattr(self, "__dependents"):
            for i in self.__dependents:
                result.extend(getattr(self, i))
        return result

    @classmethod
    def get_class__(cls, item: str) -> "Base":
        """Lookup to get the respective Class from class name or table name"""
        if not cls.__cache["class_lookup"]:
            # noinspection PyUnresolvedReferences
            cls.__cache["class_lookup"] = {i.persist_selectable.name: i.class_ for i in cls.registry.mappers}
            cls.__cache["class_lookup"].update({i.class_.__name__: i.class_ for i in cls.registry.mappers})
        if item not in cls.__cache["class_lookup"]:
            raise ClassNotFoundError(item)
        return cls.__cache["class_lookup"][item]

    @classmethod
    def get_columns__(cls) -> Callable[[], ReadOnlyColumnCollection[str, KeyedColumnElement[Any]]]:
        """Get Columns"""
        return cls.__table__.c

    @classmethod
    def initialize__(cls, session: Session):
        pass

    # noinspection PyUnresolvedReferences
    @classmethod
    def get__(
        cls,
        session: Session,
        requirement__: str = "+",
        search__: str | re.Pattern = None,
        statuses__: Iterable[str] = None,
        **kwargs,
    ):
        """Return record or tuple using **kwargs

        requirement__:
          - '0': one optional record - error when more
          - '1': one record must be returned - error when more or not found
          - 'S': one record must be returned - must be selectable,  error when more or not found
          - 's': return only selectable records (tuple of records)
          - '+': (default) return matching records (tuple of records)

        search__:
          - if ``str`` - match normal
          - if ``re.Pattern`` - match using regular expression
        """
        logger.debug(f"table_class: {cls.__name__}")
        logger.debug(f"requirement__: '{requirement__}'")
        logger.debug(f"statuses__: '{statuses__}'")
        logger.debug(f"kwargs: {kwargs}")

        if requirement__ not in "01Ss+":
            raise ValueError(requirement__)

        selector = select(cls)

        if hasattr(cls, "search__") and search__ is not None:
            logger.debug(f"search__: '{search__}'")
            selector = cls.search__(selector=selector, value=search__)

        if hasattr(cls, "status") and statuses__:
            logger.debug(f"statuses__: {statuses__}")
            # noinspection PyUnresolvedReferences
            selector = cls.status_filter__(session, selector, statuses__)

        for i in (i for i in kwargs if not i.endswith("_kids")):
            if hasattr(cls, i):
                temp = kwargs[i]
                # looks like a column, but might be a reference
                if not i.endswith("_id") and hasattr(cls, f"{i}_id") and isinstance(kwargs[i], str):
                    # ok so this is a reference that has to be resolved
                    temp_kwargs = kwargs.copy()
                    temp_kwargs["name"] = kwargs[i]
                    temp = Base.get_class__(i).get__(session=session, requirement__="1", **temp_kwargs)

                # noinspection PyTypeChecker
                selector = selector.where(getattr(cls, i) == temp)

        if requirement__ in "sS" and hasattr(cls, "is_selectable__"):
            selector = selector.where(cls.is_selectable__)
        # noinspection PyTypeChecker
        logger.debug(selector.compile(compile_kwargs={"literal_binds": True}))
        # noinspection PyTypeChecker
        response: tuple["Base"] = tuple(session.scalars(selector))
        logger.debug(f"got {len(response)} records")

        if requirement__ in "01S":
            # max one record
            if len(response) > 1:
                raise MultipleRecordsFoundError(cls, len(response))
            if len(response) == 1:
                return response[0]
            else:
                return None
        return response

    def get_session__(self):
        try:
            return self._sa_instance_state.session
        except:
            return None

    # @classmethod
    # def cli_exit_add_pre(cls, **kwargs):
    #     pass
    #
    # @classmethod
    # def cli_exit_add_post(cls, **kwargs):
    #     pass
    #
    # @classmethod
    # def cli_exit_change_pre(cls, **kwargs):
    #     pass
    #
    # @classmethod
    # def cli_exit_change_post(cls, **kwargs):
    #     pass
    #
    # @classmethod
    # def cli_exit_change_pre(cls, **kwargs):
    #     pass
    #
    # @classmethod
    # def cli_exit_change_post(cls, **kwargs):
    #     pass
