from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.search_issueby_jql_editmeta import SearchIssuebyJQLEditmeta
from ..models.search_issueby_jql_operations import SearchIssuebyJQLOperations
from ..models.search_issueby_jql_fields_to_include import (
    SearchIssuebyJQLFieldsToInclude,
)
from ..models.search_issueby_jql_changelog import SearchIssuebyJQLChangelog
from ..models.search_issueby_jql_fields import SearchIssuebyJQLFields
from ..models.search_issueby_jql_transitions_array_item_ref import (
    SearchIssuebyJQLTransitionsArrayItemRef,
)
from ..models.search_issueby_jql_schema import SearchIssuebyJQLSchema


class SearchIssuebyJQL(BaseModel):
    """
    Attributes:
        changelog (Optional[SearchIssuebyJQLChangelog]):
        editmeta (Optional[SearchIssuebyJQLEditmeta]):
        expand (Optional[str]): Expand options that include additional issue details in the response.
        fields_to_include (Optional[SearchIssuebyJQLFieldsToInclude]):
        fields (Optional[SearchIssuebyJQLFields]):
        id (Optional[str]): The ID of the issue.
        key (Optional[str]): The key of the issue.
        operations (Optional[SearchIssuebyJQLOperations]):
        schema (Optional[SearchIssuebyJQLSchema]):
        self_ (Optional[str]): The URL of the issue details.
        transitions (Optional[list['SearchIssuebyJQLTransitionsArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow")

    changelog: Optional["SearchIssuebyJQLChangelog"] = None
    editmeta: Optional["SearchIssuebyJQLEditmeta"] = None
    expand: Optional[str] = None
    fields_to_include: Optional["SearchIssuebyJQLFieldsToInclude"] = None
    fields: Optional["SearchIssuebyJQLFields"] = None
    id: Optional[str] = None
    key: Optional[str] = None
    operations: Optional["SearchIssuebyJQLOperations"] = None
    schema: Optional["SearchIssuebyJQLSchema"] = None
    self_: Optional[str] = None
    transitions: Optional[list["SearchIssuebyJQLTransitionsArrayItemRef"]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SearchIssuebyJQL"], src_dict: Dict[str, Any]):
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
