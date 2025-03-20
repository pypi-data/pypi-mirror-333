from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_transitions_array_item_ref import (
        SearchIssuebyJQLTransitionsArrayItemRef,
    )
    from ..models.search_issueby_jql_operations import SearchIssuebyJQLOperations
    from ..models.search_issueby_jql_schema import SearchIssuebyJQLSchema
    from ..models.search_issueby_jql_fields import SearchIssuebyJQLFields
    from ..models.search_issueby_jql_fields_to_include import (
        SearchIssuebyJQLFieldsToInclude,
    )
    from ..models.search_issueby_jql_changelog import SearchIssuebyJQLChangelog
    from ..models.search_issueby_jql_editmeta import SearchIssuebyJQLEditmeta


T = TypeVar("T", bound="SearchIssuebyJQL")


@_attrs_define
class SearchIssuebyJQL:
    """
    Attributes:
        changelog (Union[Unset, SearchIssuebyJQLChangelog]):
        editmeta (Union[Unset, SearchIssuebyJQLEditmeta]):
        expand (Union[Unset, str]): Expand options that include additional issue details in the response.
        fields_to_include (Union[Unset, SearchIssuebyJQLFieldsToInclude]):
        fields (Union[Unset, SearchIssuebyJQLFields]):
        id (Union[Unset, str]): The ID of the issue.
        key (Union[Unset, str]): The key of the issue.
        operations (Union[Unset, SearchIssuebyJQLOperations]):
        schema (Union[Unset, SearchIssuebyJQLSchema]):
        self_ (Union[Unset, str]): The URL of the issue details.
        transitions (Union[Unset, list['SearchIssuebyJQLTransitionsArrayItemRef']]):
    """

    changelog: Union[Unset, "SearchIssuebyJQLChangelog"] = UNSET
    editmeta: Union[Unset, "SearchIssuebyJQLEditmeta"] = UNSET
    expand: Union[Unset, str] = UNSET
    fields_to_include: Union[Unset, "SearchIssuebyJQLFieldsToInclude"] = UNSET
    fields: Union[Unset, "SearchIssuebyJQLFields"] = UNSET
    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    operations: Union[Unset, "SearchIssuebyJQLOperations"] = UNSET
    schema: Union[Unset, "SearchIssuebyJQLSchema"] = UNSET
    self_: Union[Unset, str] = UNSET
    transitions: Union[Unset, list["SearchIssuebyJQLTransitionsArrayItemRef"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        changelog: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.changelog, Unset):
            changelog = self.changelog.to_dict()

        editmeta: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.editmeta, Unset):
            editmeta = self.editmeta.to_dict()

        expand = self.expand

        fields_to_include: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields_to_include, Unset):
            fields_to_include = self.fields_to_include.to_dict()

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        id = self.id

        key = self.key

        operations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = self.operations.to_dict()

        schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        self_ = self.self_

        transitions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.transitions, Unset):
            transitions = []
            for (
                componentsschemas_search_issueby_jql_transitions_item_data
            ) in self.transitions:
                componentsschemas_search_issueby_jql_transitions_item = (
                    componentsschemas_search_issueby_jql_transitions_item_data.to_dict()
                )
                transitions.append(
                    componentsschemas_search_issueby_jql_transitions_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if changelog is not UNSET:
            field_dict["changelog"] = changelog
        if editmeta is not UNSET:
            field_dict["editmeta"] = editmeta
        if expand is not UNSET:
            field_dict["expand"] = expand
        if fields_to_include is not UNSET:
            field_dict["fieldsToInclude"] = fields_to_include
        if fields is not UNSET:
            field_dict["fields"] = fields
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if operations is not UNSET:
            field_dict["operations"] = operations
        if schema is not UNSET:
            field_dict["schema"] = schema
        if self_ is not UNSET:
            field_dict["self"] = self_
        if transitions is not UNSET:
            field_dict["transitions"] = transitions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_transitions_array_item_ref import (
            SearchIssuebyJQLTransitionsArrayItemRef,
        )
        from ..models.search_issueby_jql_operations import SearchIssuebyJQLOperations
        from ..models.search_issueby_jql_schema import SearchIssuebyJQLSchema
        from ..models.search_issueby_jql_fields import SearchIssuebyJQLFields
        from ..models.search_issueby_jql_fields_to_include import (
            SearchIssuebyJQLFieldsToInclude,
        )
        from ..models.search_issueby_jql_changelog import SearchIssuebyJQLChangelog
        from ..models.search_issueby_jql_editmeta import SearchIssuebyJQLEditmeta

        d = src_dict.copy()
        _changelog = d.pop("changelog", UNSET)
        changelog: Union[Unset, SearchIssuebyJQLChangelog]
        if isinstance(_changelog, Unset):
            changelog = UNSET
        else:
            changelog = SearchIssuebyJQLChangelog.from_dict(_changelog)

        _editmeta = d.pop("editmeta", UNSET)
        editmeta: Union[Unset, SearchIssuebyJQLEditmeta]
        if isinstance(_editmeta, Unset):
            editmeta = UNSET
        else:
            editmeta = SearchIssuebyJQLEditmeta.from_dict(_editmeta)

        expand = d.pop("expand", UNSET)

        _fields_to_include = d.pop("fieldsToInclude", UNSET)
        fields_to_include: Union[Unset, SearchIssuebyJQLFieldsToInclude]
        if isinstance(_fields_to_include, Unset):
            fields_to_include = UNSET
        else:
            fields_to_include = SearchIssuebyJQLFieldsToInclude.from_dict(
                _fields_to_include
            )

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, SearchIssuebyJQLFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = SearchIssuebyJQLFields.from_dict(_fields)

        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        _operations = d.pop("operations", UNSET)
        operations: Union[Unset, SearchIssuebyJQLOperations]
        if isinstance(_operations, Unset):
            operations = UNSET
        else:
            operations = SearchIssuebyJQLOperations.from_dict(_operations)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, SearchIssuebyJQLSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = SearchIssuebyJQLSchema.from_dict(_schema)

        self_ = d.pop("self", UNSET)

        transitions = []
        _transitions = d.pop("transitions", UNSET)
        for componentsschemas_search_issueby_jql_transitions_item_data in (
            _transitions or []
        ):
            componentsschemas_search_issueby_jql_transitions_item = (
                SearchIssuebyJQLTransitionsArrayItemRef.from_dict(
                    componentsschemas_search_issueby_jql_transitions_item_data
                )
            )

            transitions.append(componentsschemas_search_issueby_jql_transitions_item)

        search_issueby_jql = cls(
            changelog=changelog,
            editmeta=editmeta,
            expand=expand,
            fields_to_include=fields_to_include,
            fields=fields,
            id=id,
            key=key,
            operations=operations,
            schema=schema,
            self_=self_,
            transitions=transitions,
        )

        search_issueby_jql.additional_properties = d
        return search_issueby_jql

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
