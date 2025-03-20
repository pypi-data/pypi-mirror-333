from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.search_issueby_jql_transitions_to import SearchIssuebyJQLTransitionsTo
    from ..models.search_issueby_jql_transitions_fields import (
        SearchIssuebyJQLTransitionsFields,
    )


T = TypeVar("T", bound="SearchIssuebyJQLTransitionsArrayItemRef")


@_attrs_define
class SearchIssuebyJQLTransitionsArrayItemRef:
    """
    Attributes:
        expand (Union[Unset, str]): Expand options that include additional transition details in the response.
        fields (Union[Unset, SearchIssuebyJQLTransitionsFields]):
        has_screen (Union[Unset, bool]): Whether there is a screen associated with the issue transition.
        id (Union[Unset, str]): The ID of the issue transition. Required when specifying a transition to undertake.
        is_available (Union[Unset, bool]): Whether the transition is available to be performed.
        is_conditional (Union[Unset, bool]): Whether the issue has to meet criteria before the issue transition is
            applied.
        is_global (Union[Unset, bool]): Whether the issue transition is global, that is, the transition is applied to
            issues regardless of their status.
        is_initial (Union[Unset, bool]): Whether this is the initial issue transition for the workflow.
        looped (Union[Unset, bool]):
        name (Union[Unset, str]): The name of the issue transition.
        to (Union[Unset, SearchIssuebyJQLTransitionsTo]):
    """

    expand: Union[Unset, str] = UNSET
    fields: Union[Unset, "SearchIssuebyJQLTransitionsFields"] = UNSET
    has_screen: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    is_available: Union[Unset, bool] = UNSET
    is_conditional: Union[Unset, bool] = UNSET
    is_global: Union[Unset, bool] = UNSET
    is_initial: Union[Unset, bool] = UNSET
    looped: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    to: Union[Unset, "SearchIssuebyJQLTransitionsTo"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        expand = self.expand

        fields: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        has_screen = self.has_screen

        id = self.id

        is_available = self.is_available

        is_conditional = self.is_conditional

        is_global = self.is_global

        is_initial = self.is_initial

        looped = self.looped

        name = self.name

        to: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.to, Unset):
            to = self.to.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if expand is not UNSET:
            field_dict["expand"] = expand
        if fields is not UNSET:
            field_dict["fields"] = fields
        if has_screen is not UNSET:
            field_dict["hasScreen"] = has_screen
        if id is not UNSET:
            field_dict["id"] = id
        if is_available is not UNSET:
            field_dict["isAvailable"] = is_available
        if is_conditional is not UNSET:
            field_dict["isConditional"] = is_conditional
        if is_global is not UNSET:
            field_dict["isGlobal"] = is_global
        if is_initial is not UNSET:
            field_dict["isInitial"] = is_initial
        if looped is not UNSET:
            field_dict["looped"] = looped
        if name is not UNSET:
            field_dict["name"] = name
        if to is not UNSET:
            field_dict["to"] = to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.search_issueby_jql_transitions_to import (
            SearchIssuebyJQLTransitionsTo,
        )
        from ..models.search_issueby_jql_transitions_fields import (
            SearchIssuebyJQLTransitionsFields,
        )

        d = src_dict.copy()
        expand = d.pop("expand", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, SearchIssuebyJQLTransitionsFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = SearchIssuebyJQLTransitionsFields.from_dict(_fields)

        has_screen = d.pop("hasScreen", UNSET)

        id = d.pop("id", UNSET)

        is_available = d.pop("isAvailable", UNSET)

        is_conditional = d.pop("isConditional", UNSET)

        is_global = d.pop("isGlobal", UNSET)

        is_initial = d.pop("isInitial", UNSET)

        looped = d.pop("looped", UNSET)

        name = d.pop("name", UNSET)

        _to = d.pop("to", UNSET)
        to: Union[Unset, SearchIssuebyJQLTransitionsTo]
        if isinstance(_to, Unset):
            to = UNSET
        else:
            to = SearchIssuebyJQLTransitionsTo.from_dict(_to)

        search_issueby_jql_transitions_array_item_ref = cls(
            expand=expand,
            fields=fields,
            has_screen=has_screen,
            id=id,
            is_available=is_available,
            is_conditional=is_conditional,
            is_global=is_global,
            is_initial=is_initial,
            looped=looped,
            name=name,
            to=to,
        )

        search_issueby_jql_transitions_array_item_ref.additional_properties = d
        return search_issueby_jql_transitions_array_item_ref

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
