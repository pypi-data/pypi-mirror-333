from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="GetIssueResponseTransitionErrorCollection")


@_attrs_define
class GetIssueResponseTransitionErrorCollection:
    """
    Attributes:
        error_messages (Union[Unset, list[str]]):
        status (Union[Unset, int]):
    """

    error_messages: Union[Unset, list[str]] = UNSET
    status: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        error_messages: Union[Unset, list[str]] = UNSET
        if not isinstance(self.error_messages, Unset):
            error_messages = self.error_messages

        status = self.status

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_messages is not UNSET:
            field_dict["errorMessages"] = error_messages
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        error_messages = cast(list[str], d.pop("errorMessages", UNSET))

        status = d.pop("status", UNSET)

        get_issue_response_transition_error_collection = cls(
            error_messages=error_messages,
            status=status,
        )

        get_issue_response_transition_error_collection.additional_properties = d
        return get_issue_response_transition_error_collection

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
