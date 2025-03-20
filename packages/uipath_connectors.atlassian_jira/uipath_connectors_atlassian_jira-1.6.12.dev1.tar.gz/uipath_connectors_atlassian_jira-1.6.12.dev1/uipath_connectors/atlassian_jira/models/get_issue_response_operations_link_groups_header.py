from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseOperationsLinkGroupsHeader")


@_attrs_define
class GetIssueResponseOperationsLinkGroupsHeader:
    """
    Attributes:
        href (Union[Unset, str]):
        icon_class (Union[Unset, str]):
        id (Union[Unset, str]):
        label (Union[Unset, str]):
        style_class (Union[Unset, str]):
        title (Union[Unset, str]):
        weight (Union[Unset, int]):
    """

    href: Union[Unset, str] = UNSET
    icon_class: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    label: Union[Unset, str] = UNSET
    style_class: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    weight: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        href = self.href

        icon_class = self.icon_class

        id = self.id

        label = self.label

        style_class = self.style_class

        title = self.title

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if href is not UNSET:
            field_dict["href"] = href
        if icon_class is not UNSET:
            field_dict["iconClass"] = icon_class
        if id is not UNSET:
            field_dict["id"] = id
        if label is not UNSET:
            field_dict["label"] = label
        if style_class is not UNSET:
            field_dict["styleClass"] = style_class
        if title is not UNSET:
            field_dict["title"] = title
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        href = d.pop("href", UNSET)

        icon_class = d.pop("iconClass", UNSET)

        id = d.pop("id", UNSET)

        label = d.pop("label", UNSET)

        style_class = d.pop("styleClass", UNSET)

        title = d.pop("title", UNSET)

        weight = d.pop("weight", UNSET)

        get_issue_response_operations_link_groups_header = cls(
            href=href,
            icon_class=icon_class,
            id=id,
            label=label,
            style_class=style_class,
            title=title,
            weight=weight,
        )

        get_issue_response_operations_link_groups_header.additional_properties = d
        return get_issue_response_operations_link_groups_header

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
