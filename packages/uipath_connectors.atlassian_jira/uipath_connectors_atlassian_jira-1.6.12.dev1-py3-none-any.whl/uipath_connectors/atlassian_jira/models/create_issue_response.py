from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.create_issue_response_fields import CreateIssueResponseFields


T = TypeVar("T", bound="CreateIssueResponse")


@_attrs_define
class CreateIssueResponse:
    """
    Attributes:
        fields (Union[Unset, CreateIssueResponseFields]):
        id (Union[Unset, str]): The ID of the issue
        key (Union[Unset, str]): The key of the issue
    """

    fields: Union[Unset, "CreateIssueResponseFields"] = UNSET
    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        id = self.id

        key = self.key

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_issue_response_fields import CreateIssueResponseFields

        d = src_dict.copy()
        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, CreateIssueResponseFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = CreateIssueResponseFields.from_dict(_fields)

        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        create_issue_response = cls(
            fields=fields,
            id=id,
            key=key,
        )

        create_issue_response.additional_properties = d
        return create_issue_response

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
