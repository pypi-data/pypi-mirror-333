from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_issuelinks_outward_issue_fields import (
        GetIssueResponseFieldsIssuelinksOutwardIssueFields,
    )


T = TypeVar("T", bound="GetIssueResponseFieldsIssuelinksOutwardIssue")


@_attrs_define
class GetIssueResponseFieldsIssuelinksOutwardIssue:
    """
    Attributes:
        key (Union[Unset, str]): The key identifier for the outwardly linked issue Example: PR-2.
        fields (Union[Unset, GetIssueResponseFieldsIssuelinksOutwardIssueFields]):
        self_ (Union[Unset, str]): API endpoint URL for the linked outward issue Example: https://your-
            domain.atlassian.net/rest/api/3/issue/PR-2.
        id (Union[Unset, str]): The unique identifier for the linked outward issue Example: 10004L.
    """

    key: Union[Unset, str] = UNSET
    fields: Union[Unset, "GetIssueResponseFieldsIssuelinksOutwardIssueFields"] = UNSET
    self_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        key = self.key

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        self_ = self.self_

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if key is not UNSET:
            field_dict["key"] = key
        if fields is not UNSET:
            field_dict["fields"] = fields
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_issuelinks_outward_issue_fields import (
            GetIssueResponseFieldsIssuelinksOutwardIssueFields,
        )

        d = src_dict.copy()
        key = d.pop("key", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, GetIssueResponseFieldsIssuelinksOutwardIssueFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = GetIssueResponseFieldsIssuelinksOutwardIssueFields.from_dict(
                _fields
            )

        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        get_issue_response_fields_issuelinks_outward_issue = cls(
            key=key,
            fields=fields,
            self_=self_,
            id=id,
        )

        get_issue_response_fields_issuelinks_outward_issue.additional_properties = d
        return get_issue_response_fields_issuelinks_outward_issue

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
