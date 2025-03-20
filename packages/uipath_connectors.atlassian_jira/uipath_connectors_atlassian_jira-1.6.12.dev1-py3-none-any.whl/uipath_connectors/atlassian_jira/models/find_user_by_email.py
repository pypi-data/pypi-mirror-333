from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.find_user_by_email_account_type import FindUserByEmailAccountType
from typing import Union

if TYPE_CHECKING:
    from ..models.find_user_by_email_groups import FindUserByEmailGroups
    from ..models.find_user_by_email_application_roles import (
        FindUserByEmailApplicationRoles,
    )
    from ..models.find_user_by_email_avatar_urls import FindUserByEmailAvatarUrls


T = TypeVar("T", bound="FindUserByEmail")


@_attrs_define
class FindUserByEmail:
    """
    Attributes:
        account_id (Union[Unset, str]): The account ID of the user, which uniquely identifies the user across all
            Atlassian products. For example, *5b10ac8d82e05b22cc7d4ef5*. Required in requests.
        account_type (Union[Unset, FindUserByEmailAccountType]): The user account type. Can take the following values:

             *  `atlassian` regular Atlassian user account
             *  `app` system account used for Connect applications and OAuth to represent external systems
             *  `customer` Jira Service Desk account representing an external service desk
        active (Union[Unset, bool]): Whether the user is active.
        application_roles (Union[Unset, FindUserByEmailApplicationRoles]):
        avatar_urls (Union[Unset, FindUserByEmailAvatarUrls]):
        display_name (Union[Unset, str]): The display name of the user. Depending on the user’s privacy setting, this
            may return an alternative value.
        email_address (Union[Unset, str]): The email address of the user. Depending on the user’s privacy setting, this
            may be returned as null.
        expand (Union[Unset, str]): Expand options that include additional user details in the response.
        groups (Union[Unset, FindUserByEmailGroups]):
        key (Union[Unset, str]): This property is no longer available and will be removed from the documentation soon.
            See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-
            privacy-api-migration-guide/) for details.
        locale (Union[Unset, str]): The locale of the user. Depending on the user’s privacy setting, this may be
            returned as null.
        name (Union[Unset, str]): This property is no longer available and will be removed from the documentation soon.
            See the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-
            privacy-api-migration-guide/) for details.
        self_ (Union[Unset, str]): The URL of the user.
        time_zone (Union[Unset, str]): The time zone specified in the user's profile. Depending on the user’s privacy
            setting, this may be returned as null.
    """

    account_id: Union[Unset, str] = UNSET
    account_type: Union[Unset, FindUserByEmailAccountType] = UNSET
    active: Union[Unset, bool] = UNSET
    application_roles: Union[Unset, "FindUserByEmailApplicationRoles"] = UNSET
    avatar_urls: Union[Unset, "FindUserByEmailAvatarUrls"] = UNSET
    display_name: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    expand: Union[Unset, str] = UNSET
    groups: Union[Unset, "FindUserByEmailGroups"] = UNSET
    key: Union[Unset, str] = UNSET
    locale: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    time_zone: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        account_id = self.account_id

        account_type: Union[Unset, str] = UNSET
        if not isinstance(self.account_type, Unset):
            account_type = self.account_type.value

        active = self.active

        application_roles: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.application_roles, Unset):
            application_roles = self.application_roles.to_dict()

        avatar_urls: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.avatar_urls, Unset):
            avatar_urls = self.avatar_urls.to_dict()

        display_name = self.display_name

        email_address = self.email_address

        expand = self.expand

        groups: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups.to_dict()

        key = self.key

        locale = self.locale

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
        if application_roles is not UNSET:
            field_dict["applicationRoles"] = application_roles
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if expand is not UNSET:
            field_dict["expand"] = expand
        if groups is not UNSET:
            field_dict["groups"] = groups
        if key is not UNSET:
            field_dict["key"] = key
        if locale is not UNSET:
            field_dict["locale"] = locale
        if name is not UNSET:
            field_dict["name"] = name
        if self_ is not UNSET:
            field_dict["self"] = self_
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.find_user_by_email_groups import FindUserByEmailGroups
        from ..models.find_user_by_email_application_roles import (
            FindUserByEmailApplicationRoles,
        )
        from ..models.find_user_by_email_avatar_urls import FindUserByEmailAvatarUrls

        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        _account_type = d.pop("accountType", UNSET)
        account_type: Union[Unset, FindUserByEmailAccountType]
        if isinstance(_account_type, Unset):
            account_type = UNSET
        else:
            account_type = FindUserByEmailAccountType(_account_type)

        active = d.pop("active", UNSET)

        _application_roles = d.pop("applicationRoles", UNSET)
        application_roles: Union[Unset, FindUserByEmailApplicationRoles]
        if isinstance(_application_roles, Unset):
            application_roles = UNSET
        else:
            application_roles = FindUserByEmailApplicationRoles.from_dict(
                _application_roles
            )

        _avatar_urls = d.pop("avatarUrls", UNSET)
        avatar_urls: Union[Unset, FindUserByEmailAvatarUrls]
        if isinstance(_avatar_urls, Unset):
            avatar_urls = UNSET
        else:
            avatar_urls = FindUserByEmailAvatarUrls.from_dict(_avatar_urls)

        display_name = d.pop("displayName", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        expand = d.pop("expand", UNSET)

        _groups = d.pop("groups", UNSET)
        groups: Union[Unset, FindUserByEmailGroups]
        if isinstance(_groups, Unset):
            groups = UNSET
        else:
            groups = FindUserByEmailGroups.from_dict(_groups)

        key = d.pop("key", UNSET)

        locale = d.pop("locale", UNSET)

        name = d.pop("name", UNSET)

        self_ = d.pop("self", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        find_user_by_email = cls(
            account_id=account_id,
            account_type=account_type,
            active=active,
            application_roles=application_roles,
            avatar_urls=avatar_urls,
            display_name=display_name,
            email_address=email_address,
            expand=expand,
            groups=groups,
            key=key,
            locale=locale,
            name=name,
            self_=self_,
            time_zone=time_zone,
        )

        find_user_by_email.additional_properties = d
        return find_user_by_email

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
