from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_editmeta_fields import (
        GetIssueResponseEditmetaFields,
    )


T = TypeVar("T", bound="GetIssueResponseEditmeta")


@_attrs_define
class GetIssueResponseEditmeta:
    """
    Attributes:
        fields (Union[Unset, GetIssueResponseEditmetaFields]):
    """

    fields: Union[Unset, "GetIssueResponseEditmetaFields"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if fields is not UNSET:
            field_dict["fields"] = fields

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_editmeta_fields import (
            GetIssueResponseEditmetaFields,
        )

        d = src_dict.copy()
        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, GetIssueResponseEditmetaFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = GetIssueResponseEditmetaFields.from_dict(_fields)

        get_issue_response_editmeta = cls(
            fields=fields,
        )

        get_issue_response_editmeta.additional_properties = d
        return get_issue_response_editmeta

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
