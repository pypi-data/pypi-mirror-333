from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.create_issue_request_fields_project import (
        CreateIssueRequestFieldsProject,
    )
    from ..models.create_issue_request_fields_issuetype import (
        CreateIssueRequestFieldsIssuetype,
    )


T = TypeVar("T", bound="CreateIssueRequestFields")


@_attrs_define
class CreateIssueRequestFields:
    """
    Attributes:
        project (Union[Unset, CreateIssueRequestFieldsProject]):
        issuetype (Union[Unset, CreateIssueRequestFieldsIssuetype]):
    """

    project: Union[Unset, "CreateIssueRequestFieldsProject"] = UNSET
    issuetype: Union[Unset, "CreateIssueRequestFieldsIssuetype"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        project: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.project, Unset):
            project = self.project.to_dict()

        issuetype: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuetype, Unset):
            issuetype = self.issuetype.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if project is not UNSET:
            field_dict["project"] = project
        if issuetype is not UNSET:
            field_dict["issuetype"] = issuetype

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_issue_request_fields_project import (
            CreateIssueRequestFieldsProject,
        )
        from ..models.create_issue_request_fields_issuetype import (
            CreateIssueRequestFieldsIssuetype,
        )

        d = src_dict.copy()
        _project = d.pop("project", UNSET)
        project: Union[Unset, CreateIssueRequestFieldsProject]
        if isinstance(_project, Unset):
            project = UNSET
        else:
            project = CreateIssueRequestFieldsProject.from_dict(_project)

        _issuetype = d.pop("issuetype", UNSET)
        issuetype: Union[Unset, CreateIssueRequestFieldsIssuetype]
        if isinstance(_issuetype, Unset):
            issuetype = UNSET
        else:
            issuetype = CreateIssueRequestFieldsIssuetype.from_dict(_issuetype)

        create_issue_request_fields = cls(
            project=project,
            issuetype=issuetype,
        )

        create_issue_request_fields.additional_properties = d
        return create_issue_request_fields

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
