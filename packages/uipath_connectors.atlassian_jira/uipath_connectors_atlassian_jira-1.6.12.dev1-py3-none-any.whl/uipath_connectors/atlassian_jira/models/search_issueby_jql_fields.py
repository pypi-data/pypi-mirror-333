from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.search_issueby_jql_fields_versions_array_item_ref import (
        SearchIssuebyJQLFieldsVersionsArrayItemRef,
    )
    from ..models.search_issueby_jql_fields_project import SearchIssuebyJQLFieldsProject
    from ..models.search_issueby_jql_fields_watches import SearchIssuebyJQLFieldsWatches
    from ..models.search_issueby_jql_fields_priority import (
        SearchIssuebyJQLFieldsPriority,
    )
    from ..models.search_issueby_jql_fields_security import (
        SearchIssuebyJQLFieldsSecurity,
    )
    from ..models.search_issueby_jql_fields_fix_versions_array_item_ref import (
        SearchIssuebyJQLFieldsFixVersionsArrayItemRef,
    )
    from ..models.search_issueby_jql_fields_progress import (
        SearchIssuebyJQLFieldsProgress,
    )
    from ..models.search_issueby_jql_fields_reporter import (
        SearchIssuebyJQLFieldsReporter,
    )
    from ..models.search_issueby_jql_fields_timetracking import (
        SearchIssuebyJQLFieldsTimetracking,
    )
    from ..models.search_issueby_jql_fields_votes import SearchIssuebyJQLFieldsVotes
    from ..models.search_issueby_jql_fields_status import SearchIssuebyJQLFieldsStatus
    from ..models.search_issueby_jql_fields_creator import SearchIssuebyJQLFieldsCreator
    from ..models.search_issueby_jql_fields_aggregateprogress import (
        SearchIssuebyJQLFieldsAggregateprogress,
    )
    from ..models.search_issueby_jql_fields_assignee import (
        SearchIssuebyJQLFieldsAssignee,
    )
    from ..models.search_issueby_jql_fields_issuetype import (
        SearchIssuebyJQLFieldsIssuetype,
    )
    from ..models.search_issueby_jql_fields_components_array_item_ref import (
        SearchIssuebyJQLFieldsComponentsArrayItemRef,
    )


T = TypeVar("T", bound="SearchIssuebyJQLFields")


@_attrs_define
class SearchIssuebyJQLFields:
    """
    Attributes:
        aggregateprogress (Union[Unset, SearchIssuebyJQLFieldsAggregateprogress]):
        assignee (Union[Unset, SearchIssuebyJQLFieldsAssignee]):
        components (Union[Unset, list['SearchIssuebyJQLFieldsComponentsArrayItemRef']]):
        created (Union[Unset, datetime.datetime]):
        creator (Union[Unset, SearchIssuebyJQLFieldsCreator]):
        description (Union[Unset, str]):
        duedate (Union[Unset, datetime.date]):
        environment (Union[Unset, str]):
        fix_versions (Union[Unset, list['SearchIssuebyJQLFieldsFixVersionsArrayItemRef']]):
        issuetype (Union[Unset, SearchIssuebyJQLFieldsIssuetype]):
        labels (Union[Unset, list[str]]):
        priority (Union[Unset, SearchIssuebyJQLFieldsPriority]):
        progress (Union[Unset, SearchIssuebyJQLFieldsProgress]):
        project (Union[Unset, SearchIssuebyJQLFieldsProject]):
        reporter (Union[Unset, SearchIssuebyJQLFieldsReporter]):
        security (Union[Unset, SearchIssuebyJQLFieldsSecurity]):
        status (Union[Unset, SearchIssuebyJQLFieldsStatus]):
        statuscategorychangedate (Union[Unset, datetime.datetime]):
        summary (Union[Unset, str]):
        timetracking (Union[Unset, SearchIssuebyJQLFieldsTimetracking]):
        updated (Union[Unset, datetime.datetime]):
        versions (Union[Unset, list['SearchIssuebyJQLFieldsVersionsArrayItemRef']]):
        votes (Union[Unset, SearchIssuebyJQLFieldsVotes]):
        watches (Union[Unset, SearchIssuebyJQLFieldsWatches]):
        workratio (Union[Unset, int]):
    """

    aggregateprogress: Union[Unset, "SearchIssuebyJQLFieldsAggregateprogress"] = UNSET
    assignee: Union[Unset, "SearchIssuebyJQLFieldsAssignee"] = UNSET
    components: Union[Unset, list["SearchIssuebyJQLFieldsComponentsArrayItemRef"]] = (
        UNSET
    )
    created: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, "SearchIssuebyJQLFieldsCreator"] = UNSET
    description: Union[Unset, str] = UNSET
    duedate: Union[Unset, datetime.date] = UNSET
    environment: Union[Unset, str] = UNSET
    fix_versions: Union[
        Unset, list["SearchIssuebyJQLFieldsFixVersionsArrayItemRef"]
    ] = UNSET
    issuetype: Union[Unset, "SearchIssuebyJQLFieldsIssuetype"] = UNSET
    labels: Union[Unset, list[str]] = UNSET
    priority: Union[Unset, "SearchIssuebyJQLFieldsPriority"] = UNSET
    progress: Union[Unset, "SearchIssuebyJQLFieldsProgress"] = UNSET
    project: Union[Unset, "SearchIssuebyJQLFieldsProject"] = UNSET
    reporter: Union[Unset, "SearchIssuebyJQLFieldsReporter"] = UNSET
    security: Union[Unset, "SearchIssuebyJQLFieldsSecurity"] = UNSET
    status: Union[Unset, "SearchIssuebyJQLFieldsStatus"] = UNSET
    statuscategorychangedate: Union[Unset, datetime.datetime] = UNSET
    summary: Union[Unset, str] = UNSET
    timetracking: Union[Unset, "SearchIssuebyJQLFieldsTimetracking"] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    versions: Union[Unset, list["SearchIssuebyJQLFieldsVersionsArrayItemRef"]] = UNSET
    votes: Union[Unset, "SearchIssuebyJQLFieldsVotes"] = UNSET
    watches: Union[Unset, "SearchIssuebyJQLFieldsWatches"] = UNSET
    workratio: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        aggregateprogress: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.aggregateprogress, Unset):
            aggregateprogress = self.aggregateprogress.to_dict()

        assignee: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.assignee, Unset):
            assignee = self.assignee.to_dict()

        components: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.components, Unset):
            components = []
            for (
                componentsschemas_search_issueby_jql_fields_components_item_data
            ) in self.components:
                componentsschemas_search_issueby_jql_fields_components_item = componentsschemas_search_issueby_jql_fields_components_item_data.to_dict()
                components.append(
                    componentsschemas_search_issueby_jql_fields_components_item
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
                componentsschemas_search_issueby_jql_fields_fix_versions_item_data
            ) in self.fix_versions:
                componentsschemas_search_issueby_jql_fields_fix_versions_item = componentsschemas_search_issueby_jql_fields_fix_versions_item_data.to_dict()
                fix_versions.append(
                    componentsschemas_search_issueby_jql_fields_fix_versions_item
                )

        issuetype: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.issuetype, Unset):
            issuetype = self.issuetype.to_dict()

        labels: Union[Unset, list[str]] = UNSET
        if not isinstance(self.labels, Unset):
            labels = self.labels

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
                componentsschemas_search_issueby_jql_fields_versions_item_data
            ) in self.versions:
                componentsschemas_search_issueby_jql_fields_versions_item = componentsschemas_search_issueby_jql_fields_versions_item_data.to_dict()
                versions.append(
                    componentsschemas_search_issueby_jql_fields_versions_item
                )

        votes: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.votes, Unset):
            votes = self.votes.to_dict()

        watches: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.watches, Unset):
            watches = self.watches.to_dict()

        workratio = self.workratio

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if aggregateprogress is not UNSET:
            field_dict["aggregateprogress"] = aggregateprogress
        if assignee is not UNSET:
            field_dict["assignee"] = assignee
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_fields_versions_array_item_ref import (
            SearchIssuebyJQLFieldsVersionsArrayItemRef,
        )
        from ..models.search_issueby_jql_fields_project import (
            SearchIssuebyJQLFieldsProject,
        )
        from ..models.search_issueby_jql_fields_watches import (
            SearchIssuebyJQLFieldsWatches,
        )
        from ..models.search_issueby_jql_fields_priority import (
            SearchIssuebyJQLFieldsPriority,
        )
        from ..models.search_issueby_jql_fields_security import (
            SearchIssuebyJQLFieldsSecurity,
        )
        from ..models.search_issueby_jql_fields_fix_versions_array_item_ref import (
            SearchIssuebyJQLFieldsFixVersionsArrayItemRef,
        )
        from ..models.search_issueby_jql_fields_progress import (
            SearchIssuebyJQLFieldsProgress,
        )
        from ..models.search_issueby_jql_fields_reporter import (
            SearchIssuebyJQLFieldsReporter,
        )
        from ..models.search_issueby_jql_fields_timetracking import (
            SearchIssuebyJQLFieldsTimetracking,
        )
        from ..models.search_issueby_jql_fields_votes import SearchIssuebyJQLFieldsVotes
        from ..models.search_issueby_jql_fields_status import (
            SearchIssuebyJQLFieldsStatus,
        )
        from ..models.search_issueby_jql_fields_creator import (
            SearchIssuebyJQLFieldsCreator,
        )
        from ..models.search_issueby_jql_fields_aggregateprogress import (
            SearchIssuebyJQLFieldsAggregateprogress,
        )
        from ..models.search_issueby_jql_fields_assignee import (
            SearchIssuebyJQLFieldsAssignee,
        )
        from ..models.search_issueby_jql_fields_issuetype import (
            SearchIssuebyJQLFieldsIssuetype,
        )
        from ..models.search_issueby_jql_fields_components_array_item_ref import (
            SearchIssuebyJQLFieldsComponentsArrayItemRef,
        )

        d = src_dict.copy()
        _aggregateprogress = d.pop("aggregateprogress", UNSET)
        aggregateprogress: Union[Unset, SearchIssuebyJQLFieldsAggregateprogress]
        if isinstance(_aggregateprogress, Unset):
            aggregateprogress = UNSET
        else:
            aggregateprogress = SearchIssuebyJQLFieldsAggregateprogress.from_dict(
                _aggregateprogress
            )

        _assignee = d.pop("assignee", UNSET)
        assignee: Union[Unset, SearchIssuebyJQLFieldsAssignee]
        if isinstance(_assignee, Unset):
            assignee = UNSET
        else:
            assignee = SearchIssuebyJQLFieldsAssignee.from_dict(_assignee)

        components = []
        _components = d.pop("components", UNSET)
        for componentsschemas_search_issueby_jql_fields_components_item_data in (
            _components or []
        ):
            componentsschemas_search_issueby_jql_fields_components_item = (
                SearchIssuebyJQLFieldsComponentsArrayItemRef.from_dict(
                    componentsschemas_search_issueby_jql_fields_components_item_data
                )
            )

            components.append(
                componentsschemas_search_issueby_jql_fields_components_item
            )

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _creator = d.pop("creator", UNSET)
        creator: Union[Unset, SearchIssuebyJQLFieldsCreator]
        if isinstance(_creator, Unset):
            creator = UNSET
        else:
            creator = SearchIssuebyJQLFieldsCreator.from_dict(_creator)

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
        for componentsschemas_search_issueby_jql_fields_fix_versions_item_data in (
            _fix_versions or []
        ):
            componentsschemas_search_issueby_jql_fields_fix_versions_item = (
                SearchIssuebyJQLFieldsFixVersionsArrayItemRef.from_dict(
                    componentsschemas_search_issueby_jql_fields_fix_versions_item_data
                )
            )

            fix_versions.append(
                componentsschemas_search_issueby_jql_fields_fix_versions_item
            )

        _issuetype = d.pop("issuetype", UNSET)
        issuetype: Union[Unset, SearchIssuebyJQLFieldsIssuetype]
        if isinstance(_issuetype, Unset):
            issuetype = UNSET
        else:
            issuetype = SearchIssuebyJQLFieldsIssuetype.from_dict(_issuetype)

        labels = cast(list[str], d.pop("labels", UNSET))

        _priority = d.pop("priority", UNSET)
        priority: Union[Unset, SearchIssuebyJQLFieldsPriority]
        if isinstance(_priority, Unset):
            priority = UNSET
        else:
            priority = SearchIssuebyJQLFieldsPriority.from_dict(_priority)

        _progress = d.pop("progress", UNSET)
        progress: Union[Unset, SearchIssuebyJQLFieldsProgress]
        if isinstance(_progress, Unset):
            progress = UNSET
        else:
            progress = SearchIssuebyJQLFieldsProgress.from_dict(_progress)

        _project = d.pop("project", UNSET)
        project: Union[Unset, SearchIssuebyJQLFieldsProject]
        if isinstance(_project, Unset):
            project = UNSET
        else:
            project = SearchIssuebyJQLFieldsProject.from_dict(_project)

        _reporter = d.pop("reporter", UNSET)
        reporter: Union[Unset, SearchIssuebyJQLFieldsReporter]
        if isinstance(_reporter, Unset):
            reporter = UNSET
        else:
            reporter = SearchIssuebyJQLFieldsReporter.from_dict(_reporter)

        _security = d.pop("security", UNSET)
        security: Union[Unset, SearchIssuebyJQLFieldsSecurity]
        if isinstance(_security, Unset):
            security = UNSET
        else:
            security = SearchIssuebyJQLFieldsSecurity.from_dict(_security)

        _status = d.pop("status", UNSET)
        status: Union[Unset, SearchIssuebyJQLFieldsStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = SearchIssuebyJQLFieldsStatus.from_dict(_status)

        _statuscategorychangedate = d.pop("statuscategorychangedate", UNSET)
        statuscategorychangedate: Union[Unset, datetime.datetime]
        if isinstance(_statuscategorychangedate, Unset):
            statuscategorychangedate = UNSET
        else:
            statuscategorychangedate = isoparse(_statuscategorychangedate)

        summary = d.pop("summary", UNSET)

        _timetracking = d.pop("timetracking", UNSET)
        timetracking: Union[Unset, SearchIssuebyJQLFieldsTimetracking]
        if isinstance(_timetracking, Unset):
            timetracking = UNSET
        else:
            timetracking = SearchIssuebyJQLFieldsTimetracking.from_dict(_timetracking)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        versions = []
        _versions = d.pop("versions", UNSET)
        for componentsschemas_search_issueby_jql_fields_versions_item_data in (
            _versions or []
        ):
            componentsschemas_search_issueby_jql_fields_versions_item = (
                SearchIssuebyJQLFieldsVersionsArrayItemRef.from_dict(
                    componentsschemas_search_issueby_jql_fields_versions_item_data
                )
            )

            versions.append(componentsschemas_search_issueby_jql_fields_versions_item)

        _votes = d.pop("votes", UNSET)
        votes: Union[Unset, SearchIssuebyJQLFieldsVotes]
        if isinstance(_votes, Unset):
            votes = UNSET
        else:
            votes = SearchIssuebyJQLFieldsVotes.from_dict(_votes)

        _watches = d.pop("watches", UNSET)
        watches: Union[Unset, SearchIssuebyJQLFieldsWatches]
        if isinstance(_watches, Unset):
            watches = UNSET
        else:
            watches = SearchIssuebyJQLFieldsWatches.from_dict(_watches)

        workratio = d.pop("workratio", UNSET)

        search_issueby_jql_fields = cls(
            aggregateprogress=aggregateprogress,
            assignee=assignee,
            components=components,
            created=created,
            creator=creator,
            description=description,
            duedate=duedate,
            environment=environment,
            fix_versions=fix_versions,
            issuetype=issuetype,
            labels=labels,
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
        )

        search_issueby_jql_fields.additional_properties = d
        return search_issueby_jql_fields

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
