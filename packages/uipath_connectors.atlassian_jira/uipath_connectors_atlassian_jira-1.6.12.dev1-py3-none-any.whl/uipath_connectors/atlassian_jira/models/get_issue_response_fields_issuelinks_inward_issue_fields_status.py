from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus")


@_attrs_define
class GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus:
    """
    Attributes:
        icon_url (Union[Unset, str]): URL of the icon representing the status of the linked inward issue Example:
            https://your-domain.atlassian.net/images/icons/statuses/open.png.
        name (Union[Unset, str]): The status name of the linked inward issue Example: Open.
    """

    icon_url: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        icon_url = self.icon_url

        name = self.name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        icon_url = d.pop("iconUrl", UNSET)

        name = d.pop("name", UNSET)

        get_issue_response_fields_issuelinks_inward_issue_fields_status = cls(
            icon_url=icon_url,
            name=name,
        )

        get_issue_response_fields_issuelinks_inward_issue_fields_status.additional_properties = d
        return get_issue_response_fields_issuelinks_inward_issue_fields_status

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
