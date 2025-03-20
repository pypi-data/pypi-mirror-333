from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_transition_to import GetIssueResponseTransitionTo
    from ..models.get_issue_response_transition_error_collection import (
        GetIssueResponseTransitionErrorCollection,
    )
    from ..models.get_issue_response_transition_fields import (
        GetIssueResponseTransitionFields,
    )


T = TypeVar("T", bound="GetIssueResponseTransition")


@_attrs_define
class GetIssueResponseTransition:
    """
    Attributes:
        error_collection (Union[Unset, GetIssueResponseTransitionErrorCollection]):
        expand (Union[Unset, str]): Expand options that include additional transition details in the response
        fields (Union[Unset, GetIssueResponseTransitionFields]):
        has_screen (Union[Unset, bool]): Whether there is a screen associated with the issue transition
        id (Union[Unset, str]): The ID of the issue transition. Required when specifying a transition to undertake.
        is_available (Union[Unset, bool]): Whether the transition is available to be performed
        is_conditional (Union[Unset, bool]): Whether the issue has to meet criteria before the issue transition is
            applied
        is_global (Union[Unset, bool]): Whether the issue transition is global, that is, the transition is applied to
            issues regardless of their status.
        is_initial (Union[Unset, bool]): Whether this is the initial issue transition for the workflow
        looped (Union[Unset, bool]):
        name (Union[Unset, str]): The name of the issue transition
        status (Union[Unset, int]):
        to (Union[Unset, GetIssueResponseTransitionTo]):
    """

    error_collection: Union[Unset, "GetIssueResponseTransitionErrorCollection"] = UNSET
    expand: Union[Unset, str] = UNSET
    fields: Union[Unset, "GetIssueResponseTransitionFields"] = UNSET
    has_screen: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    is_available: Union[Unset, bool] = UNSET
    is_conditional: Union[Unset, bool] = UNSET
    is_global: Union[Unset, bool] = UNSET
    is_initial: Union[Unset, bool] = UNSET
    looped: Union[Unset, bool] = UNSET
    name: Union[Unset, str] = UNSET
    status: Union[Unset, int] = UNSET
    to: Union[Unset, "GetIssueResponseTransitionTo"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        error_collection: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.error_collection, Unset):
            error_collection = self.error_collection.to_dict()

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

        status = self.status

        to: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.to, Unset):
            to = self.to.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_collection is not UNSET:
            field_dict["errorCollection"] = error_collection
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
        if status is not UNSET:
            field_dict["status"] = status
        if to is not UNSET:
            field_dict["to"] = to

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_transition_to import (
            GetIssueResponseTransitionTo,
        )
        from ..models.get_issue_response_transition_error_collection import (
            GetIssueResponseTransitionErrorCollection,
        )
        from ..models.get_issue_response_transition_fields import (
            GetIssueResponseTransitionFields,
        )

        d = src_dict.copy()
        _error_collection = d.pop("errorCollection", UNSET)
        error_collection: Union[Unset, GetIssueResponseTransitionErrorCollection]
        if isinstance(_error_collection, Unset):
            error_collection = UNSET
        else:
            error_collection = GetIssueResponseTransitionErrorCollection.from_dict(
                _error_collection
            )

        expand = d.pop("expand", UNSET)

        _fields = d.pop("fields", UNSET)
        fields: Union[Unset, GetIssueResponseTransitionFields]
        if isinstance(_fields, Unset):
            fields = UNSET
        else:
            fields = GetIssueResponseTransitionFields.from_dict(_fields)

        has_screen = d.pop("hasScreen", UNSET)

        id = d.pop("id", UNSET)

        is_available = d.pop("isAvailable", UNSET)

        is_conditional = d.pop("isConditional", UNSET)

        is_global = d.pop("isGlobal", UNSET)

        is_initial = d.pop("isInitial", UNSET)

        looped = d.pop("looped", UNSET)

        name = d.pop("name", UNSET)

        status = d.pop("status", UNSET)

        _to = d.pop("to", UNSET)
        to: Union[Unset, GetIssueResponseTransitionTo]
        if isinstance(_to, Unset):
            to = UNSET
        else:
            to = GetIssueResponseTransitionTo.from_dict(_to)

        get_issue_response_transition = cls(
            error_collection=error_collection,
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
            status=status,
            to=to,
        )

        get_issue_response_transition.additional_properties = d
        return get_issue_response_transition

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
