from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="SearchIssuebyJQLFieldsToInclude")


@_attrs_define
class SearchIssuebyJQLFieldsToInclude:
    """
    Attributes:
        actually_included (Union[Unset, list[str]]):
        excluded (Union[Unset, list[str]]):
        included (Union[Unset, list[str]]):
    """

    actually_included: Union[Unset, list[str]] = UNSET
    excluded: Union[Unset, list[str]] = UNSET
    included: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        actually_included: Union[Unset, list[str]] = UNSET
        if not isinstance(self.actually_included, Unset):
            actually_included = self.actually_included

        excluded: Union[Unset, list[str]] = UNSET
        if not isinstance(self.excluded, Unset):
            excluded = self.excluded

        included: Union[Unset, list[str]] = UNSET
        if not isinstance(self.included, Unset):
            included = self.included

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if actually_included is not UNSET:
            field_dict["actuallyIncluded"] = actually_included
        if excluded is not UNSET:
            field_dict["excluded"] = excluded
        if included is not UNSET:
            field_dict["included"] = included

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        actually_included = cast(list[str], d.pop("actuallyIncluded", UNSET))

        excluded = cast(list[str], d.pop("excluded", UNSET))

        included = cast(list[str], d.pop("included", UNSET))

        search_issueby_jql_fields_to_include = cls(
            actually_included=actually_included,
            excluded=excluded,
            included=included,
        )

        search_issueby_jql_fields_to_include.additional_properties = d
        return search_issueby_jql_fields_to_include

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
