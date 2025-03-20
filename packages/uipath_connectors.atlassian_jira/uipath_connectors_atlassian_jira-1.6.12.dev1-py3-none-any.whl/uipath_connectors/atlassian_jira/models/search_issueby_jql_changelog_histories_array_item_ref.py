from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.search_issueby_jql_changelog_histories_author import (
        SearchIssuebyJQLChangelogHistoriesAuthor,
    )
    from ..models.search_issueby_jql_changelog_histories_items_array_item_ref import (
        SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef,
    )
    from ..models.search_issueby_jql_changelog_histories_history_metadata import (
        SearchIssuebyJQLChangelogHistoriesHistoryMetadata,
    )


T = TypeVar("T", bound="SearchIssuebyJQLChangelogHistoriesArrayItemRef")


@_attrs_define
class SearchIssuebyJQLChangelogHistoriesArrayItemRef:
    """
    Attributes:
        author (Union[Unset, SearchIssuebyJQLChangelogHistoriesAuthor]):
        created (Union[Unset, datetime.datetime]): The date on which the change took place.
        history_metadata (Union[Unset, SearchIssuebyJQLChangelogHistoriesHistoryMetadata]):
        id (Union[Unset, str]): The ID of the changelog.
        items (Union[Unset, list['SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef']]):
    """

    author: Union[Unset, "SearchIssuebyJQLChangelogHistoriesAuthor"] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    history_metadata: Union[
        Unset, "SearchIssuebyJQLChangelogHistoriesHistoryMetadata"
    ] = UNSET
    id: Union[Unset, str] = UNSET
    items: Union[Unset, list["SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef"]] = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        history_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.history_metadata, Unset):
            history_metadata = self.history_metadata.to_dict()

        id = self.id

        items: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.items, Unset):
            items = []
            for (
                componentsschemas_search_issueby_jql_changelog_histories_items_item_data
            ) in self.items:
                componentsschemas_search_issueby_jql_changelog_histories_items_item = componentsschemas_search_issueby_jql_changelog_histories_items_item_data.to_dict()
                items.append(
                    componentsschemas_search_issueby_jql_changelog_histories_items_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if author is not UNSET:
            field_dict["author"] = author
        if created is not UNSET:
            field_dict["created"] = created
        if history_metadata is not UNSET:
            field_dict["historyMetadata"] = history_metadata
        if id is not UNSET:
            field_dict["id"] = id
        if items is not UNSET:
            field_dict["items"] = items

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_changelog_histories_author import (
            SearchIssuebyJQLChangelogHistoriesAuthor,
        )
        from ..models.search_issueby_jql_changelog_histories_items_array_item_ref import (
            SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef,
        )
        from ..models.search_issueby_jql_changelog_histories_history_metadata import (
            SearchIssuebyJQLChangelogHistoriesHistoryMetadata,
        )

        d = src_dict.copy()
        _author = d.pop("author", UNSET)
        author: Union[Unset, SearchIssuebyJQLChangelogHistoriesAuthor]
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = SearchIssuebyJQLChangelogHistoriesAuthor.from_dict(_author)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _history_metadata = d.pop("historyMetadata", UNSET)
        history_metadata: Union[
            Unset, SearchIssuebyJQLChangelogHistoriesHistoryMetadata
        ]
        if isinstance(_history_metadata, Unset):
            history_metadata = UNSET
        else:
            history_metadata = (
                SearchIssuebyJQLChangelogHistoriesHistoryMetadata.from_dict(
                    _history_metadata
                )
            )

        id = d.pop("id", UNSET)

        items = []
        _items = d.pop("items", UNSET)
        for (
            componentsschemas_search_issueby_jql_changelog_histories_items_item_data
        ) in _items or []:
            componentsschemas_search_issueby_jql_changelog_histories_items_item = SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef.from_dict(
                componentsschemas_search_issueby_jql_changelog_histories_items_item_data
            )

            items.append(
                componentsschemas_search_issueby_jql_changelog_histories_items_item
            )

        search_issueby_jql_changelog_histories_array_item_ref = cls(
            author=author,
            created=created,
            history_metadata=history_metadata,
            id=id,
            items=items,
        )

        search_issueby_jql_changelog_histories_array_item_ref.additional_properties = d
        return search_issueby_jql_changelog_histories_array_item_ref

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
