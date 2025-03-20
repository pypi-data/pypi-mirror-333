from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_transitions_fields_schema import (
    GetIssueResponseTransitionsFieldsSchema,
)


class GetIssueResponseTransitionsFields(BaseModel):
    """
    Attributes:
        allowed_values (Optional[list[str]]):
        auto_complete_url (Optional[str]): The URL that can be used to automatically complete the field
        default_value (Optional[str]): The default value of the field
        has_default_value (Optional[bool]): Whether the field has a default value
        key (Optional[str]): The key of the field
        name (Optional[str]): The name of the field
        operations (Optional[list[str]]):
        required (Optional[bool]): Whether the field is required
        schema (Optional[GetIssueResponseTransitionsFieldsSchema]):
    """

    model_config = ConfigDict(extra="allow")

    allowed_values: Optional[list[str]] = None
    auto_complete_url: Optional[str] = None
    default_value: Optional[str] = None
    has_default_value: Optional[bool] = None
    key: Optional[str] = None
    name: Optional[str] = None
    operations: Optional[list[str]] = None
    required: Optional[bool] = None
    schema: Optional["GetIssueResponseTransitionsFieldsSchema"] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseTransitionsFields"], src_dict: Dict[str, Any]
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
