from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_transition_to_status_category import (
        GetIssueResponseTransitionToStatusCategory,
    )


T = TypeVar("T", bound="GetIssueResponseTransitionTo")


@_attrs_define
class GetIssueResponseTransitionTo:
    """
    Attributes:
        description (Union[Unset, str]): The description of the status
        icon_url (Union[Unset, str]): The URL of the icon used to represent the status
        id (Union[Unset, str]): The ID of the status
        name (Union[Unset, str]): The name of the status
        self_ (Union[Unset, str]): The URL of the status
        status_category (Union[Unset, GetIssueResponseTransitionToStatusCategory]):
    """

    description: Union[Unset, str] = UNSET
    icon_url: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    status_category: Union[Unset, "GetIssueResponseTransitionToStatusCategory"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        description = self.description

        icon_url = self.icon_url

        id = self.id

        name = self.name

        self_ = self.self_

        status_category: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status_category, Unset):
            status_category = self.status_category.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if description is not UNSET:
            field_dict["description"] = description
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if self_ is not UNSET:
            field_dict["self"] = self_
        if status_category is not UNSET:
            field_dict["statusCategory"] = status_category

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_transition_to_status_category import (
            GetIssueResponseTransitionToStatusCategory,
        )

        d = src_dict.copy()
        description = d.pop("description", UNSET)

        icon_url = d.pop("iconUrl", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        self_ = d.pop("self", UNSET)

        _status_category = d.pop("statusCategory", UNSET)
        status_category: Union[Unset, GetIssueResponseTransitionToStatusCategory]
        if isinstance(_status_category, Unset):
            status_category = UNSET
        else:
            status_category = GetIssueResponseTransitionToStatusCategory.from_dict(
                _status_category
            )

        get_issue_response_transition_to = cls(
            description=description,
            icon_url=icon_url,
            id=id,
            name=name,
            self_=self_,
            status_category=status_category,
        )

        get_issue_response_transition_to.additional_properties = d
        return get_issue_response_transition_to

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
