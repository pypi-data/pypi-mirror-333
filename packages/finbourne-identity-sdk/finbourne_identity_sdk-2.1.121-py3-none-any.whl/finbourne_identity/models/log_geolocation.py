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


from typing import Any, Dict, Optional, Union
from pydantic.v1 import StrictStr, Field, BaseModel, StrictFloat, StrictInt 

class LogGeolocation(BaseModel):
    """
    Represents a LogGeolocation resource in the Okta API  # noqa: E501
    """
    latitude: Optional[Union[StrictFloat, StrictInt]] = None
    longitude: Optional[Union[StrictFloat, StrictInt]] = None
    __properties = ["latitude", "longitude"]

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
    def from_json(cls, json_str: str) -> LogGeolocation:
        """Create an instance of LogGeolocation from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if latitude (nullable) is None
        # and __fields_set__ contains the field
        if self.latitude is None and "latitude" in self.__fields_set__:
            _dict['latitude'] = None

        # set to None if longitude (nullable) is None
        # and __fields_set__ contains the field
        if self.longitude is None and "longitude" in self.__fields_set__:
            _dict['longitude'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LogGeolocation:
        """Create an instance of LogGeolocation from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LogGeolocation.parse_obj(obj)

        _obj = LogGeolocation.parse_obj({
            "latitude": obj.get("latitude"),
            "longitude": obj.get("longitude")
        })
        return _obj
