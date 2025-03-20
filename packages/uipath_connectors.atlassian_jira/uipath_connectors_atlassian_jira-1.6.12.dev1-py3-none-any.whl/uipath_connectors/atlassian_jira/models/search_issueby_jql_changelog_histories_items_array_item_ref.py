from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef")


@_attrs_define
class SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef:
    """
    Attributes:
        field (Union[Unset, str]): The name of the field changed.
        field_id (Union[Unset, str]): The ID of the field changed.
        fieldtype (Union[Unset, str]): The type of the field changed.
        from_ (Union[Unset, str]): The details of the original value.
        from_string (Union[Unset, str]): The details of the original value as a string.
        to (Union[Unset, str]): The details of the new value.
        to_string (Union[Unset, str]): The details of the new value as a string.
    """

    field: Union[Unset, str] = UNSET
    field_id: Union[Unset, str] = UNSET
    fieldtype: Union[Unset, str] = UNSET
    from_: Union[Unset, str] = UNSET
    from_string: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    to_string: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        field = self.field

        field_id = self.field_id

        fieldtype = self.fieldtype

        from_ = self.from_

        from_string = self.from_string

        to = self.to

        to_string = self.to_string

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if field is not UNSET:
            field_dict["field"] = field
        if field_id is not UNSET:
            field_dict["fieldId"] = field_id
        if fieldtype is not UNSET:
            field_dict["fieldtype"] = fieldtype
        if from_ is not UNSET:
            field_dict["from"] = from_
        if from_string is not UNSET:
            field_dict["fromString"] = from_string
        if to is not UNSET:
            field_dict["to"] = to
        if to_string is not UNSET:
            field_dict["toString"] = to_string

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        field = d.pop("field", UNSET)

        field_id = d.pop("fieldId", UNSET)

        fieldtype = d.pop("fieldtype", UNSET)

        from_ = d.pop("from", UNSET)

        from_string = d.pop("fromString", UNSET)

        to = d.pop("to", UNSET)

        to_string = d.pop("toString", UNSET)

        search_issueby_jql_changelog_histories_items_array_item_ref = cls(
            field=field,
            field_id=field_id,
            fieldtype=fieldtype,
            from_=from_,
            from_string=from_string,
            to=to,
            to_string=to_string,
        )

        search_issueby_jql_changelog_histories_items_array_item_ref.additional_properties = d
        return search_issueby_jql_changelog_histories_items_array_item_ref

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
