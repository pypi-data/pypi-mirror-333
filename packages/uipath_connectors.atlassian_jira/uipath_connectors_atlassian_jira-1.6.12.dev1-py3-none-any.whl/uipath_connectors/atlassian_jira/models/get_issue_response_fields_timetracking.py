from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsTimetracking")


@_attrs_define
class GetIssueResponseFieldsTimetracking:
    """
    Attributes:
        original_estimate (Union[Unset, str]):
        remaining_estimate (Union[Unset, str]):
    """

    original_estimate: Union[Unset, str] = UNSET
    remaining_estimate: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        original_estimate = self.original_estimate

        remaining_estimate = self.remaining_estimate

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if original_estimate is not UNSET:
            field_dict["originalEstimate"] = original_estimate
        if remaining_estimate is not UNSET:
            field_dict["remainingEstimate"] = remaining_estimate

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        original_estimate = d.pop("originalEstimate", UNSET)

        remaining_estimate = d.pop("remainingEstimate", UNSET)

        get_issue_response_fields_timetracking = cls(
            original_estimate=original_estimate,
            remaining_estimate=remaining_estimate,
        )

        get_issue_response_fields_timetracking.additional_properties = d
        return get_issue_response_fields_timetracking

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
