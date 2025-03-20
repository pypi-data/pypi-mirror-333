from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsIssuetype")


@_attrs_define
class GetIssueResponseFieldsIssuetype:
    """
    Attributes:
        avatar_id (Union[Unset, int]):
        description (Union[Unset, str]):
        entity_id (Union[Unset, str]):
        hierarchy_level (Union[Unset, int]):
        icon_url (Union[Unset, str]):
        id (Union[Unset, str]): The type of the issue (task, story, bug, epic, etc). Select one to enable custom fields
        name (Union[Unset, str]):
        self_ (Union[Unset, str]):
        subtask (Union[Unset, bool]):
    """

    avatar_id: Union[Unset, int] = UNSET
    description: Union[Unset, str] = UNSET
    entity_id: Union[Unset, str] = UNSET
    hierarchy_level: Union[Unset, int] = UNSET
    icon_url: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    subtask: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        avatar_id = self.avatar_id

        description = self.description

        entity_id = self.entity_id

        hierarchy_level = self.hierarchy_level

        icon_url = self.icon_url

        id = self.id

        name = self.name

        self_ = self.self_

        subtask = self.subtask

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if avatar_id is not UNSET:
            field_dict["avatarId"] = avatar_id
        if description is not UNSET:
            field_dict["description"] = description
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if hierarchy_level is not UNSET:
            field_dict["hierarchyLevel"] = hierarchy_level
        if icon_url is not UNSET:
            field_dict["iconUrl"] = icon_url
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if self_ is not UNSET:
            field_dict["self"] = self_
        if subtask is not UNSET:
            field_dict["subtask"] = subtask

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        avatar_id = d.pop("avatarId", UNSET)

        description = d.pop("description", UNSET)

        entity_id = d.pop("entityId", UNSET)

        hierarchy_level = d.pop("hierarchyLevel", UNSET)

        icon_url = d.pop("iconUrl", UNSET)

        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        self_ = d.pop("self", UNSET)

        subtask = d.pop("subtask", UNSET)

        get_issue_response_fields_issuetype = cls(
            avatar_id=avatar_id,
            description=description,
            entity_id=entity_id,
            hierarchy_level=hierarchy_level,
            icon_url=icon_url,
            id=id,
            name=name,
            self_=self_,
            subtask=subtask,
        )

        get_issue_response_fields_issuetype.additional_properties = d
        return get_issue_response_fields_issuetype

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
