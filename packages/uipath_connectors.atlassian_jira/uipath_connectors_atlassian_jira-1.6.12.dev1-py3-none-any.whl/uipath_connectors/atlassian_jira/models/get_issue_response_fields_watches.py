from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetIssueResponseFieldsWatches")


@_attrs_define
class GetIssueResponseFieldsWatches:
    """
    Attributes:
        is_watching (Union[Unset, bool]):
        self_ (Union[Unset, str]):
        watch_count (Union[Unset, int]):
    """

    is_watching: Union[Unset, bool] = UNSET
    self_: Union[Unset, str] = UNSET
    watch_count: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        is_watching = self.is_watching

        self_ = self.self_

        watch_count = self.watch_count

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if is_watching is not UNSET:
            field_dict["isWatching"] = is_watching
        if self_ is not UNSET:
            field_dict["self"] = self_
        if watch_count is not UNSET:
            field_dict["watchCount"] = watch_count

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        is_watching = d.pop("isWatching", UNSET)

        self_ = d.pop("self", UNSET)

        watch_count = d.pop("watchCount", UNSET)

        get_issue_response_fields_watches = cls(
            is_watching=is_watching,
            self_=self_,
            watch_count=watch_count,
        )

        get_issue_response_fields_watches.additional_properties = d
        return get_issue_response_fields_watches

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
