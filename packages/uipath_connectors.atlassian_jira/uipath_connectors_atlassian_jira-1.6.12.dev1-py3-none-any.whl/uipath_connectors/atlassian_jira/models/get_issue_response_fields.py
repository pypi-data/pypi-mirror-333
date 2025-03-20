from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_priority import (
        GetIssueResponseFieldsPriority,
    )
    from ..models.get_issue_response_fields_attachment_array_item_ref import (
        GetIssueResponseFieldsAttachmentArrayItemRef,
    )
    from ..models.get_issue_response_fields_versions_array_item_ref import (
        GetIssueResponseFieldsVersionsArrayItemRef,
    )
    from ..models.get_issue_response_fields_progress import (
        GetIssueResponseFieldsProgress,
    )
    from ..models.get_issue_response_fields_parent import GetIssueResponseFieldsParent
    from ..models.get_issue_response_fields_aggregateprogress import (
        GetIssueResponseFieldsAggregateprogress,
    )
    from ..models.get_issue_response_fields_watches import GetIssueResponseFieldsWatches
    from ..models.get_issue_response_fields_components_array_item_ref import (
        GetIssueResponseFieldsComponentsArrayItemRef,
    )
    from ..models.get_issue_response_fields_security import (
        GetIssueResponseFieldsSecurity,
    )
    from ..models.get_issue_response_fields_issuelinks_array_item_ref import (
        GetIssueResponseFieldsIssuelinksArrayItemRef,
    )
    from ..models.get_issue_response_fields_votes import GetIssueResponseFieldsVotes
    from ..models.get_issue_response_fields_fix_versions_array_item_ref import (
        GetIssueResponseFieldsFixVersionsArrayItemRef,
    )
    from ..models.get_issue_response_fields_timetracking import (
        GetIssueResponseFieldsTimetracking,
    )
    from ..models.get_issue_response_fields_issuetype import (
        GetIssueResponseFieldsIssuetype,
    )
    from ..models.get_issue_response_fields_status import GetIssueResponseFieldsStatus
    from ..models.get_issue_response_fields_creator import GetIssueResponseFieldsCreator
    from ..models.get_issue_response_fields_assignee import (
        GetIssueResponseFieldsAssignee,
    )
    from ..models.get_issue_response_fields_reporter import (
        GetIssueResponseFieldsReporter,
    )
    from ..models.get_issue_response_fields_project import GetIssueResponseFieldsProject


T = TypeVar("T", bound="GetIssueResponseFields")


@_attrs_define
class GetIssueResponseFields:
    """
    Attributes:
        aggregateprogress (Union[Unset, GetIssueResponseFieldsAggregateprogress]):
        assignee (Union[Unset, GetIssueResponseFieldsAssignee]):
        attachment (Union[Unset, list['GetIssueResponseFieldsAttachmentArrayItemRef']]):
        components (Union[Unset, list['GetIssueResponseFieldsComponentsArrayItemRef']]):
        created (Union[Unset, datetime.datetime]):
        creator (Union[Unset, GetIssueResponseFieldsCreator]):
        description (Union[Unset, str]):
        duedate (Union[Unset, datetime.date]):
        environment (Union[Unset, str]):
        fix_versions (Union[Unset, list['GetIssueResponseFieldsFixVersionsArrayItemRef']]):
        issuetype (Union[Unset, GetIssueResponseFieldsIssuetype]):
        labels (Union[Unset, list[str]]):
        parent (Union[Unset, GetIssueResponseFieldsParent]):
        priority (Union[Unset, GetIssueResponseFieldsPriority]):
        progress (Union[Unset, GetIssueResponseFieldsProgress]):
        project (Union[Unset, GetIssueResponseFieldsProject]):
        reporter (Union[Unset, GetIssueResponseFieldsReporter]):
        security (Union[Unset, GetIssueResponseFieldsSecurity]):
        status (Union[Unset, GetIssueResponseFieldsStatus]):
        statuscategorychangedate (Union[Unset, datetime.datetime]):
        summary (Union[Unset, str]):
        timetracking (Union[Unset, GetIssueResponseFieldsTimetracking]):
        updated (Union[Unset, datetime.datetime]):
        versions (Union[Unset, list['GetIssueResponseFieldsVersionsArrayItemRef']]):
        votes (Union[Unset, GetIssueResponseFieldsVotes]):
        watches (Union[Unset, GetIssueResponseFieldsWatches]):
        workratio (Union[Unset, int]):
        issuelinks (Union[Unset, list['GetIssueResponseFieldsIssuelinksArrayItemRef']]):
    """

    aggregateprogress: Union[Unset, "GetIssueResponseFieldsAggregateprogress"] = UNSET
    assignee: Union[Unset, "GetIssueResponseFieldsAssignee"] = UNSET
    attachment: Union[Unset, list["GetIssueResponseFieldsAttachmentArrayItemRef"]] = (
        UNSET
    )
    components: Union[Unset, list["GetIssueResponseFieldsComponentsArrayItemRef"]] = (
        UNSET
    )
    created: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, "GetIssueResponseFieldsCreator"] = UNSET
    description: Union[Unset, str] = UNSET
    duedate: Union[Unset, datetime.date] = UNSET
    environment: Union[Unset, str] = UNSET
    fix_versions: Union[
        Unset, list["GetIssueResponseFieldsFixVersionsArrayItemRef"]
    ] = UNSET
    issuetype: Union[Unset, "GetIssueResponseFieldsIssuetype"] = UNSET
    labels: Union[Unset, list[str]] = UNSET
    parent: Union[Unset, "GetIssueResponseFieldsParent"] = UNSET
    priority: Union[Unset, "GetIssueResponseFieldsPriority"] = UNSET
    progress: Union[Unset, "GetIssueResponseFieldsProgress"] = UNSET
    project: Union[Unset, "GetIssueResponseFieldsProject"] = UNSET
    reporter: Union[Unset, "GetIssueResponseFieldsReporter"] = UNSET
    security: Union[Unset, "GetIssueResponseFieldsSecurity"] = UNSET
    status: Union[Unset, "GetIssueResponseFieldsStatus"] = UNSET
    statuscategorychangedate: Union[Unset, datetime.datetime] = UNSET
    summary: Union[Unset, str] = UNSET
    timetracking: Union[Unset, "GetIssueResponseFieldsTimetracking"] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    versions: Union[Unset, list["GetIssueResponseFieldsVersionsArrayItemRef"]] = UNSET
    votes: Union[Unset, "GetIssueResponseFieldsVotes"] = UNSET
    watches: Union[Unset, "GetIssueResponseFieldsWatches"] = UNSET
    workratio: Union[Unset, int] = UNSET
    issuelinks: Union[Unset, list["GetIssueResponseFieldsIssuelinksArrayItemRef"]] = (
        UNSET
    )
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        aggregateprogress: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregateprogress, Unset):
            aggregateprogress = self.aggregateprogress.to_dict()

        assignee: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.assignee, Unset):
            assignee = self.assignee.to_dict()

        attachment: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attachment, Unset):
            attachment = []
            for (
                componentsschemas_get_issue_response_fields_attachment_item_data
            ) in self.attachment:
                componentsschemas_get_issue_response_fields_attachment_item = componentsschemas_get_issue_response_fields_attachment_item_data.to_dict()
                attachment.append(
                    componentsschemas_get_issue_response_fields_attachment_item
                )

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for (
                componentsschemas_get_issue_response_fields_components_item_data
            ) in self.components:
                componentsschemas_get_issue_response_fields_components_item = componentsschemas_get_issue_response_fields_components_item_data.to_dict()
                components.append(
                    componentsschemas_get_issue_response_fields_components_item
                )

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        creator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        description = self.description

        duedate: Union[Unset, str] = UNSET
        if not isinstance(self.duedate, Unset):
            duedate = self.duedate.isoformat()

        environment = self.environment

        fix_versions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.fix_versions, Unset):
            fix_versions = []
            for (
                componentsschemas_get_issue_response_fields_fix_versions_item_data
            ) in self.fix_versions:
                componentsschemas_get_issue_response_fields_fix_versions_item = componentsschemas_get_issue_response_fields_fix_versions_item_data.to_dict()
                fix_versions.append(
                    componentsschemas_get_issue_response_fields_fix_versions_item
                )

        issuetype: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuetype, Unset):
            issuetype = self.issuetype.to_dict()

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

        parent: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.parent, Unset):
            parent = self.parent.to_dict()

        priority: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.priority, Unset):
            priority = self.priority.to_dict()

        progress: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.progress, Unset):
            progress = self.progress.to_dict()

        project: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.project, Unset):
            project = self.project.to_dict()

        reporter: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reporter, Unset):
            reporter = self.reporter.to_dict()

        security: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.security, Unset):
            security = self.security.to_dict()

        status: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.to_dict()

        statuscategorychangedate: Union[Unset, str] = UNSET
        if not isinstance(self.statuscategorychangedate, Unset):
            statuscategorychangedate = self.statuscategorychangedate.isoformat()

        summary = self.summary

        timetracking: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.timetracking, Unset):
            timetracking = self.timetracking.to_dict()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        versions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.versions, Unset):
            versions = []
            for (
                componentsschemas_get_issue_response_fields_versions_item_data
            ) in self.versions:
                componentsschemas_get_issue_response_fields_versions_item = componentsschemas_get_issue_response_fields_versions_item_data.to_dict()
                versions.append(
                    componentsschemas_get_issue_response_fields_versions_item
                )

        votes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.votes, Unset):
            votes = self.votes.to_dict()

        watches: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.watches, Unset):
            watches = self.watches.to_dict()

        workratio = self.workratio

        issuelinks: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.issuelinks, Unset):
            issuelinks = []
            for (
                componentsschemas_get_issue_response_fields_issuelinks_item_data
            ) in self.issuelinks:
                componentsschemas_get_issue_response_fields_issuelinks_item = componentsschemas_get_issue_response_fields_issuelinks_item_data.to_dict()
                issuelinks.append(
                    componentsschemas_get_issue_response_fields_issuelinks_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregateprogress is not UNSET:
            field_dict["aggregateprogress"] = aggregateprogress
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
        if attachment is not UNSET:
            field_dict["attachment"] = attachment
        if components is not UNSET:
            field_dict["components"] = components
        if created is not UNSET:
            field_dict["created"] = created
        if creator is not UNSET:
            field_dict["creator"] = creator
        if description is not UNSET:
            field_dict["description"] = description
        if duedate is not UNSET:
            field_dict["duedate"] = duedate
        if environment is not UNSET:
            field_dict["environment"] = environment
        if fix_versions is not UNSET:
            field_dict["fixVersions"] = fix_versions
        if issuetype is not UNSET:
            field_dict["issuetype"] = issuetype
        if labels is not UNSET:
            field_dict["labels"] = labels
        if parent is not UNSET:
            field_dict["parent"] = parent
        if priority is not UNSET:
            field_dict["priority"] = priority
        if progress is not UNSET:
            field_dict["progress"] = progress
        if project is not UNSET:
            field_dict["project"] = project
        if reporter is not UNSET:
            field_dict["reporter"] = reporter
        if security is not UNSET:
            field_dict["security"] = security
        if status is not UNSET:
            field_dict["status"] = status
        if statuscategorychangedate is not UNSET:
            field_dict["statuscategorychangedate"] = statuscategorychangedate
        if summary is not UNSET:
            field_dict["summary"] = summary
        if timetracking is not UNSET:
            field_dict["timetracking"] = timetracking
        if updated is not UNSET:
            field_dict["updated"] = updated
        if versions is not UNSET:
            field_dict["versions"] = versions
        if votes is not UNSET:
            field_dict["votes"] = votes
        if watches is not UNSET:
            field_dict["watches"] = watches
        if workratio is not UNSET:
            field_dict["workratio"] = workratio
        if issuelinks is not UNSET:
            field_dict["issuelinks"] = issuelinks

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_priority import (
            GetIssueResponseFieldsPriority,
        )
        from ..models.get_issue_response_fields_attachment_array_item_ref import (
            GetIssueResponseFieldsAttachmentArrayItemRef,
        )
        from ..models.get_issue_response_fields_versions_array_item_ref import (
            GetIssueResponseFieldsVersionsArrayItemRef,
        )
        from ..models.get_issue_response_fields_progress import (
            GetIssueResponseFieldsProgress,
        )
        from ..models.get_issue_response_fields_parent import (
            GetIssueResponseFieldsParent,
        )
        from ..models.get_issue_response_fields_aggregateprogress import (
            GetIssueResponseFieldsAggregateprogress,
        )
        from ..models.get_issue_response_fields_watches import (
            GetIssueResponseFieldsWatches,
        )
        from ..models.get_issue_response_fields_components_array_item_ref import (
            GetIssueResponseFieldsComponentsArrayItemRef,
        )
        from ..models.get_issue_response_fields_security import (
            GetIssueResponseFieldsSecurity,
        )
        from ..models.get_issue_response_fields_issuelinks_array_item_ref import (
            GetIssueResponseFieldsIssuelinksArrayItemRef,
        )
        from ..models.get_issue_response_fields_votes import GetIssueResponseFieldsVotes
        from ..models.get_issue_response_fields_fix_versions_array_item_ref import (
            GetIssueResponseFieldsFixVersionsArrayItemRef,
        )
        from ..models.get_issue_response_fields_timetracking import (
            GetIssueResponseFieldsTimetracking,
        )
        from ..models.get_issue_response_fields_issuetype import (
            GetIssueResponseFieldsIssuetype,
        )
        from ..models.get_issue_response_fields_status import (
            GetIssueResponseFieldsStatus,
        )
        from ..models.get_issue_response_fields_creator import (
            GetIssueResponseFieldsCreator,
        )
        from ..models.get_issue_response_fields_assignee import (
            GetIssueResponseFieldsAssignee,
        )
        from ..models.get_issue_response_fields_reporter import (
            GetIssueResponseFieldsReporter,
        )
        from ..models.get_issue_response_fields_project import (
            GetIssueResponseFieldsProject,
        )

        d = src_dict.copy()
        _aggregateprogress = d.pop("aggregateprogress", UNSET)
        aggregateprogress: Union[Unset, GetIssueResponseFieldsAggregateprogress]
        if isinstance(_aggregateprogress, Unset):
            aggregateprogress = UNSET
        else:
            aggregateprogress = GetIssueResponseFieldsAggregateprogress.from_dict(
                _aggregateprogress
            )

        _assignee = d.pop("assignee", UNSET)
        assignee: Union[Unset, GetIssueResponseFieldsAssignee]
        if isinstance(_assignee, Unset):
            assignee = UNSET
        else:
            assignee = GetIssueResponseFieldsAssignee.from_dict(_assignee)

        attachment = []
        _attachment = d.pop("attachment", UNSET)
        for componentsschemas_get_issue_response_fields_attachment_item_data in (
            _attachment or []
        ):
            componentsschemas_get_issue_response_fields_attachment_item = (
                GetIssueResponseFieldsAttachmentArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_fields_attachment_item_data
                )
            )

            attachment.append(
                componentsschemas_get_issue_response_fields_attachment_item
            )

        components = []
        _components = d.pop("components", UNSET)
        for componentsschemas_get_issue_response_fields_components_item_data in (
            _components or []
        ):
            componentsschemas_get_issue_response_fields_components_item = (
                GetIssueResponseFieldsComponentsArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_fields_components_item_data
                )
            )

            components.append(
                componentsschemas_get_issue_response_fields_components_item
            )

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _creator = d.pop("creator", UNSET)
        creator: Union[Unset, GetIssueResponseFieldsCreator]
        if isinstance(_creator, Unset):
            creator = UNSET
        else:
            creator = GetIssueResponseFieldsCreator.from_dict(_creator)

        description = d.pop("description", UNSET)

        _duedate = d.pop("duedate", UNSET)
        duedate: Union[Unset, datetime.date]
        if isinstance(_duedate, Unset):
            duedate = UNSET
        else:
            duedate = isoparse(_duedate).date()

        environment = d.pop("environment", UNSET)

        fix_versions = []
        _fix_versions = d.pop("fixVersions", UNSET)
        for componentsschemas_get_issue_response_fields_fix_versions_item_data in (
            _fix_versions or []
        ):
            componentsschemas_get_issue_response_fields_fix_versions_item = (
                GetIssueResponseFieldsFixVersionsArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_fields_fix_versions_item_data
                )
            )

            fix_versions.append(
                componentsschemas_get_issue_response_fields_fix_versions_item
            )

        _issuetype = d.pop("issuetype", UNSET)
        issuetype: Union[Unset, GetIssueResponseFieldsIssuetype]
        if isinstance(_issuetype, Unset):
            issuetype = UNSET
        else:
            issuetype = GetIssueResponseFieldsIssuetype.from_dict(_issuetype)

        labels = cast(list[str], d.pop("labels", UNSET))

        _parent = d.pop("parent", UNSET)
        parent: Union[Unset, GetIssueResponseFieldsParent]
        if isinstance(_parent, Unset):
            parent = UNSET
        else:
            parent = GetIssueResponseFieldsParent.from_dict(_parent)

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, GetIssueResponseFieldsPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = GetIssueResponseFieldsPriority.from_dict(_priority)

        _progress = d.pop("progress", UNSET)
        progress: Union[Unset, GetIssueResponseFieldsProgress]
        if isinstance(_progress, Unset):
            progress = UNSET
        else:
            progress = GetIssueResponseFieldsProgress.from_dict(_progress)

        _project = d.pop("project", UNSET)
        project: Union[Unset, GetIssueResponseFieldsProject]
        if isinstance(_project, Unset):
            project = UNSET
        else:
            project = GetIssueResponseFieldsProject.from_dict(_project)

        _reporter = d.pop("reporter", UNSET)
        reporter: Union[Unset, GetIssueResponseFieldsReporter]
        if isinstance(_reporter, Unset):
            reporter = UNSET
        else:
            reporter = GetIssueResponseFieldsReporter.from_dict(_reporter)

        _security = d.pop("security", UNSET)
        security: Union[Unset, GetIssueResponseFieldsSecurity]
        if isinstance(_security, Unset):
            security = UNSET
        else:
            security = GetIssueResponseFieldsSecurity.from_dict(_security)

        _status = d.pop("status", UNSET)
        status: Union[Unset, GetIssueResponseFieldsStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = GetIssueResponseFieldsStatus.from_dict(_status)

        _statuscategorychangedate = d.pop("statuscategorychangedate", UNSET)
        statuscategorychangedate: Union[Unset, datetime.datetime]
        if isinstance(_statuscategorychangedate, Unset):
            statuscategorychangedate = UNSET
        else:
            statuscategorychangedate = isoparse(_statuscategorychangedate)

        summary = d.pop("summary", UNSET)

        _timetracking = d.pop("timetracking", UNSET)
        timetracking: Union[Unset, GetIssueResponseFieldsTimetracking]
        if isinstance(_timetracking, Unset):
            timetracking = UNSET
        else:
            timetracking = GetIssueResponseFieldsTimetracking.from_dict(_timetracking)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        versions = []
        _versions = d.pop("versions", UNSET)
        for componentsschemas_get_issue_response_fields_versions_item_data in (
            _versions or []
        ):
            componentsschemas_get_issue_response_fields_versions_item = (
                GetIssueResponseFieldsVersionsArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_fields_versions_item_data
                )
            )

            versions.append(componentsschemas_get_issue_response_fields_versions_item)

        _votes = d.pop("votes", UNSET)
        votes: Union[Unset, GetIssueResponseFieldsVotes]
        if isinstance(_votes, Unset):
            votes = UNSET
        else:
            votes = GetIssueResponseFieldsVotes.from_dict(_votes)

        _watches = d.pop("watches", UNSET)
        watches: Union[Unset, GetIssueResponseFieldsWatches]
        if isinstance(_watches, Unset):
            watches = UNSET
        else:
            watches = GetIssueResponseFieldsWatches.from_dict(_watches)

        workratio = d.pop("workratio", UNSET)

        issuelinks = []
        _issuelinks = d.pop("issuelinks", UNSET)
        for componentsschemas_get_issue_response_fields_issuelinks_item_data in (
            _issuelinks or []
        ):
            componentsschemas_get_issue_response_fields_issuelinks_item = (
                GetIssueResponseFieldsIssuelinksArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_fields_issuelinks_item_data
                )
            )

            issuelinks.append(
                componentsschemas_get_issue_response_fields_issuelinks_item
            )

        get_issue_response_fields = cls(
            aggregateprogress=aggregateprogress,
            assignee=assignee,
            attachment=attachment,
            components=components,
            created=created,
            creator=creator,
            description=description,
            duedate=duedate,
            environment=environment,
            fix_versions=fix_versions,
            issuetype=issuetype,
            labels=labels,
            parent=parent,
            priority=priority,
            progress=progress,
            project=project,
            reporter=reporter,
            security=security,
            status=status,
            statuscategorychangedate=statuscategorychangedate,
            summary=summary,
            timetracking=timetracking,
            updated=updated,
            versions=versions,
            votes=votes,
            watches=watches,
            workratio=workratio,
            issuelinks=issuelinks,
        )

        get_issue_response_fields.additional_properties = d
        return get_issue_response_fields

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
