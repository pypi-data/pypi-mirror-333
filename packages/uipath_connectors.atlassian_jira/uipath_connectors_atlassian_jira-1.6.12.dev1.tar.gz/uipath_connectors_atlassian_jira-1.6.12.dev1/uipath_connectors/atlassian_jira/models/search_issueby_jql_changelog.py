from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_changelog_histories_array_item_ref import (
        SearchIssuebyJQLChangelogHistoriesArrayItemRef,
    )


T = TypeVar("T", bound="SearchIssuebyJQLChangelog")


@_attrs_define
class SearchIssuebyJQLChangelog:
    """
    Attributes:
        histories (Union[Unset, list['SearchIssuebyJQLChangelogHistoriesArrayItemRef']]):
        max_results (Union[Unset, int]): The maximum number of results that could be on the page.
        start_at (Union[Unset, int]): The index of the first item returned on the page.
        total (Union[Unset, int]): The number of results on the page.
    """

    histories: Union[Unset, list["SearchIssuebyJQLChangelogHistoriesArrayItemRef"]] = (
        UNSET
    )
    max_results: Union[Unset, int] = UNSET
    start_at: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        histories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.histories, Unset):
            histories = []
            for (
                componentsschemas_search_issueby_jql_changelog_histories_item_data
            ) in self.histories:
                componentsschemas_search_issueby_jql_changelog_histories_item = componentsschemas_search_issueby_jql_changelog_histories_item_data.to_dict()
                histories.append(
                    componentsschemas_search_issueby_jql_changelog_histories_item
                )

        max_results = self.max_results

        start_at = self.start_at

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if histories is not UNSET:
            field_dict["histories"] = histories
        if max_results is not UNSET:
            field_dict["maxResults"] = max_results
        if start_at is not UNSET:
            field_dict["startAt"] = start_at
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_changelog_histories_array_item_ref import (
            SearchIssuebyJQLChangelogHistoriesArrayItemRef,
        )

        d = src_dict.copy()
        histories = []
        _histories = d.pop("histories", UNSET)
        for componentsschemas_search_issueby_jql_changelog_histories_item_data in (
            _histories or []
        ):
            componentsschemas_search_issueby_jql_changelog_histories_item = (
                SearchIssuebyJQLChangelogHistoriesArrayItemRef.from_dict(
                    componentsschemas_search_issueby_jql_changelog_histories_item_data
                )
            )

            histories.append(
                componentsschemas_search_issueby_jql_changelog_histories_item
            )

        max_results = d.pop("maxResults", UNSET)

        start_at = d.pop("startAt", UNSET)

        total = d.pop("total", UNSET)

        search_issueby_jql_changelog = cls(
            histories=histories,
            max_results=max_results,
            start_at=start_at,
            total=total,
        )

        search_issueby_jql_changelog.additional_properties = d
        return search_issueby_jql_changelog

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
