from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsIssuelinksOutwardIssueFieldsStatus")


@_attrs_define
class GetIssueResponseFieldsIssuelinksOutwardIssueFieldsStatus:
    """
    Attributes:
        name (Union[Unset, str]): Name of the status for the linked outward issue Example: Open.
        icon_url (Union[Unset, str]): URL of the icon representing the status of the linked outward issue Example:
            https://your-domain.atlassian.net/images/icons/statuses/open.png.
    """

    name: Union[Unset, str] = UNSET
    icon_url: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        icon_url = self.icon_url

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        icon_url = d.pop("iconUrl", UNSET)

        get_issue_response_fields_issuelinks_outward_issue_fields_status = cls(
            name=name,
            icon_url=icon_url,
        )

        get_issue_response_fields_issuelinks_outward_issue_fields_status.additional_properties = d
        return get_issue_response_fields_issuelinks_outward_issue_fields_status

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
