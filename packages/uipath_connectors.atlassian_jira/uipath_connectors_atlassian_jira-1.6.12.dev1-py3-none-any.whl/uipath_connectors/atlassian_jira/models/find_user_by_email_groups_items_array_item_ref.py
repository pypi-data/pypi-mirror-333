from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="FindUserByEmailGroupsItemsArrayItemRef")


@_attrs_define
class FindUserByEmailGroupsItemsArrayItemRef:
    """
    Attributes:
        name (Union[Unset, str]): The name of group.
        self_ (Union[Unset, str]): The URL for these group details.
    """

    name: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        name = self.name

        self_ = self.self_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if name is not UNSET:
            field_dict["name"] = name
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name", UNSET)

        self_ = d.pop("self", UNSET)

        find_user_by_email_groups_items_array_item_ref = cls(
            name=name,
            self_=self_,
        )

        find_user_by_email_groups_items_array_item_ref.additional_properties = d
        return find_user_by_email_groups_items_array_item_ref

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
