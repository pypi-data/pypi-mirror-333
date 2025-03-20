from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_attachment_author import (
        GetIssueResponseFieldsAttachmentAuthor,
    )


T = TypeVar("T", bound="GetIssueResponseFieldsAttachmentArrayItemRef")


@_attrs_define
class GetIssueResponseFieldsAttachmentArrayItemRef:
    """
    Attributes:
        thumbnail (Union[Unset, str]): The thumbnail of attachment
        filename (Union[Unset, str]): The file name of attachment
        size (Union[Unset, int]): The size of attachment
        author (Union[Unset, GetIssueResponseFieldsAttachmentAuthor]):
        created (Union[Unset, datetime.datetime]): The created of attachment
        self_ (Union[Unset, str]): The self of attachment
        id (Union[Unset, str]): The ID of attachment
        mime_type (Union[Unset, str]): The mime type of attachment
        content (Union[Unset, str]): The content of attachment
    """

    thumbnail: Union[Unset, str] = UNSET
    filename: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    author: Union[Unset, "GetIssueResponseFieldsAttachmentAuthor"] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    self_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        thumbnail = self.thumbnail

        filename = self.filename

        size = self.size

        author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        self_ = self.self_

        id = self.id

        mime_type = self.mime_type

        content = self.content

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail
        if filename is not UNSET:
            field_dict["filename"] = filename
        if size is not UNSET:
            field_dict["size"] = size
        if author is not UNSET:
            field_dict["author"] = author
        if created is not UNSET:
            field_dict["created"] = created
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if content is not UNSET:
            field_dict["content"] = content

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_attachment_author import (
            GetIssueResponseFieldsAttachmentAuthor,
        )

        d = src_dict.copy()
        thumbnail = d.pop("thumbnail", UNSET)

        filename = d.pop("filename", UNSET)

        size = d.pop("size", UNSET)

        _author = d.pop("author", UNSET)
        author: Union[Unset, GetIssueResponseFieldsAttachmentAuthor]
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = GetIssueResponseFieldsAttachmentAuthor.from_dict(_author)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        mime_type = d.pop("mimeType", UNSET)

        content = d.pop("content", UNSET)

        get_issue_response_fields_attachment_array_item_ref = cls(
            thumbnail=thumbnail,
            filename=filename,
            size=size,
            author=author,
            created=created,
            self_=self_,
            id=id,
            mime_type=mime_type,
            content=content,
        )

        get_issue_response_fields_attachment_array_item_ref.additional_properties = d
        return get_issue_response_fields_attachment_array_item_ref

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
