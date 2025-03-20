from sqlalchemy.orm import attribute_keyed_dict, add_mapped_attribute, relationship

from .to_snake_case import to_snake_case


def bidirectional_relationship(
    table_class: "Base", foreign_table_class: "Base", dictionary_key: str = None, extension: str = "children"
) -> "Relationship":
    """Create a bidirectional relationship between two table-classes.

    Automatically adds dependent information to foreign key class.

    :param table_class: Table class with foreign key.
    :type table_class: "Base"
    :param foreign_table_class: Table class referred to via foreign key.
    :type foreign_table_class: "Base"
    :param dictionary_key: Dictionary key for foreign key. If not provided, a Set will be used.
    :type dictionary_key: str
    :param extension: Extension name in parent table.
    :type extension: str
    :returns: Relationship object.
    :rtype: Relationship
    """
    column_name = f"{to_snake_case(table_class.__name__)}_{extension}"
    kwargs = dict(back_populates=foreign_table_class.__tablename__, cascade="all, delete-orphan")
    kwargs["collection_class"] = attribute_keyed_dict(dictionary_key) if dictionary_key else set

    add_mapped_attribute(foreign_table_class, column_name, relationship(table_class, **kwargs))
    foreign_table_class.add_dependent__(column_name)

    return relationship(foreign_table_class.__name__, back_populates=column_name)
