from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.get_comments_visibility_visibility_type import (
    GetCommentsVisibilityVisibilityType,
)
from typing import Union


T = TypeVar("T", bound="GetCommentsVisibility")


@_attrs_define
class GetCommentsVisibility:
    """
    Attributes:
        type_ (Union[Unset, GetCommentsVisibilityVisibilityType]): Whether visibility of this item is restricted to a
            group or role.
        value (Union[Unset, str]): The name of the group or role to which visibility of this item is restricted.
    """

    type_: Union[Unset, GetCommentsVisibilityVisibilityType] = UNSET
    value: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        value = self.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["type"] = type_
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, GetCommentsVisibilityVisibilityType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = GetCommentsVisibilityVisibilityType(_type_)

        value = d.pop("value", UNSET)

        get_comments_visibility = cls(
            type_=type_,
            value=value,
        )

        get_comments_visibility.additional_properties = d
        return get_comments_visibility

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
