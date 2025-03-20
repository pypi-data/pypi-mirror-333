from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseEditmetaFieldsSchema")


@_attrs_define
class GetIssueResponseEditmetaFieldsSchema:
    """
    Attributes:
        custom (Union[Unset, str]): If the field is a custom field, the URI of the field
        custom_id (Union[Unset, int]): If the field is a custom field, the custom ID of the field
        items (Union[Unset, str]): When the data type is an array, the name of the field items within the array
        system (Union[Unset, str]): If the field is a system field, the name of the field
        type_ (Union[Unset, str]): The data type of the field
    """

    custom: Union[Unset, str] = UNSET
    custom_id: Union[Unset, int] = UNSET
    items: Union[Unset, str] = UNSET
    system: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        custom = self.custom

        custom_id = self.custom_id

        items = self.items

        system = self.system

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if custom is not UNSET:
            field_dict["custom"] = custom
        if custom_id is not UNSET:
            field_dict["customId"] = custom_id
        if items is not UNSET:
            field_dict["items"] = items
        if system is not UNSET:
            field_dict["system"] = system
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        custom = d.pop("custom", UNSET)

        custom_id = d.pop("customId", UNSET)

        items = d.pop("items", UNSET)

        system = d.pop("system", UNSET)

        type_ = d.pop("type", UNSET)

        get_issue_response_editmeta_fields_schema = cls(
            custom=custom,
            custom_id=custom_id,
            items=items,
            system=system,
            type_=type_,
        )

        get_issue_response_editmeta_fields_schema.additional_properties = d
        return get_issue_response_editmeta_fields_schema

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
