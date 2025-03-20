from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_update_comment import GetIssueResponseUpdateComment
    from ..models.get_issue_response_update_issuelink import (
        GetIssueResponseUpdateIssuelink,
    )
    from ..models.get_issue_response_update_issuelinks import (
        GetIssueResponseUpdateIssuelinks,
    )


T = TypeVar("T", bound="GetIssueResponseUpdate")


@_attrs_define
class GetIssueResponseUpdate:
    """
    Attributes:
        issuelink (Union[Unset, GetIssueResponseUpdateIssuelink]):
        issuelinks (Union[Unset, GetIssueResponseUpdateIssuelinks]):
        comment (Union[Unset, GetIssueResponseUpdateComment]):
    """

    issuelink: Union[Unset, "GetIssueResponseUpdateIssuelink"] = UNSET
    issuelinks: Union[Unset, "GetIssueResponseUpdateIssuelinks"] = UNSET
    comment: Union[Unset, "GetIssueResponseUpdateComment"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        issuelink: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuelink, Unset):
            issuelink = self.issuelink.to_dict()

        issuelinks: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuelinks, Unset):
            issuelinks = self.issuelinks.to_dict()

        comment: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.comment, Unset):
            comment = self.comment.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if issuelink is not UNSET:
            field_dict["issuelink"] = issuelink
        if issuelinks is not UNSET:
            field_dict["issuelinks"] = issuelinks
        if comment is not UNSET:
            field_dict["comment"] = comment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_update_comment import (
            GetIssueResponseUpdateComment,
        )
        from ..models.get_issue_response_update_issuelink import (
            GetIssueResponseUpdateIssuelink,
        )
        from ..models.get_issue_response_update_issuelinks import (
            GetIssueResponseUpdateIssuelinks,
        )

        d = src_dict.copy()
        _issuelink = d.pop("issuelink", UNSET)
        issuelink: Union[Unset, GetIssueResponseUpdateIssuelink]
        if isinstance(_issuelink, Unset):
            issuelink = UNSET
        else:
            issuelink = GetIssueResponseUpdateIssuelink.from_dict(_issuelink)

        _issuelinks = d.pop("issuelinks", UNSET)
        issuelinks: Union[Unset, GetIssueResponseUpdateIssuelinks]
        if isinstance(_issuelinks, Unset):
            issuelinks = UNSET
        else:
            issuelinks = GetIssueResponseUpdateIssuelinks.from_dict(_issuelinks)

        _comment = d.pop("comment", UNSET)
        comment: Union[Unset, GetIssueResponseUpdateComment]
        if isinstance(_comment, Unset):
            comment = UNSET
        else:
            comment = GetIssueResponseUpdateComment.from_dict(_comment)

        get_issue_response_update = cls(
            issuelink=issuelink,
            issuelinks=issuelinks,
            comment=comment,
        )

        get_issue_response_update.additional_properties = d
        return get_issue_response_update

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
