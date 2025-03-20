from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_update import GetIssueResponseUpdate
from ..models.get_issue_response_changelog import GetIssueResponseChangelog
from ..models.get_issue_response_transitions_array_item_ref import (
    GetIssueResponseTransitionsArrayItemRef,
)
from ..models.get_issue_response_history_metadata import GetIssueResponseHistoryMetadata
from ..models.get_issue_response_transition import GetIssueResponseTransition
from ..models.get_issue_response_properties_array_item_ref import (
    GetIssueResponsePropertiesArrayItemRef,
)
from ..models.get_issue_response_fields import GetIssueResponseFields
from ..models.get_issue_response_fields_to_include import (
    GetIssueResponseFieldsToInclude,
)
from ..models.get_issue_response_operations import GetIssueResponseOperations
from ..models.get_issue_response_editmeta import GetIssueResponseEditmeta
from ..models.get_issue_response_schema import GetIssueResponseSchema


class GetIssueResponse(BaseModel):
    """
    Attributes:
        changelog (Optional[GetIssueResponseChangelog]):
        editmeta (Optional[GetIssueResponseEditmeta]):
        expand (Optional[str]): Expand options that include additional issue details in the response
        fields_to_include (Optional[GetIssueResponseFieldsToInclude]):
        update (Optional[GetIssueResponseUpdate]):
        fields (Optional[GetIssueResponseFields]):
        history_metadata (Optional[GetIssueResponseHistoryMetadata]):
        id (Optional[str]): The ID of the issue
        key (Optional[str]): The key of the issue
        operations (Optional[GetIssueResponseOperations]):
        properties (Optional[list['GetIssueResponsePropertiesArrayItemRef']]):
        schema (Optional[GetIssueResponseSchema]):
        self_ (Optional[str]): The URL of the issue details
        transition (Optional[GetIssueResponseTransition]):
        transitions (Optional[list['GetIssueResponseTransitionsArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow")

    changelog: Optional["GetIssueResponseChangelog"] = None
    editmeta: Optional["GetIssueResponseEditmeta"] = None
    expand: Optional[str] = None
    fields_to_include: Optional["GetIssueResponseFieldsToInclude"] = None
    update: Optional["GetIssueResponseUpdate"] = None
    fields: Optional["GetIssueResponseFields"] = None
    history_metadata: Optional["GetIssueResponseHistoryMetadata"] = None
    id: Optional[str] = None
    key: Optional[str] = None
    operations: Optional["GetIssueResponseOperations"] = None
    properties: Optional[list["GetIssueResponsePropertiesArrayItemRef"]] = None
    schema: Optional["GetIssueResponseSchema"] = None
    self_: Optional[str] = None
    transition: Optional["GetIssueResponseTransition"] = None
    transitions: Optional[list["GetIssueResponseTransitionsArrayItemRef"]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetIssueResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
