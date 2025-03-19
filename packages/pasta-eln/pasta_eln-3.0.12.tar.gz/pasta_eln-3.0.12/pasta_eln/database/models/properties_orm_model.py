""" Represents the ORM model for the properties table in the database. """
#  PASTA-ELN and all its sub-parts are covered by the MIT license.
#
#  Copyright (c) 2024
#
#  Author: Jithu Murugan
#  Filename: properties_orm_model.py
#
#  You should have received a copy of the license with this file. Please refer the license file for more information.

from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from pasta_eln.database.models.orm_model_base import OrmModelBase


class PropertiesOrmModel(OrmModelBase):
  """Represents the ORM model for the properties table in the database.

  This class defines the structure of the properties model used in the application,
  including fields for ID, key, value, and unit. It provides a method to retrieve the
  names of the table columns for database operations.
  """
  __tablename__ = 'properties'

  id: Mapped[str] = mapped_column(primary_key=True)
  key: Mapped[str] = mapped_column(primary_key=True)
  value: Mapped[Optional[str]]
  unit: Mapped[Optional[str]]

  @classmethod
  def get_table_columns(cls) -> list[str]:
    """Retrieves the list of column names for the properties table.

    This method returns a list of strings representing the names of the columns
    defined in the properties model. It is useful for database operations that
    require knowledge of the table structure.

    Returns:
        list[str]: A list of column names for the properties table.
    """
    return ['id', 'key', 'value', 'unit']
