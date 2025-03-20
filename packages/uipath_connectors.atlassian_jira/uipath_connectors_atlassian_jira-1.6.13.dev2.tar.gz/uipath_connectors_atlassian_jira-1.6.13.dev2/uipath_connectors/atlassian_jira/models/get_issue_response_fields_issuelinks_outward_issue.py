from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_fields_issuelinks_outward_issue_fields import (
    GetIssueResponseFieldsIssuelinksOutwardIssueFields,
)


class GetIssueResponseFieldsIssuelinksOutwardIssue(BaseModel):
    """
    Attributes:
        key (Optional[str]): The key identifier for the outwardly linked issue Example: PR-2.
        fields (Optional[GetIssueResponseFieldsIssuelinksOutwardIssueFields]):
        self_ (Optional[str]): API endpoint URL for the linked outward issue Example: https://your-
            domain.atlassian.net/rest/api/3/issue/PR-2.
        id (Optional[str]): The unique identifier for the linked outward issue Example: 10004L.
    """

    model_config = ConfigDict(extra="allow")

    key: Optional[str] = None
    fields: Optional["GetIssueResponseFieldsIssuelinksOutwardIssueFields"] = None
    self_: Optional[str] = None
    id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseFieldsIssuelinksOutwardIssue"],
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
