from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.search_issueby_jql_transitions_fields import (
    SearchIssuebyJQLTransitionsFields,
)
from ..models.search_issueby_jql_transitions_to import SearchIssuebyJQLTransitionsTo


class SearchIssuebyJQLTransitionsArrayItemRef(BaseModel):
    """
    Attributes:
        expand (Optional[str]): Expand options that include additional transition details in the response.
        fields (Optional[SearchIssuebyJQLTransitionsFields]):
        has_screen (Optional[bool]): Whether there is a screen associated with the issue transition.
        id (Optional[str]): The ID of the issue transition. Required when specifying a transition to undertake.
        is_available (Optional[bool]): Whether the transition is available to be performed.
        is_conditional (Optional[bool]): Whether the issue has to meet criteria before the issue transition is applied.
        is_global (Optional[bool]): Whether the issue transition is global, that is, the transition is applied to issues
            regardless of their status.
        is_initial (Optional[bool]): Whether this is the initial issue transition for the workflow.
        looped (Optional[bool]):
        name (Optional[str]): The name of the issue transition.
        to (Optional[SearchIssuebyJQLTransitionsTo]):
    """

    model_config = ConfigDict(extra="allow")

    expand: Optional[str] = None
    fields: Optional["SearchIssuebyJQLTransitionsFields"] = None
    has_screen: Optional[bool] = None
    id: Optional[str] = None
    is_available: Optional[bool] = None
    is_conditional: Optional[bool] = None
    is_global: Optional[bool] = None
    is_initial: Optional[bool] = None
    looped: Optional[bool] = None
    name: Optional[str] = None
    to: Optional["SearchIssuebyJQLTransitionsTo"] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SearchIssuebyJQLTransitionsArrayItemRef"], src_dict: Dict[str, Any]
    ):
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
