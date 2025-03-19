# coding: utf-8

"""
    FINBOURNE Identity Service API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, Optional
from pydantic.v1 import StrictStr, Field, BaseModel, Field, StrictStr 

class LogActor(BaseModel):
    """
    Represents a LogActor resource in the Okta API  # noqa: E501
    """
    id:  Optional[StrictStr] = Field(None,alias="id") 
    type:  Optional[StrictStr] = Field(None,alias="type") 
    alternate_id:  Optional[StrictStr] = Field(None,alias="alternateId") 
    display_name:  Optional[StrictStr] = Field(None,alias="displayName") 
    detail_entry: Optional[Dict[str, Any]] = Field(None, alias="detailEntry")
    __properties = ["id", "type", "alternateId", "displayName", "detailEntry"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def __str__(self):
        """For `print` and `pprint`"""
        return pprint.pformat(self.dict(by_alias=False))

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> LogActor:
        """Create an instance of LogActor from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if id (nullable) is None
        # and __fields_set__ contains the field
        if self.id is None and "id" in self.__fields_set__:
            _dict['id'] = None

        # set to None if type (nullable) is None
        # and __fields_set__ contains the field
        if self.type is None and "type" in self.__fields_set__:
            _dict['type'] = None

        # set to None if alternate_id (nullable) is None
        # and __fields_set__ contains the field
        if self.alternate_id is None and "alternate_id" in self.__fields_set__:
            _dict['alternateId'] = None

        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if detail_entry (nullable) is None
        # and __fields_set__ contains the field
        if self.detail_entry is None and "detail_entry" in self.__fields_set__:
            _dict['detailEntry'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LogActor:
        """Create an instance of LogActor from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LogActor.parse_obj(obj)

        _obj = LogActor.parse_obj({
            "id": obj.get("id"),
            "type": obj.get("type"),
            "alternate_id": obj.get("alternateId"),
            "display_name": obj.get("displayName"),
            "detail_entry": obj.get("detailEntry")
        })
        return _obj
