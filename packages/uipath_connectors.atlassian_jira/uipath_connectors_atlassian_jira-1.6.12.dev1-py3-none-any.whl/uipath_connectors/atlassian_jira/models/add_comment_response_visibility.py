from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="AddCommentResponseVisibility")


@_attrs_define
class AddCommentResponseVisibility:
    """
    Attributes:
        value (Union[Unset, str]): The Visibility value Example: Administrators.
        type_ (Union[Unset, str]): The Visibility type Example: role.
        identifier (Union[Unset, str]): The Visibility IDentifier Example: Administrators.
    """

    value: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    identifier: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        value = self.value

        type_ = self.type_

        identifier = self.identifier

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if type_ is not UNSET:
            field_dict["type"] = type_
        if identifier is not UNSET:
            field_dict["identifier"] = identifier

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        type_ = d.pop("type", UNSET)

        identifier = d.pop("identifier", UNSET)

        add_comment_response_visibility = cls(
            value=value,
            type_=type_,
            identifier=identifier,
        )

        add_comment_response_visibility.additional_properties = d
        return add_comment_response_visibility

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
