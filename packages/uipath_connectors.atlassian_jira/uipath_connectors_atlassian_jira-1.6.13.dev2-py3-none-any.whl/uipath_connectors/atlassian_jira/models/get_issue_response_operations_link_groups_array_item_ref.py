from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_operations_link_groups_header import (
    GetIssueResponseOperationsLinkGroupsHeader,
)
from ..models.get_issue_response_operations_link_groups_groups_array_item_ref import (
    GetIssueResponseOperationsLinkGroupsGroupsArrayItemRef,
)
from ..models.get_issue_response_operations_link_groups_links_array_item_ref import (
    GetIssueResponseOperationsLinkGroupsLinksArrayItemRef,
)


class GetIssueResponseOperationsLinkGroupsArrayItemRef(BaseModel):
    """
    Attributes:
        groups (Optional[list['GetIssueResponseOperationsLinkGroupsGroupsArrayItemRef']]):
        header (Optional[GetIssueResponseOperationsLinkGroupsHeader]):
        id (Optional[str]):
        links (Optional[list['GetIssueResponseOperationsLinkGroupsLinksArrayItemRef']]):
        style_class (Optional[str]):
        weight (Optional[int]):
    """

    model_config = ConfigDict(extra="allow")

    groups: Optional[list["GetIssueResponseOperationsLinkGroupsGroupsArrayItemRef"]] = (
        None
    )
    header: Optional["GetIssueResponseOperationsLinkGroupsHeader"] = None
    id: Optional[str] = None
    links: Optional[list["GetIssueResponseOperationsLinkGroupsLinksArrayItemRef"]] = (
        None
    )
    style_class: Optional[str] = None
    weight: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseOperationsLinkGroupsArrayItemRef"],
        src_dict: Dict[str, Any],
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
