from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_issuelinks_inward_issue_fields import (
        GetIssueResponseFieldsIssuelinksInwardIssueFields,
    )


T = TypeVar("T", bound="GetIssueResponseFieldsIssuelinksInwardIssue")


@_attrs_define
class GetIssueResponseFieldsIssuelinksInwardIssue:
    """
    Attributes:
        id (Union[Unset, str]): The unique ID for the inwardly linked issue Example: 10004.
        key (Union[Unset, str]): The key identifier for the inwardly linked issue Example: PR-3.
        fields (Union[Unset, GetIssueResponseFieldsIssuelinksInwardIssueFields]):
        self_ (Union[Unset, str]): API endpoint URL for the linked inward issue Example: https://your-
            domain.atlassian.net/rest/api/3/issue/PR-3.
    """

    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    fields: Union[Unset, "GetIssueResponseFieldsIssuelinksInwardIssueFields"] = UNSET
    self_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        id = self.id

        key = self.key

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        self_ = self.self_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if fields is not UNSET:
            field_dict["fields"] = fields
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_issuelinks_inward_issue_fields import (
            GetIssueResponseFieldsIssuelinksInwardIssueFields,
        )

        d = src_dict.copy()
        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, GetIssueResponseFieldsIssuelinksInwardIssueFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = GetIssueResponseFieldsIssuelinksInwardIssueFields.from_dict(
                _fields
            )

        self_ = d.pop("self", UNSET)

        get_issue_response_fields_issuelinks_inward_issue = cls(
            id=id,
            key=key,
            fields=fields,
            self_=self_,
        )

        get_issue_response_fields_issuelinks_inward_issue.additional_properties = d
        return get_issue_response_fields_issuelinks_inward_issue

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
