from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsPriority")


@_attrs_define
class GetIssueResponseFieldsPriority:
    """
    Attributes:
        icon_url (Union[Unset, str]):
        id (Union[Unset, str]):
        self_ (Union[Unset, str]):
    """

    icon_url: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        icon_url = self.icon_url

        id = self.id

        self_ = self.self_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if id is not UNSET:
            field_dict["id"] = id
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        icon_url = d.pop("iconUrl", UNSET)

        id = d.pop("id", UNSET)

        self_ = d.pop("self", UNSET)

        get_issue_response_fields_priority = cls(
            icon_url=icon_url,
            id=id,
            self_=self_,
        )

        get_issue_response_fields_priority.additional_properties = d
        return get_issue_response_fields_priority

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
