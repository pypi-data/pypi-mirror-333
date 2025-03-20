from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_operations_link_groups_array_item_ref import (
        SearchIssuebyJQLOperationsLinkGroupsArrayItemRef,
    )


T = TypeVar("T", bound="SearchIssuebyJQLOperations")


@_attrs_define
class SearchIssuebyJQLOperations:
    """
    Attributes:
        link_groups (Union[Unset, list['SearchIssuebyJQLOperationsLinkGroupsArrayItemRef']]):
    """

    link_groups: Union[
        Unset, list["SearchIssuebyJQLOperationsLinkGroupsArrayItemRef"]
    ] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        link_groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.link_groups, Unset):
            link_groups = []
            for (
                componentsschemas_search_issueby_jql_operations_link_groups_item_data
            ) in self.link_groups:
                componentsschemas_search_issueby_jql_operations_link_groups_item = componentsschemas_search_issueby_jql_operations_link_groups_item_data.to_dict()
                link_groups.append(
                    componentsschemas_search_issueby_jql_operations_link_groups_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if link_groups is not UNSET:
            field_dict["linkGroups"] = link_groups

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_operations_link_groups_array_item_ref import (
            SearchIssuebyJQLOperationsLinkGroupsArrayItemRef,
        )

        d = src_dict.copy()
        link_groups = []
        _link_groups = d.pop("linkGroups", UNSET)
        for componentsschemas_search_issueby_jql_operations_link_groups_item_data in (
            _link_groups or []
        ):
            componentsschemas_search_issueby_jql_operations_link_groups_item = SearchIssuebyJQLOperationsLinkGroupsArrayItemRef.from_dict(
                componentsschemas_search_issueby_jql_operations_link_groups_item_data
            )

            link_groups.append(
                componentsschemas_search_issueby_jql_operations_link_groups_item
            )

        search_issueby_jql_operations = cls(
            link_groups=link_groups,
        )

        search_issueby_jql_operations.additional_properties = d
        return search_issueby_jql_operations

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
