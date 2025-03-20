from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

import datetime


class GetInstanceInfoResponse(BaseModel):
    """
    Attributes:
        base_url (Optional[str]): The base URL of the Jira instance
        site_url (Optional[str]): The site URL of the Jira instance
        build_date (Optional[datetime.datetime]): The timestamp when the Jira version was built.
        build_number (Optional[int]): The build number of the Jira version.
        deployment_type (Optional[str]): The type of server deployment. This is always returned as *Cloud*.
        scm_info (Optional[str]): The unique identifier of the Jira version.
        server_time (Optional[datetime.datetime]): The time in Jira when this request was responded to.
        server_title (Optional[str]): The name of the Jira instance.
        version (Optional[str]): The version of Jira.
        version_numbers (Optional[list[int]]):
    """

    model_config = ConfigDict(extra="allow")

    base_url: Optional[str] = None
    site_url: Optional[str] = None
    build_date: Optional[datetime.datetime] = None
    build_number: Optional[int] = None
    deployment_type: Optional[str] = None
    scm_info: Optional[str] = None
    server_time: Optional[datetime.datetime] = None
    server_title: Optional[str] = None
    version: Optional[str] = None
    version_numbers: Optional[list[int]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetInstanceInfoResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
