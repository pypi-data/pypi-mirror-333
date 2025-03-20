from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_fields_reporter_avatar_urls import (
    GetIssueResponseFieldsReporterAvatarUrls,
)


class GetIssueResponseFieldsReporter(BaseModel):
    """
    Attributes:
        account_id (Optional[str]):
        account_type (Optional[str]):
        active (Optional[bool]):
        avatar_urls (Optional[GetIssueResponseFieldsReporterAvatarUrls]):
        display_name (Optional[str]):
        email_address (Optional[str]):
        id (Optional[str]):
        self_ (Optional[str]):
        time_zone (Optional[str]):
    """

    model_config = ConfigDict(extra="allow")

    account_id: Optional[str] = None
    account_type: Optional[str] = None
    active: Optional[bool] = None
    avatar_urls: Optional["GetIssueResponseFieldsReporterAvatarUrls"] = None
    display_name: Optional[str] = None
    email_address: Optional[str] = None
    id: Optional[str] = None
    self_: Optional[str] = None
    time_zone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseFieldsReporter"], src_dict: Dict[str, Any]
    ):
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
