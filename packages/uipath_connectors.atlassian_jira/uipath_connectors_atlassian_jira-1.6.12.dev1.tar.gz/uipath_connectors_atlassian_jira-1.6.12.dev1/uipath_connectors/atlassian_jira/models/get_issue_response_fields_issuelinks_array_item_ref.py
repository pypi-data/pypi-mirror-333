from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_issuelinks_type import (
        GetIssueResponseFieldsIssuelinksType,
    )
    from ..models.get_issue_response_fields_issuelinks_inward_issue import (
        GetIssueResponseFieldsIssuelinksInwardIssue,
    )
    from ..models.get_issue_response_fields_issuelinks_outward_issue import (
        GetIssueResponseFieldsIssuelinksOutwardIssue,
    )


T = TypeVar("T", bound="GetIssueResponseFieldsIssuelinksArrayItemRef")


@_attrs_define
class GetIssueResponseFieldsIssuelinksArrayItemRef:
    """
    Attributes:
        outward_issue (Union[Unset, GetIssueResponseFieldsIssuelinksOutwardIssue]):
        inward_issue (Union[Unset, GetIssueResponseFieldsIssuelinksInwardIssue]):
        type_ (Union[Unset, GetIssueResponseFieldsIssuelinksType]):
        id (Union[Unset, str]): The unique identifier for the issue link Example: 10001.
    """

    outward_issue: Union[Unset, "GetIssueResponseFieldsIssuelinksOutwardIssue"] = UNSET
    inward_issue: Union[Unset, "GetIssueResponseFieldsIssuelinksInwardIssue"] = UNSET
    type_: Union[Unset, "GetIssueResponseFieldsIssuelinksType"] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        outward_issue: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.outward_issue, Unset):
            outward_issue = self.outward_issue.to_dict()

        inward_issue: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.inward_issue, Unset):
            inward_issue = self.inward_issue.to_dict()

        type_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.to_dict()

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if outward_issue is not UNSET:
            field_dict["outwardIssue"] = outward_issue
        if inward_issue is not UNSET:
            field_dict["inwardIssue"] = inward_issue
        if type_ is not UNSET:
            field_dict["type"] = type_
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_issuelinks_type import (
            GetIssueResponseFieldsIssuelinksType,
        )
        from ..models.get_issue_response_fields_issuelinks_inward_issue import (
            GetIssueResponseFieldsIssuelinksInwardIssue,
        )
        from ..models.get_issue_response_fields_issuelinks_outward_issue import (
            GetIssueResponseFieldsIssuelinksOutwardIssue,
        )

        d = src_dict.copy()
        _outward_issue = d.pop("outwardIssue", UNSET)
        outward_issue: Union[Unset, GetIssueResponseFieldsIssuelinksOutwardIssue]
        if isinstance(_outward_issue, Unset):
            outward_issue = UNSET
        else:
            outward_issue = GetIssueResponseFieldsIssuelinksOutwardIssue.from_dict(
                _outward_issue
            )

        _inward_issue = d.pop("inwardIssue", UNSET)
        inward_issue: Union[Unset, GetIssueResponseFieldsIssuelinksInwardIssue]
        if isinstance(_inward_issue, Unset):
            inward_issue = UNSET
        else:
            inward_issue = GetIssueResponseFieldsIssuelinksInwardIssue.from_dict(
                _inward_issue
            )

        _type_ = d.pop("type", UNSET)
        type_: Union[Unset, GetIssueResponseFieldsIssuelinksType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = GetIssueResponseFieldsIssuelinksType.from_dict(_type_)

        id = d.pop("id", UNSET)

        get_issue_response_fields_issuelinks_array_item_ref = cls(
            outward_issue=outward_issue,
            inward_issue=inward_issue,
            type_=type_,
            id=id,
        )

        get_issue_response_fields_issuelinks_array_item_ref.additional_properties = d
        return get_issue_response_fields_issuelinks_array_item_ref

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
