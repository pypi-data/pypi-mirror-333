from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

import datetime
from ..models.get_issue_response_fields_fix_versions_array_item_ref import (
    GetIssueResponseFieldsFixVersionsArrayItemRef,
)
from ..models.get_issue_response_fields_watches import GetIssueResponseFieldsWatches
from ..models.get_issue_response_fields_creator import GetIssueResponseFieldsCreator
from ..models.get_issue_response_fields_issuelinks_array_item_ref import (
    GetIssueResponseFieldsIssuelinksArrayItemRef,
)
from ..models.get_issue_response_fields_security import GetIssueResponseFieldsSecurity
from ..models.get_issue_response_fields_assignee import GetIssueResponseFieldsAssignee
from ..models.get_issue_response_fields_aggregateprogress import (
    GetIssueResponseFieldsAggregateprogress,
)
from ..models.get_issue_response_fields_progress import GetIssueResponseFieldsProgress
from ..models.get_issue_response_fields_votes import GetIssueResponseFieldsVotes
from ..models.get_issue_response_fields_issuetype import GetIssueResponseFieldsIssuetype
from ..models.get_issue_response_fields_versions_array_item_ref import (
    GetIssueResponseFieldsVersionsArrayItemRef,
)
from ..models.get_issue_response_fields_reporter import GetIssueResponseFieldsReporter
from ..models.get_issue_response_fields_priority import GetIssueResponseFieldsPriority
from ..models.get_issue_response_fields_parent import GetIssueResponseFieldsParent
from ..models.get_issue_response_fields_components_array_item_ref import (
    GetIssueResponseFieldsComponentsArrayItemRef,
)
from ..models.get_issue_response_fields_status import GetIssueResponseFieldsStatus
from ..models.get_issue_response_fields_attachment_array_item_ref import (
    GetIssueResponseFieldsAttachmentArrayItemRef,
)
from ..models.get_issue_response_fields_timetracking import (
    GetIssueResponseFieldsTimetracking,
)
from ..models.get_issue_response_fields_project import GetIssueResponseFieldsProject


class GetIssueResponseFields(BaseModel):
    """
    Attributes:
        aggregateprogress (Optional[GetIssueResponseFieldsAggregateprogress]):
        assignee (Optional[GetIssueResponseFieldsAssignee]):
        attachment (Optional[list['GetIssueResponseFieldsAttachmentArrayItemRef']]):
        components (Optional[list['GetIssueResponseFieldsComponentsArrayItemRef']]):
        created (Optional[datetime.datetime]):
        creator (Optional[GetIssueResponseFieldsCreator]):
        description (Optional[str]):
        duedate (Optional[datetime.date]):
        environment (Optional[str]):
        fix_versions (Optional[list['GetIssueResponseFieldsFixVersionsArrayItemRef']]):
        issuetype (Optional[GetIssueResponseFieldsIssuetype]):
        labels (Optional[list[str]]):
        parent (Optional[GetIssueResponseFieldsParent]):
        priority (Optional[GetIssueResponseFieldsPriority]):
        progress (Optional[GetIssueResponseFieldsProgress]):
        project (Optional[GetIssueResponseFieldsProject]):
        reporter (Optional[GetIssueResponseFieldsReporter]):
        security (Optional[GetIssueResponseFieldsSecurity]):
        status (Optional[GetIssueResponseFieldsStatus]):
        statuscategorychangedate (Optional[datetime.datetime]):
        summary (Optional[str]):
        timetracking (Optional[GetIssueResponseFieldsTimetracking]):
        updated (Optional[datetime.datetime]):
        versions (Optional[list['GetIssueResponseFieldsVersionsArrayItemRef']]):
        votes (Optional[GetIssueResponseFieldsVotes]):
        watches (Optional[GetIssueResponseFieldsWatches]):
        workratio (Optional[int]):
        issuelinks (Optional[list['GetIssueResponseFieldsIssuelinksArrayItemRef']]):
    """

    model_config = ConfigDict(extra="allow")

    aggregateprogress: Optional["GetIssueResponseFieldsAggregateprogress"] = None
    assignee: Optional["GetIssueResponseFieldsAssignee"] = None
    attachment: Optional[list["GetIssueResponseFieldsAttachmentArrayItemRef"]] = None
    components: Optional[list["GetIssueResponseFieldsComponentsArrayItemRef"]] = None
    created: Optional[datetime.datetime] = None
    creator: Optional["GetIssueResponseFieldsCreator"] = None
    description: Optional[str] = None
    duedate: Optional[datetime.date] = None
    environment: Optional[str] = None
    fix_versions: Optional[list["GetIssueResponseFieldsFixVersionsArrayItemRef"]] = None
    issuetype: Optional["GetIssueResponseFieldsIssuetype"] = None
    labels: Optional[list[str]] = None
    parent: Optional["GetIssueResponseFieldsParent"] = None
    priority: Optional["GetIssueResponseFieldsPriority"] = None
    progress: Optional["GetIssueResponseFieldsProgress"] = None
    project: Optional["GetIssueResponseFieldsProject"] = None
    reporter: Optional["GetIssueResponseFieldsReporter"] = None
    security: Optional["GetIssueResponseFieldsSecurity"] = None
    status: Optional["GetIssueResponseFieldsStatus"] = None
    statuscategorychangedate: Optional[datetime.datetime] = None
    summary: Optional[str] = None
    timetracking: Optional["GetIssueResponseFieldsTimetracking"] = None
    updated: Optional[datetime.datetime] = None
    versions: Optional[list["GetIssueResponseFieldsVersionsArrayItemRef"]] = None
    votes: Optional["GetIssueResponseFieldsVotes"] = None
    watches: Optional["GetIssueResponseFieldsWatches"] = None
    workratio: Optional[int] = None
    issuelinks: Optional[list["GetIssueResponseFieldsIssuelinksArrayItemRef"]] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetIssueResponseFields"], src_dict: Dict[str, Any]):
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
