from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_fields_issuelinks_inward_issue_fields import (
    GetIssueResponseFieldsIssuelinksInwardIssueFields,
)


class GetIssueResponseFieldsIssuelinksInwardIssue(BaseModel):
    """
    Attributes:
        id (Optional[str]): The unique ID for the inwardly linked issue Example: 10004.
        key (Optional[str]): The key identifier for the inwardly linked issue Example: PR-3.
        fields (Optional[GetIssueResponseFieldsIssuelinksInwardIssueFields]):
        self_ (Optional[str]): API endpoint URL for the linked inward issue Example: https://your-
            domain.atlassian.net/rest/api/3/issue/PR-3.
    """

    model_config = ConfigDict(extra="allow")

    id: Optional[str] = None
    key: Optional[str] = None
    fields: Optional["GetIssueResponseFieldsIssuelinksInwardIssueFields"] = None
    self_: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseFieldsIssuelinksInwardIssue"],
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
