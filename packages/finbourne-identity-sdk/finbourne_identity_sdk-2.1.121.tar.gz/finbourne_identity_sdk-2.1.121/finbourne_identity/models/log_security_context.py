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
from pydantic.v1 import StrictStr, Field, BaseModel, Field, StrictBool, StrictInt, StrictStr 

class LogSecurityContext(BaseModel):
    """
    Represents a LogSecurityContext resource in the Okta API  # noqa: E501
    """
    as_number: Optional[StrictInt] = Field(None, alias="asNumber")
    as_org:  Optional[StrictStr] = Field(None,alias="asOrg") 
    isp:  Optional[StrictStr] = Field(None,alias="isp") 
    domain:  Optional[StrictStr] = Field(None,alias="domain") 
    is_proxy: Optional[StrictBool] = Field(None, alias="isProxy")
    __properties = ["asNumber", "asOrg", "isp", "domain", "isProxy"]

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
    def from_json(cls, json_str: str) -> LogSecurityContext:
        """Create an instance of LogSecurityContext from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if as_number (nullable) is None
        # and __fields_set__ contains the field
        if self.as_number is None and "as_number" in self.__fields_set__:
            _dict['asNumber'] = None

        # set to None if as_org (nullable) is None
        # and __fields_set__ contains the field
        if self.as_org is None and "as_org" in self.__fields_set__:
            _dict['asOrg'] = None

        # set to None if isp (nullable) is None
        # and __fields_set__ contains the field
        if self.isp is None and "isp" in self.__fields_set__:
            _dict['isp'] = None

        # set to None if domain (nullable) is None
        # and __fields_set__ contains the field
        if self.domain is None and "domain" in self.__fields_set__:
            _dict['domain'] = None

        # set to None if is_proxy (nullable) is None
        # and __fields_set__ contains the field
        if self.is_proxy is None and "is_proxy" in self.__fields_set__:
            _dict['isProxy'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> LogSecurityContext:
        """Create an instance of LogSecurityContext from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return LogSecurityContext.parse_obj(obj)

        _obj = LogSecurityContext.parse_obj({
            "as_number": obj.get("asNumber"),
            "as_org": obj.get("asOrg"),
            "isp": obj.get("isp"),
            "domain": obj.get("domain"),
            "is_proxy": obj.get("isProxy")
        })
        return _obj
