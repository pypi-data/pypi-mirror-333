from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_changelog_histories_author_avatar_urls import (
        SearchIssuebyJQLChangelogHistoriesAuthorAvatarUrls,
    )


T = TypeVar("T", bound="SearchIssuebyJQLChangelogHistoriesAuthor")


@_attrs_define
class SearchIssuebyJQLChangelogHistoriesAuthor:
    """
    Attributes:
        account_id (Union[Unset, str]): The account ID of the user, which uniquely identifies the user across all
            Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*.
        account_type (Union[Unset, str]): The type of account represented by this user. This will be one of 'atlassian'
            (normal users), 'app' (application user) or 'customer' (Jira Service Desk customer user)
        active (Union[Unset, bool]): Whether the user is active.
        avatar_urls (Union[Unset, SearchIssuebyJQLChangelogHistoriesAuthorAvatarUrls]):
        display_name (Union[Unset, str]): The display name of the user. Depending on the user’s privacy settings, this
            may return an alternative value.
        email_address (Union[Unset, str]): The email address of the user. Depending on the user’s privacy settings, this
            may be returned as null.
        key (Union[Unset, str]): This property is no longer available and will be removed from the documentation soon.
            See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-
            privacy-api-migration-guide/) for details.
        name (Union[Unset, str]): This property is no longer available and will be removed from the documentation soon.
            See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-
            privacy-api-migration-guide/) for details.
        self_ (Union[Unset, str]): The URL of the user.
        time_zone (Union[Unset, str]): The time zone specified in the user's profile. Depending on the user’s privacy
            settings, this may be returned as null.
    """

    account_id: Union[Unset, str] = UNSET
    account_type: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    avatar_urls: Union[Unset, "SearchIssuebyJQLChangelogHistoriesAuthorAvatarUrls"] = (
        UNSET
    )
    display_name: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
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

        key = self.key

        name = self.name

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
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if self_ is not UNSET:
            field_dict["self"] = self_
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_changelog_histories_author_avatar_urls import (
            SearchIssuebyJQLChangelogHistoriesAuthorAvatarUrls,
        )

        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        account_type = d.pop("accountType", UNSET)

        active = d.pop("active", UNSET)

        _avatar_urls = d.pop("avatarUrls", UNSET)
        avatar_urls: Union[Unset, SearchIssuebyJQLChangelogHistoriesAuthorAvatarUrls]
        if isinstance(_avatar_urls, Unset):
            avatar_urls = UNSET
        else:
            avatar_urls = SearchIssuebyJQLChangelogHistoriesAuthorAvatarUrls.from_dict(
                _avatar_urls
            )

        display_name = d.pop("displayName", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        self_ = d.pop("self", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        search_issueby_jql_changelog_histories_author = cls(
            account_id=account_id,
            account_type=account_type,
            active=active,
            avatar_urls=avatar_urls,
            display_name=display_name,
            email_address=email_address,
            key=key,
            name=name,
            self_=self_,
            time_zone=time_zone,
        )

        search_issueby_jql_changelog_histories_author.additional_properties = d
        return search_issueby_jql_changelog_histories_author

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
