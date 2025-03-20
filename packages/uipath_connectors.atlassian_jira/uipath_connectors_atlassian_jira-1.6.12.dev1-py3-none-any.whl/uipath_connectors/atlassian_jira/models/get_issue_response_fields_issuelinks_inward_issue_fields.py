from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_issuelinks_inward_issue_fields_status import (
        GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus,
    )


T = TypeVar("T", bound="GetIssueResponseFieldsIssuelinksInwardIssueFields")


@_attrs_define
class GetIssueResponseFieldsIssuelinksInwardIssueFields:
    """
    Attributes:
        status (Union[Unset, GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus]):
    """

    status: Union[Unset, "GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus"] = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_issuelinks_inward_issue_fields_status import (
            GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus,
        )

        d = src_dict.copy()
        _status = d.pop("status", UNSET)
        status: Union[Unset, GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetIssueResponseFieldsIssuelinksInwardIssueFieldsStatus.from_dict(
                _status
            )

        get_issue_response_fields_issuelinks_inward_issue_fields = cls(
            status=status,
        )

        get_issue_response_fields_issuelinks_inward_issue_fields.additional_properties = d
        return get_issue_response_fields_issuelinks_inward_issue_fields

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
