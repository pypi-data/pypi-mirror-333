from sqlalchemy import or_

from imuthes import inherit_private_iterable, class_property
import hakisto._severity
from hakisto import Logger

logger = Logger("imuthes.ansible.intpk.SearchableMixin")
logger.severity = hakisto.severity.ERROR


class Searchable:
    __searchable_columns__ = None

    @class_property
    def searchable_columns__(cls):
        if cls.__searchable_columns__ is None:
            cls.__searchable_columns__ = tuple(inherit_private_iterable(cls, "__searchable_columns__", unique=True))
        return cls.__searchable_columns__

    @classmethod
    def _make_comparator__(cls, value):
        if isinstance(value, str):
            kwargs = {}
            if "%" in value:
                kwargs["escape"] = "/"
                value = value.replace("%", "/%")

            def comparator(column):
                return column.ilike(f"%{value}%", **kwargs)

        else:

            def comparator(column):
                return column.regexp_match(value.pattern)

        return comparator

    @classmethod
    def search__(cls, selector, value):
        logger.debug(f"{cls.__name__}.search__: searchable_columns: {cls.searchable_columns__}")
        if cls.searchable_columns__:
            comparator = cls._make_comparator__(value)
            selector = selector.where(or_(*[comparator(getattr(cls, i)) for i in cls.searchable_columns__]))
        return selector
