from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

import datetime
from ..models.get_issue_response_fields_attachment_author import (
    GetIssueResponseFieldsAttachmentAuthor,
)


class GetIssueResponseFieldsAttachmentArrayItemRef(BaseModel):
    """
    Attributes:
        thumbnail (Optional[str]): The thumbnail of attachment
        filename (Optional[str]): The file name of attachment
        size (Optional[int]): The size of attachment
        author (Optional[GetIssueResponseFieldsAttachmentAuthor]):
        created (Optional[datetime.datetime]): The created of attachment
        self_ (Optional[str]): The self of attachment
        id (Optional[str]): The ID of attachment
        mime_type (Optional[str]): The mime type of attachment
        content (Optional[str]): The content of attachment
    """

    model_config = ConfigDict(extra="allow")

    thumbnail: Optional[str] = None
    filename: Optional[str] = None
    size: Optional[int] = None
    author: Optional["GetIssueResponseFieldsAttachmentAuthor"] = None
    created: Optional[datetime.datetime] = None
    self_: Optional[str] = None
    id: Optional[str] = None
    mime_type: Optional[str] = None
    content: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseFieldsAttachmentArrayItemRef"],
        src_dict: Dict[str, Any],
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
