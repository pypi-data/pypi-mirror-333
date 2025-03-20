from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="AddCommentResponseUpdateAuthor")


@_attrs_define
class AddCommentResponseUpdateAuthor:
    """
    Attributes:
        self_ (Union[Unset, str]): The Update author self Example: https://your-
            domain.atlassian.net/rest/api/3/user?accountId=5b10a2844c20165700ede21g.
        account_id (Union[Unset, str]): The Update author account ID Example: 5b10a2844c20165700ede21g.
        active (Union[Unset, bool]): The Update author active
        display_name (Union[Unset, str]): The Update author display name Example: Mia Krystof.
    """

    self_: Union[Unset, str] = UNSET
    account_id: Union[Unset, str] = UNSET
    active: Union[Unset, bool] = UNSET
    display_name: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        self_ = self.self_

        account_id = self.account_id

        active = self.active

        display_name = self.display_name

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if self_ is not UNSET:
            field_dict["self"] = self_
        if account_id is not UNSET:
            field_dict["accountId"] = account_id
        if active is not UNSET:
            field_dict["active"] = active
        if display_name is not UNSET:
            field_dict["displayName"] = display_name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        self_ = d.pop("self", UNSET)

        account_id = d.pop("accountId", UNSET)

        active = d.pop("active", UNSET)

        display_name = d.pop("displayName", UNSET)

        add_comment_response_update_author = cls(
            self_=self_,
            account_id=account_id,
            active=active,
            display_name=display_name,
        )

        add_comment_response_update_author.additional_properties = d
        return add_comment_response_update_author

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
