from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.find_user_by_email_application_roles_items_array_item_ref import (
        FindUserByEmailApplicationRolesItemsArrayItemRef,
    )


T = TypeVar("T", bound="FindUserByEmailApplicationRoles")


@_attrs_define
class FindUserByEmailApplicationRoles:
    """
    Attributes:
        items (Union[Unset, list['FindUserByEmailApplicationRolesItemsArrayItemRef']]):
        max_results (Union[Unset, int]):
        size (Union[Unset, int]):
    """

    items: Union[Unset, list["FindUserByEmailApplicationRolesItemsArrayItemRef"]] = (
        UNSET
    )
    max_results: Union[Unset, int] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for (
                componentsschemas_find_user_by_email_application_roles_items_item_data
            ) in self.items:
                componentsschemas_find_user_by_email_application_roles_items_item = componentsschemas_find_user_by_email_application_roles_items_item_data.to_dict()
                items.append(
                    componentsschemas_find_user_by_email_application_roles_items_item
                )

        max_results = self.max_results

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if items is not UNSET:
            field_dict["items"] = items
        if max_results is not UNSET:
            field_dict["max-results"] = max_results
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.find_user_by_email_application_roles_items_array_item_ref import (
            FindUserByEmailApplicationRolesItemsArrayItemRef,
        )

        d = src_dict.copy()
        items = []
        _items = d.pop("items", UNSET)
        for componentsschemas_find_user_by_email_application_roles_items_item_data in (
            _items or []
        ):
            componentsschemas_find_user_by_email_application_roles_items_item = FindUserByEmailApplicationRolesItemsArrayItemRef.from_dict(
                componentsschemas_find_user_by_email_application_roles_items_item_data
            )

            items.append(
                componentsschemas_find_user_by_email_application_roles_items_item
            )

        max_results = d.pop("max-results", UNSET)

        size = d.pop("size", UNSET)

        find_user_by_email_application_roles = cls(
            items=items,
            max_results=max_results,
            size=size,
        )

        find_user_by_email_application_roles.additional_properties = d
        return find_user_by_email_application_roles

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
