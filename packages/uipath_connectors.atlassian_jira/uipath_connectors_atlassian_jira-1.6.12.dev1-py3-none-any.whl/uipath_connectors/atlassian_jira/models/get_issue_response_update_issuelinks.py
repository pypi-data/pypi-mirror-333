from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_update_issuelinks_outward_issue import (
        GetIssueResponseUpdateIssuelinksOutwardIssue,
    )
    from ..models.get_issue_response_update_issuelinks_type import (
        GetIssueResponseUpdateIssuelinksType,
    )


T = TypeVar("T", bound="GetIssueResponseUpdateIssuelinks")


@_attrs_define
class GetIssueResponseUpdateIssuelinks:
    """
    Attributes:
        outward_issue (Union[Unset, GetIssueResponseUpdateIssuelinksOutwardIssue]):
        type_ (Union[Unset, GetIssueResponseUpdateIssuelinksType]):
    """

    outward_issue: Union[Unset, "GetIssueResponseUpdateIssuelinksOutwardIssue"] = UNSET
    type_: Union[Unset, "GetIssueResponseUpdateIssuelinksType"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        outward_issue: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.outward_issue, Unset):
            outward_issue = self.outward_issue.to_dict()

        type_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if outward_issue is not UNSET:
            field_dict["outwardIssue"] = outward_issue
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_update_issuelinks_outward_issue import (
            GetIssueResponseUpdateIssuelinksOutwardIssue,
        )
        from ..models.get_issue_response_update_issuelinks_type import (
            GetIssueResponseUpdateIssuelinksType,
        )

        d = src_dict.copy()
        _outward_issue = d.pop("outwardIssue", UNSET)
        outward_issue: Union[Unset, GetIssueResponseUpdateIssuelinksOutwardIssue]
        if isinstance(_outward_issue, Unset):
            outward_issue = UNSET
        else:
            outward_issue = GetIssueResponseUpdateIssuelinksOutwardIssue.from_dict(
                _outward_issue
            )

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, GetIssueResponseUpdateIssuelinksType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = GetIssueResponseUpdateIssuelinksType.from_dict(_type_)

        get_issue_response_update_issuelinks = cls(
            outward_issue=outward_issue,
            type_=type_,
        )

        get_issue_response_update_issuelinks.additional_properties = d
        return get_issue_response_update_issuelinks

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
