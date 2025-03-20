from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class SearchIssuebyJQLFieldsIssuetype(BaseModel):
    """
    Attributes:
        avatar_id (Optional[int]):
        description (Optional[str]):
        entity_id (Optional[str]):
        hierarchy_level (Optional[int]):
        icon_url (Optional[str]):
        id (Optional[str]): The type of the issue (task, story, bug, epic, etc). Select one to enable custom fields.
        name (Optional[str]):
        self_ (Optional[str]):
        subtask (Optional[bool]):
    """

    model_config = ConfigDict(extra="allow")

    avatar_id: Optional[int] = None
    description: Optional[str] = None
    entity_id: Optional[str] = None
    hierarchy_level: Optional[int] = None
    icon_url: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    self_: Optional[str] = None
    subtask: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SearchIssuebyJQLFieldsIssuetype"], src_dict: Dict[str, Any]
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
