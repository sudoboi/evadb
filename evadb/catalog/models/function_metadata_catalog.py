# coding=utf-8
# Copyright 2018-2023 EvaDB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from evadb.catalog.models.base_model import BaseModel
from evadb.catalog.models.utils import FunctionMetadataCatalogEntry


class FunctionMetadataCatalog(BaseModel):
    """
    The `FunctionMetadataCatalog` catalog stores information about the metadata of user-defined functions (Functions).
    Metadata is implemented a key-value pair that can be used to store additional information about the Function.
    It maintains the following information for each attribute:
        `_row_id:` an autogenerated identifier
        `_key: ` key/identifier of the metadata (as a string)
        `_value:` value of the metadata (as a string)
        `_function_id:` the `_row_id` of the `FunctionCatalog` entry to which the attribute belongs
    """

    __tablename__ = "function_metadata_catalog"

    _key = Column("key", String(100))
    _value = Column("value", String(100))
    _function_id = Column(
        "function_id", Integer, ForeignKey("function_catalog._row_id")
    )

    __table_args__ = (UniqueConstraint("key", "function_id"), {})

    # Foreign key dependency with the function catalog
    _function = relationship("FunctionCatalog", back_populates="_metadata")

    def __init__(self, key: str, value: str, function_id: int):
        self._key = key
        self._value = value
        self._function_id = function_id

    def as_dataclass(self) -> "FunctionMetadataCatalogEntry":
        return FunctionMetadataCatalogEntry(
            row_id=self._row_id,
            key=self._key,
            value=self._value,
            function_id=self._function_id,
            function_name=self._function._name,
        )