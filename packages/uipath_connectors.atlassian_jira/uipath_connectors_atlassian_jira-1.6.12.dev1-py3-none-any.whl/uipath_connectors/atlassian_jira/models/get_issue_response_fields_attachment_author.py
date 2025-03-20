from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_attachment_author_avatar_urls import (
        GetIssueResponseFieldsAttachmentAuthorAvatarUrls,
    )


T = TypeVar("T", bound="GetIssueResponseFieldsAttachmentAuthor")


@_attrs_define
class GetIssueResponseFieldsAttachmentAuthor:
    """
    Attributes:
        account_id (Union[Unset, str]): The author account ID of attachment
        email_address (Union[Unset, str]): The author email address of attachment
        display_name (Union[Unset, str]): The author display name of attachment
        account_type (Union[Unset, str]): The author account type of attachment
        self_ (Union[Unset, str]): The author self of attachment
        active (Union[Unset, bool]): Is attachment author active
        time_zone (Union[Unset, str]): The timezone of author
        avatar_urls (Union[Unset, GetIssueResponseFieldsAttachmentAuthorAvatarUrls]):
    """

    account_id: Union[Unset, str] = UNSET
    email_address: Union[Unset, str] = UNSET
    display_name: Union[Unset, str] = UNSET
    account_type: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    time_zone: Union[Unset, str] = UNSET
    avatar_urls: Union[Unset, "GetIssueResponseFieldsAttachmentAuthorAvatarUrls"] = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        account_id = self.account_id

        email_address = self.email_address

        display_name = self.display_name

        account_type = self.account_type

        self_ = self.self_

        active = self.active

        time_zone = self.time_zone

        avatar_urls: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.avatar_urls, Unset):
            avatar_urls = self.avatar_urls.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if account_type is not UNSET:
            field_dict["accountType"] = account_type
        if self_ is not UNSET:
            field_dict["self"] = self_
        if active is not UNSET:
            field_dict["active"] = active
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone
        if avatar_urls is not UNSET:
            field_dict["avatarUrls"] = avatar_urls

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_attachment_author_avatar_urls import (
            GetIssueResponseFieldsAttachmentAuthorAvatarUrls,
        )

        d = src_dict.copy()
        account_id = d.pop("accountId", UNSET)

        email_address = d.pop("emailAddress", UNSET)

        display_name = d.pop("displayName", UNSET)

        account_type = d.pop("accountType", UNSET)

        self_ = d.pop("self", UNSET)

        active = d.pop("active", UNSET)

        time_zone = d.pop("timeZone", UNSET)

        _avatar_urls = d.pop("avatarUrls", UNSET)
        avatar_urls: Union[Unset, GetIssueResponseFieldsAttachmentAuthorAvatarUrls]
        if isinstance(_avatar_urls, Unset):
            avatar_urls = UNSET
        else:
            avatar_urls = GetIssueResponseFieldsAttachmentAuthorAvatarUrls.from_dict(
                _avatar_urls
            )

        get_issue_response_fields_attachment_author = cls(
            account_id=account_id,
            email_address=email_address,
            display_name=display_name,
            account_type=account_type,
            self_=self_,
            active=active,
            time_zone=time_zone,
            avatar_urls=avatar_urls,
        )

        get_issue_response_fields_attachment_author.additional_properties = d
        return get_issue_response_fields_attachment_author

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
