from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_operations_link_groups_links_array_item_ref import (
        SearchIssuebyJQLOperationsLinkGroupsLinksArrayItemRef,
    )
    from ..models.search_issueby_jql_operations_link_groups_header import (
        SearchIssuebyJQLOperationsLinkGroupsHeader,
    )
    from ..models.search_issueby_jql_operations_link_groups_groups_array_item_ref import (
        SearchIssuebyJQLOperationsLinkGroupsGroupsArrayItemRef,
    )


T = TypeVar("T", bound="SearchIssuebyJQLOperationsLinkGroupsArrayItemRef")


@_attrs_define
class SearchIssuebyJQLOperationsLinkGroupsArrayItemRef:
    """
    Attributes:
        groups (Union[Unset, list['SearchIssuebyJQLOperationsLinkGroupsGroupsArrayItemRef']]):
        header (Union[Unset, SearchIssuebyJQLOperationsLinkGroupsHeader]):
        id (Union[Unset, str]):
        links (Union[Unset, list['SearchIssuebyJQLOperationsLinkGroupsLinksArrayItemRef']]):
        style_class (Union[Unset, str]):
        weight (Union[Unset, int]):
    """

    groups: Union[
        Unset, list["SearchIssuebyJQLOperationsLinkGroupsGroupsArrayItemRef"]
    ] = UNSET
    header: Union[Unset, "SearchIssuebyJQLOperationsLinkGroupsHeader"] = UNSET
    id: Union[Unset, str] = UNSET
    links: Union[
        Unset, list["SearchIssuebyJQLOperationsLinkGroupsLinksArrayItemRef"]
    ] = UNSET
    style_class: Union[Unset, str] = UNSET
    weight: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        groups: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = []
            for componentsschemas_search_issueby_jql_operations_link_groups_groups_item_data in self.groups:
                componentsschemas_search_issueby_jql_operations_link_groups_groups_item = componentsschemas_search_issueby_jql_operations_link_groups_groups_item_data.to_dict()
                groups.append(
                    componentsschemas_search_issueby_jql_operations_link_groups_groups_item
                )

        header: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.header, Unset):
            header = self.header.to_dict()

        id = self.id

        links: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.links, Unset):
            links = []
            for componentsschemas_search_issueby_jql_operations_link_groups_links_item_data in self.links:
                componentsschemas_search_issueby_jql_operations_link_groups_links_item = componentsschemas_search_issueby_jql_operations_link_groups_links_item_data.to_dict()
                links.append(
                    componentsschemas_search_issueby_jql_operations_link_groups_links_item
                )

        style_class = self.style_class

        weight = self.weight

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if groups is not UNSET:
            field_dict["groups"] = groups
        if header is not UNSET:
            field_dict["header"] = header
        if id is not UNSET:
            field_dict["id"] = id
        if links is not UNSET:
            field_dict["links"] = links
        if style_class is not UNSET:
            field_dict["styleClass"] = style_class
        if weight is not UNSET:
            field_dict["weight"] = weight

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_operations_link_groups_links_array_item_ref import (
            SearchIssuebyJQLOperationsLinkGroupsLinksArrayItemRef,
        )
        from ..models.search_issueby_jql_operations_link_groups_header import (
            SearchIssuebyJQLOperationsLinkGroupsHeader,
        )
        from ..models.search_issueby_jql_operations_link_groups_groups_array_item_ref import (
            SearchIssuebyJQLOperationsLinkGroupsGroupsArrayItemRef,
        )

        d = src_dict.copy()
        groups = []
        _groups = d.pop("groups", UNSET)
        for (
            componentsschemas_search_issueby_jql_operations_link_groups_groups_item_data
        ) in _groups or []:
            componentsschemas_search_issueby_jql_operations_link_groups_groups_item = SearchIssuebyJQLOperationsLinkGroupsGroupsArrayItemRef.from_dict(
                componentsschemas_search_issueby_jql_operations_link_groups_groups_item_data
            )

            groups.append(
                componentsschemas_search_issueby_jql_operations_link_groups_groups_item
            )

        _header = d.pop("header", UNSET)
        header: Union[Unset, SearchIssuebyJQLOperationsLinkGroupsHeader]
        if isinstance(_header, Unset):
            header = UNSET
        else:
            header = SearchIssuebyJQLOperationsLinkGroupsHeader.from_dict(_header)

        id = d.pop("id", UNSET)

        links = []
        _links = d.pop("links", UNSET)
        for (
            componentsschemas_search_issueby_jql_operations_link_groups_links_item_data
        ) in _links or []:
            componentsschemas_search_issueby_jql_operations_link_groups_links_item = SearchIssuebyJQLOperationsLinkGroupsLinksArrayItemRef.from_dict(
                componentsschemas_search_issueby_jql_operations_link_groups_links_item_data
            )

            links.append(
                componentsschemas_search_issueby_jql_operations_link_groups_links_item
            )

        style_class = d.pop("styleClass", UNSET)

        weight = d.pop("weight", UNSET)

        search_issueby_jql_operations_link_groups_array_item_ref = cls(
            groups=groups,
            header=header,
            id=id,
            links=links,
            style_class=style_class,
            weight=weight,
        )

        search_issueby_jql_operations_link_groups_array_item_ref.additional_properties = d
        return search_issueby_jql_operations_link_groups_array_item_ref

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
