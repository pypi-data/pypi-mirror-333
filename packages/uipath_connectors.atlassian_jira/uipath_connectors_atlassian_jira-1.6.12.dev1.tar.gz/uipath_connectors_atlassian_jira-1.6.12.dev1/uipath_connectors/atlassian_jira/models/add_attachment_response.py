from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.add_attachment_response_author import AddAttachmentResponseAuthor


T = TypeVar("T", bound="AddAttachmentResponse")


@_attrs_define
class AddAttachmentResponse:
    """
    Attributes:
        author (Union[Unset, AddAttachmentResponseAuthor]):
        content (Union[Unset, str]): The content of the attachment.
        created (Union[Unset, datetime.datetime]): The datetime the attachment was created.
        filename (Union[Unset, str]): The file name of the attachment.
        id (Union[Unset, str]): The ID of the attachment
        mime_type (Union[Unset, str]): The MIME type of the attachment.
        self_ (Union[Unset, str]): The URL of the attachment details response.
        size (Union[Unset, int]): The size of the attachment.
        thumbnail (Union[Unset, str]): The URL of a thumbnail representing the attachment.
    """

    author: Union[Unset, "AddAttachmentResponseAuthor"] = UNSET
    content: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    filename: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    mime_type: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    thumbnail: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        content = self.content

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        filename = self.filename

        id = self.id

        mime_type = self.mime_type

        self_ = self.self_

        size = self.size

        thumbnail = self.thumbnail

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if author is not UNSET:
            field_dict["author"] = author
        if content is not UNSET:
            field_dict["content"] = content
        if created is not UNSET:
            field_dict["created"] = created
        if filename is not UNSET:
            field_dict["filename"] = filename
        if id is not UNSET:
            field_dict["id"] = id
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if self_ is not UNSET:
            field_dict["self"] = self_
        if size is not UNSET:
            field_dict["size"] = size
        if thumbnail is not UNSET:
            field_dict["thumbnail"] = thumbnail

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.add_attachment_response_author import AddAttachmentResponseAuthor

        d = src_dict.copy()
        _author = d.pop("author", UNSET)
        author: Union[Unset, AddAttachmentResponseAuthor]
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = AddAttachmentResponseAuthor.from_dict(_author)

        content = d.pop("content", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        filename = d.pop("filename", UNSET)

        id = d.pop("id", UNSET)

        mime_type = d.pop("mimeType", UNSET)

        self_ = d.pop("self", UNSET)

        size = d.pop("size", UNSET)

        thumbnail = d.pop("thumbnail", UNSET)

        add_attachment_response = cls(
            author=author,
            content=content,
            created=created,
            filename=filename,
            id=id,
            mime_type=mime_type,
            self_=self_,
            size=size,
            thumbnail=thumbnail,
        )

        add_attachment_response.additional_properties = d
        return add_attachment_response

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
