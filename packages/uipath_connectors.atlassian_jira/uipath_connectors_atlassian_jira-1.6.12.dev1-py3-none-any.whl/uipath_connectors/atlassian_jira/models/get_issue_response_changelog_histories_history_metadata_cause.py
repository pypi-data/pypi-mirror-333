from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseChangelogHistoriesHistoryMetadataCause")


@_attrs_define
class GetIssueResponseChangelogHistoriesHistoryMetadataCause:
    """
    Attributes:
        avatar_url (Union[Unset, str]): The URL to an avatar for the user or system associated with a history record
        display_name (Union[Unset, str]): The display name of the user or system associated with a history record
        display_name_key (Union[Unset, str]): The key of the display name of the user or system associated with a
            history record
        id (Union[Unset, str]): The ID of the user or system associated with a history record
        type_ (Union[Unset, str]): The type of the user or system associated with a history record
        url (Union[Unset, str]): The URL of the user or system associated with a history record.
    """

    avatar_url: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    display_name_key: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_url = self.avatar_url

        display_name = self.display_name

        display_name_key = self.display_name_key

        id = self.id

        type_ = self.type_

        url = self.url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_url is not UNSET:
            field_dict["avatarUrl"] = avatar_url
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if display_name_key is not UNSET:
            field_dict["displayNameKey"] = display_name_key
        if id is not UNSET:
            field_dict["id"] = id
        if type_ is not UNSET:
            field_dict["type"] = type_
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_url = d.pop("avatarUrl", UNSET)

        display_name = d.pop("displayName", UNSET)

        display_name_key = d.pop("displayNameKey", UNSET)

        id = d.pop("id", UNSET)

        type_ = d.pop("type", UNSET)

        url = d.pop("url", UNSET)

        get_issue_response_changelog_histories_history_metadata_cause = cls(
            avatar_url=avatar_url,
            display_name=display_name,
            display_name_key=display_name_key,
            id=id,
            type_=type_,
            url=url,
        )

        get_issue_response_changelog_histories_history_metadata_cause.additional_properties = d
        return get_issue_response_changelog_histories_history_metadata_cause

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
