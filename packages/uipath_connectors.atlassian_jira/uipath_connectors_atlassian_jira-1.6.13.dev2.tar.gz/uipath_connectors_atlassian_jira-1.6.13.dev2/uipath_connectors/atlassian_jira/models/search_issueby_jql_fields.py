from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

import datetime
from ..models.search_issueby_jql_fields_creator import SearchIssuebyJQLFieldsCreator
from ..models.search_issueby_jql_fields_aggregateprogress import (
    SearchIssuebyJQLFieldsAggregateprogress,
)
from ..models.search_issueby_jql_fields_assignee import SearchIssuebyJQLFieldsAssignee
from ..models.search_issueby_jql_fields_issuetype import SearchIssuebyJQLFieldsIssuetype
from ..models.search_issueby_jql_fields_components_array_item_ref import (
    SearchIssuebyJQLFieldsComponentsArrayItemRef,
)
from ..models.search_issueby_jql_fields_votes import SearchIssuebyJQLFieldsVotes
from ..models.search_issueby_jql_fields_timetracking import (
    SearchIssuebyJQLFieldsTimetracking,
)
from ..models.search_issueby_jql_fields_priority import SearchIssuebyJQLFieldsPriority
from ..models.search_issueby_jql_fields_reporter import SearchIssuebyJQLFieldsReporter
from ..models.search_issueby_jql_fields_fix_versions_array_item_ref import (
    SearchIssuebyJQLFieldsFixVersionsArrayItemRef,
)
from ..models.search_issueby_jql_fields_watches import SearchIssuebyJQLFieldsWatches
from ..models.search_issueby_jql_fields_versions_array_item_ref import (
    SearchIssuebyJQLFieldsVersionsArrayItemRef,
)
from ..models.search_issueby_jql_fields_security import SearchIssuebyJQLFieldsSecurity
from ..models.search_issueby_jql_fields_project import SearchIssuebyJQLFieldsProject
from ..models.search_issueby_jql_fields_status import SearchIssuebyJQLFieldsStatus
from ..models.search_issueby_jql_fields_progress import SearchIssuebyJQLFieldsProgress


class SearchIssuebyJQLFields(BaseModel):
    """
    Attributes:
        aggregateprogress (Optional[SearchIssuebyJQLFieldsAggregateprogress]):
        assignee (Optional[SearchIssuebyJQLFieldsAssignee]):
        components (Optional[list['SearchIssuebyJQLFieldsComponentsArrayItemRef']]):
        created (Optional[datetime.datetime]):
        creator (Optional[SearchIssuebyJQLFieldsCreator]):
        description (Optional[str]):
        duedate (Optional[datetime.date]):
        environment (Optional[str]):
        fix_versions (Optional[list['SearchIssuebyJQLFieldsFixVersionsArrayItemRef']]):
        issuetype (Optional[SearchIssuebyJQLFieldsIssuetype]):
        labels (Optional[list[str]]):
        priority (Optional[SearchIssuebyJQLFieldsPriority]):
        progress (Optional[SearchIssuebyJQLFieldsProgress]):
        project (Optional[SearchIssuebyJQLFieldsProject]):
        reporter (Optional[SearchIssuebyJQLFieldsReporter]):
        security (Optional[SearchIssuebyJQLFieldsSecurity]):
        status (Optional[SearchIssuebyJQLFieldsStatus]):
        statuscategorychangedate (Optional[datetime.datetime]):
        summary (Optional[str]):
        timetracking (Optional[SearchIssuebyJQLFieldsTimetracking]):
        updated (Optional[datetime.datetime]):
        versions (Optional[list['SearchIssuebyJQLFieldsVersionsArrayItemRef']]):
        votes (Optional[SearchIssuebyJQLFieldsVotes]):
        watches (Optional[SearchIssuebyJQLFieldsWatches]):
        workratio (Optional[int]):
    """

    model_config = ConfigDict(extra="allow")

    aggregateprogress: Optional["SearchIssuebyJQLFieldsAggregateprogress"] = None
    assignee: Optional["SearchIssuebyJQLFieldsAssignee"] = None
    components: Optional[list["SearchIssuebyJQLFieldsComponentsArrayItemRef"]] = None
    created: Optional[datetime.datetime] = None
    creator: Optional["SearchIssuebyJQLFieldsCreator"] = None
    description: Optional[str] = None
    duedate: Optional[datetime.date] = None
    environment: Optional[str] = None
    fix_versions: Optional[list["SearchIssuebyJQLFieldsFixVersionsArrayItemRef"]] = None
    issuetype: Optional["SearchIssuebyJQLFieldsIssuetype"] = None
    labels: Optional[list[str]] = None
    priority: Optional["SearchIssuebyJQLFieldsPriority"] = None
    progress: Optional["SearchIssuebyJQLFieldsProgress"] = None
    project: Optional["SearchIssuebyJQLFieldsProject"] = None
    reporter: Optional["SearchIssuebyJQLFieldsReporter"] = None
    security: Optional["SearchIssuebyJQLFieldsSecurity"] = None
    status: Optional["SearchIssuebyJQLFieldsStatus"] = None
    statuscategorychangedate: Optional[datetime.datetime] = None
    summary: Optional[str] = None
    timetracking: Optional["SearchIssuebyJQLFieldsTimetracking"] = None
    updated: Optional[datetime.datetime] = None
    versions: Optional[list["SearchIssuebyJQLFieldsVersionsArrayItemRef"]] = None
    votes: Optional["SearchIssuebyJQLFieldsVotes"] = None
    watches: Optional["SearchIssuebyJQLFieldsWatches"] = None
    workratio: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SearchIssuebyJQLFields"], src_dict: Dict[str, Any]):
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
