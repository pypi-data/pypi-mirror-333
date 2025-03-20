from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_fields_attachment_author_avatar_urls import (
    GetIssueResponseFieldsAttachmentAuthorAvatarUrls,
)


class GetIssueResponseFieldsAttachmentAuthor(BaseModel):
    """
    Attributes:
        account_id (Optional[str]): The author account ID of attachment
        email_address (Optional[str]): The author email address of attachment
        display_name (Optional[str]): The author display name of attachment
        account_type (Optional[str]): The author account type of attachment
        self_ (Optional[str]): The author self of attachment
        active (Optional[bool]): Is attachment author active
        time_zone (Optional[str]): The timezone of author
        avatar_urls (Optional[GetIssueResponseFieldsAttachmentAuthorAvatarUrls]):
    """

    model_config = ConfigDict(extra="allow")

    account_id: Optional[str] = None
    email_address: Optional[str] = None
    display_name: Optional[str] = None
    account_type: Optional[str] = None
    self_: Optional[str] = None
    active: Optional[bool] = None
    time_zone: Optional[str] = None
    avatar_urls: Optional["GetIssueResponseFieldsAttachmentAuthorAvatarUrls"] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseFieldsAttachmentAuthor"], src_dict: Dict[str, Any]
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
