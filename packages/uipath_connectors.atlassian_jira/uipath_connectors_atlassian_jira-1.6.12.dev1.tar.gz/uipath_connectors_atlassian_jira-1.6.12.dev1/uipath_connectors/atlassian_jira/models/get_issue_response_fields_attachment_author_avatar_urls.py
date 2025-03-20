from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsAttachmentAuthorAvatarUrls")


@_attrs_define
class GetIssueResponseFieldsAttachmentAuthorAvatarUrls:
    """
    Attributes:
        field_48x48 (Union[Unset, str]): The author avatar urls 48 x 48 of attachment
        field_32x32 (Union[Unset, str]): The author avatar urls 32 x 32 of attachment
        field_24x24 (Union[Unset, str]): The author avatar urls 24 x 24 of attachment
        field_16x16 (Union[Unset, str]): The author avatar urls 16 x 16 of attachment
    """

    field_48x48: Union[Unset, str] = UNSET
    field_32x32: Union[Unset, str] = UNSET
    field_24x24: Union[Unset, str] = UNSET
    field_16x16: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field_48x48 = self.field_48x48

        field_32x32 = self.field_32x32

        field_24x24 = self.field_24x24

        field_16x16 = self.field_16x16

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field_48x48 is not UNSET:
            field_dict["48x48"] = field_48x48
        if field_32x32 is not UNSET:
            field_dict["32x32"] = field_32x32
        if field_24x24 is not UNSET:
            field_dict["24x24"] = field_24x24
        if field_16x16 is not UNSET:
            field_dict["16x16"] = field_16x16

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        field_48x48 = d.pop("48x48", UNSET)

        field_32x32 = d.pop("32x32", UNSET)

        field_24x24 = d.pop("24x24", UNSET)

        field_16x16 = d.pop("16x16", UNSET)

        get_issue_response_fields_attachment_author_avatar_urls = cls(
            field_48x48=field_48x48,
            field_32x32=field_32x32,
            field_24x24=field_24x24,
            field_16x16=field_16x16,
        )

        get_issue_response_fields_attachment_author_avatar_urls.additional_properties = d
        return get_issue_response_fields_attachment_author_avatar_urls

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
