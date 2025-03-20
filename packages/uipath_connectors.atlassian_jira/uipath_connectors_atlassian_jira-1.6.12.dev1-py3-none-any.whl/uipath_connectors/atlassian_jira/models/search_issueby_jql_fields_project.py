from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_fields_project_avatar_urls import (
        SearchIssuebyJQLFieldsProjectAvatarUrls,
    )


T = TypeVar("T", bound="SearchIssuebyJQLFieldsProject")


@_attrs_define
class SearchIssuebyJQLFieldsProject:
    """
    Attributes:
        avatar_urls (Union[Unset, SearchIssuebyJQLFieldsProjectAvatarUrls]):
        id (Union[Unset, str]):
        key (Union[Unset, str]): The unique key of the project in which the issue should be created.
        name (Union[Unset, str]):
        project_type_key (Union[Unset, str]):
        self_ (Union[Unset, str]):
        simplified (Union[Unset, bool]):
    """

    avatar_urls: Union[Unset, "SearchIssuebyJQLFieldsProjectAvatarUrls"] = UNSET
    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    project_type_key: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    simplified: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        avatar_urls: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.avatar_urls, Unset):
            avatar_urls = self.avatar_urls.to_dict()

        id = self.id

        key = self.key

        name = self.name

        project_type_key = self.project_type_key

        self_ = self.self_

        simplified = self.simplified

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if project_type_key is not UNSET:
            field_dict["projectTypeKey"] = project_type_key
        if self_ is not UNSET:
            field_dict["self"] = self_
        if simplified is not UNSET:
            field_dict["simplified"] = simplified

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_fields_project_avatar_urls import (
            SearchIssuebyJQLFieldsProjectAvatarUrls,
        )

        d = src_dict.copy()
        _avatar_urls = d.pop("avatarUrls", UNSET)
        avatar_urls: Union[Unset, SearchIssuebyJQLFieldsProjectAvatarUrls]
        if isinstance(_avatar_urls, Unset):
            avatar_urls = UNSET
        else:
            avatar_urls = SearchIssuebyJQLFieldsProjectAvatarUrls.from_dict(
                _avatar_urls
            )

        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        project_type_key = d.pop("projectTypeKey", UNSET)

        self_ = d.pop("self", UNSET)

        simplified = d.pop("simplified", UNSET)

        search_issueby_jql_fields_project = cls(
            avatar_urls=avatar_urls,
            id=id,
            key=key,
            name=name,
            project_type_key=project_type_key,
            self_=self_,
            simplified=simplified,
        )

        search_issueby_jql_fields_project.additional_properties = d
        return search_issueby_jql_fields_project

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
