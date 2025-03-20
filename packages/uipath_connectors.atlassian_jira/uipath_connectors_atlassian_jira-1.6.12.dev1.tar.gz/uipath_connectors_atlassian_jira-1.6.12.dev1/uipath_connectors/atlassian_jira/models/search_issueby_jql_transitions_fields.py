from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_transitions_fields_schema import (
        SearchIssuebyJQLTransitionsFieldsSchema,
    )


T = TypeVar("T", bound="SearchIssuebyJQLTransitionsFields")


@_attrs_define
class SearchIssuebyJQLTransitionsFields:
    """
    Attributes:
        allowed_values (Union[Unset, list[str]]):
        auto_complete_url (Union[Unset, str]): The URL that can be used to automatically complete the field.
        default_value (Union[Unset, str]): The default value of the field.
        has_default_value (Union[Unset, bool]): Whether the field has a default value.
        key (Union[Unset, str]): The key of the field.
        name (Union[Unset, str]): The name of the field.
        operations (Union[Unset, list[str]]):
        required (Union[Unset, bool]): Whether the field is required.
        schema (Union[Unset, SearchIssuebyJQLTransitionsFieldsSchema]):
    """

    allowed_values: Union[Unset, list[str]] = UNSET
    auto_complete_url: Union[Unset, str] = UNSET
    default_value: Union[Unset, str] = UNSET
    has_default_value: Union[Unset, bool] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    operations: Union[Unset, list[str]] = UNSET
    required: Union[Unset, bool] = UNSET
    schema: Union[Unset, "SearchIssuebyJQLTransitionsFieldsSchema"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        allowed_values: Union[Unset, list[str]] = UNSET
        if not isinstance(self.allowed_values, Unset):
            allowed_values = self.allowed_values

        auto_complete_url = self.auto_complete_url

        default_value = self.default_value

        has_default_value = self.has_default_value

        key = self.key

        name = self.name

        operations: Union[Unset, list[str]] = UNSET
        if not isinstance(self.operations, Unset):
            operations = self.operations

        required = self.required

        schema: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if allowed_values is not UNSET:
            field_dict["allowedValues"] = allowed_values
        if auto_complete_url is not UNSET:
            field_dict["autoCompleteUrl"] = auto_complete_url
        if default_value is not UNSET:
            field_dict["defaultValue"] = default_value
        if has_default_value is not UNSET:
            field_dict["hasDefaultValue"] = has_default_value
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if operations is not UNSET:
            field_dict["operations"] = operations
        if required is not UNSET:
            field_dict["required"] = required
        if schema is not UNSET:
            field_dict["schema"] = schema

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_transitions_fields_schema import (
            SearchIssuebyJQLTransitionsFieldsSchema,
        )

        d = src_dict.copy()
        allowed_values = cast(list[str], d.pop("allowedValues", UNSET))

        auto_complete_url = d.pop("autoCompleteUrl", UNSET)

        default_value = d.pop("defaultValue", UNSET)

        has_default_value = d.pop("hasDefaultValue", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        operations = cast(list[str], d.pop("operations", UNSET))

        required = d.pop("required", UNSET)

        _schema = d.pop("schema", UNSET)
        schema: Union[Unset, SearchIssuebyJQLTransitionsFieldsSchema]
        if isinstance(_schema, Unset):
            schema = UNSET
        else:
            schema = SearchIssuebyJQLTransitionsFieldsSchema.from_dict(_schema)

        search_issueby_jql_transitions_fields = cls(
            allowed_values=allowed_values,
            auto_complete_url=auto_complete_url,
            default_value=default_value,
            has_default_value=has_default_value,
            key=key,
            name=name,
            operations=operations,
            required=required,
            schema=schema,
        )

        search_issueby_jql_transitions_fields.additional_properties = d
        return search_issueby_jql_transitions_fields

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
