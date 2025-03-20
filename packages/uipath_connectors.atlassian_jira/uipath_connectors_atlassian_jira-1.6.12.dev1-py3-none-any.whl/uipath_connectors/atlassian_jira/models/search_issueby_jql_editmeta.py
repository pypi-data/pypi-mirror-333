from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_editmeta_fields import (
        SearchIssuebyJQLEditmetaFields,
    )


T = TypeVar("T", bound="SearchIssuebyJQLEditmeta")


@_attrs_define
class SearchIssuebyJQLEditmeta:
    """
    Attributes:
        fields (Union[Unset, SearchIssuebyJQLEditmetaFields]):
    """

    fields: Union[Unset, "SearchIssuebyJQLEditmetaFields"] = UNSET
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
        from ..models.search_issueby_jql_editmeta_fields import (
            SearchIssuebyJQLEditmetaFields,
        )

        d = src_dict.copy()
        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, SearchIssuebyJQLEditmetaFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = SearchIssuebyJQLEditmetaFields.from_dict(_fields)

        search_issueby_jql_editmeta = cls(
            fields=fields,
        )

        search_issueby_jql_editmeta.additional_properties = d
        return search_issueby_jql_editmeta

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
