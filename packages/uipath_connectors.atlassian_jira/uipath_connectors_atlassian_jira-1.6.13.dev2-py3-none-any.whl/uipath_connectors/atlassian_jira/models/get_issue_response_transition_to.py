from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_transition_to_status_category import (
    GetIssueResponseTransitionToStatusCategory,
)


class GetIssueResponseTransitionTo(BaseModel):
    """
    Attributes:
        description (Optional[str]): The description of the status
        icon_url (Optional[str]): The URL of the icon used to represent the status
        id (Optional[str]): The ID of the status
        name (Optional[str]): The name of the status
        self_ (Optional[str]): The URL of the status
        status_category (Optional[GetIssueResponseTransitionToStatusCategory]):
    """

    model_config = ConfigDict(extra="allow")

    description: Optional[str] = None
    icon_url: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    self_: Optional[str] = None
    status_category: Optional["GetIssueResponseTransitionToStatusCategory"] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetIssueResponseTransitionTo"], src_dict: Dict[str, Any]):
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
