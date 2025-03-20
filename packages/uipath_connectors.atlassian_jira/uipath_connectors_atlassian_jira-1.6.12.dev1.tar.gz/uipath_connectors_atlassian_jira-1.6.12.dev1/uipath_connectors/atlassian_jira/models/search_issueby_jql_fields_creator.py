from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_fields_creator_avatar_urls import (
        SearchIssuebyJQLFieldsCreatorAvatarUrls,
    )


T = TypeVar("T", bound="SearchIssuebyJQLFieldsCreator")


@_attrs_define
class SearchIssuebyJQLFieldsCreator:
    """
    Attributes:
        account_id (Union[Unset, str]):
        account_type (Union[Unset, str]):
        active (Union[Unset, bool]):
        avatar_urls (Union[Unset, SearchIssuebyJQLFieldsCreatorAvatarUrls]):
        display_name (Union[Unset, str]):
        email_address (Union[Unset, str]):
        self_ (Union[Unset, str]):
        time_zone (Union[Unset, str]):
    """

    account_id: Union[Unset, str] = UNSET
    account_type: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    avatar_urls: Union[Unset, "SearchIssuebyJQLFieldsCreatorAvatarUrls"] = UNSET
    display_name: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    time_zone: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        account_id = self.account_id

        account_type = self.account_type

        active = self.active

        avatar_urls: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.avatar_urls, Unset):
            avatar_urls = self.avatar_urls.to_dict()

        display_name = self.display_name

        email_address = self.email_address

        self_ = self.self_

        time_zone = self.time_zone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if account_type is not UNSET:
            field_dict["accountType"] = account_type
        if active is not UNSET:
            field_dict["active"] = active
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if self_ is not UNSET:
            field_dict["self"] = self_
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_fields_creator_avatar_urls import (
            SearchIssuebyJQLFieldsCreatorAvatarUrls,
        )

        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        account_type = d.pop("accountType", UNSET)

        active = d.pop("active", UNSET)

        _avatar_urls = d.pop("avatarUrls", UNSET)
        avatar_urls: Union[Unset, SearchIssuebyJQLFieldsCreatorAvatarUrls]
        if isinstance(_avatar_urls, Unset):
            avatar_urls = UNSET
        else:
            avatar_urls = SearchIssuebyJQLFieldsCreatorAvatarUrls.from_dict(
                _avatar_urls
            )

        display_name = d.pop("displayName", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        self_ = d.pop("self", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        search_issueby_jql_fields_creator = cls(
            account_id=account_id,
            account_type=account_type,
            active=active,
            avatar_urls=avatar_urls,
            display_name=display_name,
            email_address=email_address,
            self_=self_,
            time_zone=time_zone,
        )

        search_issueby_jql_fields_creator.additional_properties = d
        return search_issueby_jql_fields_creator

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
