from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

import datetime
from ..models.add_attachment_response_author import AddAttachmentResponseAuthor


class AddAttachmentResponse(BaseModel):
    """
    Attributes:
        author (Optional[AddAttachmentResponseAuthor]):
        content (Optional[str]): The content of the attachment.
        created (Optional[datetime.datetime]): The datetime the attachment was created.
        filename (Optional[str]): The file name of the attachment.
        id (Optional[str]): The ID of the attachment
        mime_type (Optional[str]): The MIME type of the attachment.
        self_ (Optional[str]): The URL of the attachment details response.
        size (Optional[int]): The size of the attachment.
        thumbnail (Optional[str]): The URL of a thumbnail representing the attachment.
    """

    model_config = ConfigDict(extra="allow")

    author: Optional["AddAttachmentResponseAuthor"] = None
    content: Optional[str] = None
    created: Optional[datetime.datetime] = None
    filename: Optional[str] = None
    id: Optional[str] = None
    mime_type: Optional[str] = None
    self_: Optional[str] = None
    size: Optional[int] = None
    thumbnail: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["AddAttachmentResponse"], src_dict: Dict[str, Any]):
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
