from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsAggregateprogress")


@_attrs_define
class GetIssueResponseFieldsAggregateprogress:
    """
    Attributes:
        progress (Union[Unset, int]):
        total (Union[Unset, int]):
    """

    progress: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        progress = self.progress

        total = self.total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if progress is not UNSET:
            field_dict["progress"] = progress
        if total is not UNSET:
            field_dict["total"] = total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        progress = d.pop("progress", UNSET)

        total = d.pop("total", UNSET)

        get_issue_response_fields_aggregateprogress = cls(
            progress=progress,
            total=total,
        )

        get_issue_response_fields_aggregateprogress.additional_properties = d
        return get_issue_response_fields_aggregateprogress

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
