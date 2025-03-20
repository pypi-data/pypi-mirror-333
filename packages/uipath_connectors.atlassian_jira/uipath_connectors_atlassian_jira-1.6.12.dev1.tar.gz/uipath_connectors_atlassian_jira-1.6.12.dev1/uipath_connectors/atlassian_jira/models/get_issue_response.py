from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_fields_to_include import (
        GetIssueResponseFieldsToInclude,
    )
    from ..models.get_issue_response_update import GetIssueResponseUpdate
    from ..models.get_issue_response_history_metadata import (
        GetIssueResponseHistoryMetadata,
    )
    from ..models.get_issue_response_changelog import GetIssueResponseChangelog
    from ..models.get_issue_response_operations import GetIssueResponseOperations
    from ..models.get_issue_response_properties_array_item_ref import (
        GetIssueResponsePropertiesArrayItemRef,
    )
    from ..models.get_issue_response_transitions_array_item_ref import (
        GetIssueResponseTransitionsArrayItemRef,
    )
    from ..models.get_issue_response_transition import GetIssueResponseTransition
    from ..models.get_issue_response_fields import GetIssueResponseFields
    from ..models.get_issue_response_editmeta import GetIssueResponseEditmeta
    from ..models.get_issue_response_schema import GetIssueResponseSchema


T = TypeVar("T", bound="GetIssueResponse")


@_attrs_define
class GetIssueResponse:
    """
    Attributes:
        changelog (Union[Unset, GetIssueResponseChangelog]):
        editmeta (Union[Unset, GetIssueResponseEditmeta]):
        expand (Union[Unset, str]): Expand options that include additional issue details in the response
        fields_to_include (Union[Unset, GetIssueResponseFieldsToInclude]):
        update (Union[Unset, GetIssueResponseUpdate]):
        fields (Union[Unset, GetIssueResponseFields]):
        history_metadata (Union[Unset, GetIssueResponseHistoryMetadata]):
        id (Union[Unset, str]): The ID of the issue
        key (Union[Unset, str]): The key of the issue
        operations (Union[Unset, GetIssueResponseOperations]):
        properties (Union[Unset, list['GetIssueResponsePropertiesArrayItemRef']]):
        schema (Union[Unset, GetIssueResponseSchema]):
        self_ (Union[Unset, str]): The URL of the issue details
        transition (Union[Unset, GetIssueResponseTransition]):
        transitions (Union[Unset, list['GetIssueResponseTransitionsArrayItemRef']]):
    """

    changelog: Union[Unset, "GetIssueResponseChangelog"] = UNSET
    editmeta: Union[Unset, "GetIssueResponseEditmeta"] = UNSET
    expand: Union[Unset, str] = UNSET
    fields_to_include: Union[Unset, "GetIssueResponseFieldsToInclude"] = UNSET
    update: Union[Unset, "GetIssueResponseUpdate"] = UNSET
    fields: Union[Unset, "GetIssueResponseFields"] = UNSET
    history_metadata: Union[Unset, "GetIssueResponseHistoryMetadata"] = UNSET
    id: Union[Unset, str] = UNSET
    key: Union[Unset, str] = UNSET
    operations: Union[Unset, "GetIssueResponseOperations"] = UNSET
    properties: Union[Unset, list["GetIssueResponsePropertiesArrayItemRef"]] = UNSET
    schema: Union[Unset, "GetIssueResponseSchema"] = UNSET
    self_: Union[Unset, str] = UNSET
    transition: Union[Unset, "GetIssueResponseTransition"] = UNSET
    transitions: Union[Unset, list["GetIssueResponseTransitionsArrayItemRef"]] = UNSET
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

        update: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.update, Unset):
            update = self.update.to_dict()

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        history_metadata: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.history_metadata, Unset):
            history_metadata = self.history_metadata.to_dict()

        id = self.id

        key = self.key

        operations: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = self.operations.to_dict()

        properties: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for (
                componentsschemas_get_issue_response_properties_item_data
            ) in self.properties:
                componentsschemas_get_issue_response_properties_item = (
                    componentsschemas_get_issue_response_properties_item_data.to_dict()
                )
                properties.append(componentsschemas_get_issue_response_properties_item)

        schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        self_ = self.self_

        transition: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.transition, Unset):
            transition = self.transition.to_dict()

        transitions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.transitions, Unset):
            transitions = []
            for (
                componentsschemas_get_issue_response_transitions_item_data
            ) in self.transitions:
                componentsschemas_get_issue_response_transitions_item = (
                    componentsschemas_get_issue_response_transitions_item_data.to_dict()
                )
                transitions.append(
                    componentsschemas_get_issue_response_transitions_item
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
        if update is not UNSET:
            field_dict["update"] = update
        if fields is not UNSET:
            field_dict["fields"] = fields
        if history_metadata is not UNSET:
            field_dict["historyMetadata"] = history_metadata
        if id is not UNSET:
            field_dict["id"] = id
        if key is not UNSET:
            field_dict["key"] = key
        if operations is not UNSET:
            field_dict["operations"] = operations
        if properties is not UNSET:
            field_dict["properties"] = properties
        if schema is not UNSET:
            field_dict["schema"] = schema
        if self_ is not UNSET:
            field_dict["self"] = self_
        if transition is not UNSET:
            field_dict["transition"] = transition
        if transitions is not UNSET:
            field_dict["transitions"] = transitions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_fields_to_include import (
            GetIssueResponseFieldsToInclude,
        )
        from ..models.get_issue_response_update import GetIssueResponseUpdate
        from ..models.get_issue_response_history_metadata import (
            GetIssueResponseHistoryMetadata,
        )
        from ..models.get_issue_response_changelog import GetIssueResponseChangelog
        from ..models.get_issue_response_operations import GetIssueResponseOperations
        from ..models.get_issue_response_properties_array_item_ref import (
            GetIssueResponsePropertiesArrayItemRef,
        )
        from ..models.get_issue_response_transitions_array_item_ref import (
            GetIssueResponseTransitionsArrayItemRef,
        )
        from ..models.get_issue_response_transition import GetIssueResponseTransition
        from ..models.get_issue_response_fields import GetIssueResponseFields
        from ..models.get_issue_response_editmeta import GetIssueResponseEditmeta
        from ..models.get_issue_response_schema import GetIssueResponseSchema

        d = src_dict.copy()
        _changelog = d.pop("changelog", UNSET)
        changelog: Union[Unset, GetIssueResponseChangelog]
        if isinstance(_changelog, Unset):
            changelog = UNSET
        else:
            changelog = GetIssueResponseChangelog.from_dict(_changelog)

        _editmeta = d.pop("editmeta", UNSET)
        editmeta: Union[Unset, GetIssueResponseEditmeta]
        if isinstance(_editmeta, Unset):
            editmeta = UNSET
        else:
            editmeta = GetIssueResponseEditmeta.from_dict(_editmeta)

        expand = d.pop("expand", UNSET)

        _fields_to_include = d.pop("fieldsToInclude", UNSET)
        fields_to_include: Union[Unset, GetIssueResponseFieldsToInclude]
        if isinstance(_fields_to_include, Unset):
            fields_to_include = UNSET
        else:
            fields_to_include = GetIssueResponseFieldsToInclude.from_dict(
                _fields_to_include
            )

        _update = d.pop("update", UNSET)
        update: Union[Unset, GetIssueResponseUpdate]
        if isinstance(_update, Unset):
            update = UNSET
        else:
            update = GetIssueResponseUpdate.from_dict(_update)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, GetIssueResponseFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = GetIssueResponseFields.from_dict(_fields)

        _history_metadata = d.pop("historyMetadata", UNSET)
        history_metadata: Union[Unset, GetIssueResponseHistoryMetadata]
        if isinstance(_history_metadata, Unset):
            history_metadata = UNSET
        else:
            history_metadata = GetIssueResponseHistoryMetadata.from_dict(
                _history_metadata
            )

        id = d.pop("id", UNSET)

        key = d.pop("key", UNSET)

        _operations = d.pop("operations", UNSET)
        operations: Union[Unset, GetIssueResponseOperations]
        if isinstance(_operations, Unset):
            operations = UNSET
        else:
            operations = GetIssueResponseOperations.from_dict(_operations)

        properties = []
        _properties = d.pop("properties", UNSET)
        for componentsschemas_get_issue_response_properties_item_data in (
            _properties or []
        ):
            componentsschemas_get_issue_response_properties_item = (
                GetIssueResponsePropertiesArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_properties_item_data
                )
            )

            properties.append(componentsschemas_get_issue_response_properties_item)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, GetIssueResponseSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = GetIssueResponseSchema.from_dict(_schema)

        self_ = d.pop("self", UNSET)

        _transition = d.pop("transition", UNSET)
        transition: Union[Unset, GetIssueResponseTransition]
        if isinstance(_transition, Unset):
            transition = UNSET
        else:
            transition = GetIssueResponseTransition.from_dict(_transition)

        transitions = []
        _transitions = d.pop("transitions", UNSET)
        for componentsschemas_get_issue_response_transitions_item_data in (
            _transitions or []
        ):
            componentsschemas_get_issue_response_transitions_item = (
                GetIssueResponseTransitionsArrayItemRef.from_dict(
                    componentsschemas_get_issue_response_transitions_item_data
                )
            )

            transitions.append(componentsschemas_get_issue_response_transitions_item)

        get_issue_response = cls(
            changelog=changelog,
            editmeta=editmeta,
            expand=expand,
            fields_to_include=fields_to_include,
            update=update,
            fields=fields,
            history_metadata=history_metadata,
            id=id,
            key=key,
            operations=operations,
            properties=properties,
            schema=schema,
            self_=self_,
            transition=transition,
            transitions=transitions,
        )

        get_issue_response.additional_properties = d
        return get_issue_response

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
