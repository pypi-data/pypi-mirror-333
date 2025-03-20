from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_comments_author_avatar_urls import GetCommentsAuthorAvatarUrls


class GetCommentsAuthor(BaseModel):
    """
    Attributes:
        account_id (Optional[str]): The account ID of the user, which uniquely identifies the user across all Atlassian
            products. For example, *5b10ac8d82e05b22cc7d4ef5*.
        account_type (Optional[str]): The type of account represented by this user. This will be one of 'atlassian'
            (normal users), 'app' (application user) or 'customer' (Jira Service Desk customer user)
        active (Optional[bool]): Whether the user is active.
        avatar_urls (Optional[GetCommentsAuthorAvatarUrls]):
        display_name (Optional[str]): The display name of the user. Depending on the user’s privacy settings, this may
            return an alternative value.
        email_address (Optional[str]): The email address of the user. Depending on the user’s privacy settings, this may
            be returned as null.
        key (Optional[str]): This property is no longer available and will be removed from the documentation soon. See
            the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-
            api-migration-guide/) for details.
        name (Optional[str]): This property is no longer available and will be removed from the documentation soon. See
            the [deprecation notice](https://developer.atlassian.com/cloud/jira/platform/deprecation-notice-user-privacy-
            api-migration-guide/) for details.
        self_ (Optional[str]): The URL of the user.
        time_zone (Optional[str]): The time zone specified in the user's profile. Depending on the user’s privacy
            settings, this may be returned as null.
    """

    model_config = ConfigDict(extra="allow")

    account_id: Optional[str] = None
    account_type: Optional[str] = None
    active: Optional[bool] = None
    avatar_urls: Optional["GetCommentsAuthorAvatarUrls"] = None
    display_name: Optional[str] = None
    email_address: Optional[str] = None
    key: Optional[str] = None
    name: Optional[str] = None
    self_: Optional[str] = None
    time_zone: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetCommentsAuthor"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
