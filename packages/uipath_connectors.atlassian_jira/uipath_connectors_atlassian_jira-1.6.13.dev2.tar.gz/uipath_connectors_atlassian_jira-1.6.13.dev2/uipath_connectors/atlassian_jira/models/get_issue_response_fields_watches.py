from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class GetIssueResponseFieldsWatches(BaseModel):
    """
    Attributes:
        is_watching (Optional[bool]):
        self_ (Optional[str]):
        watch_count (Optional[int]):
    """

    model_config = ConfigDict(extra="allow")

    is_watching: Optional[bool] = None
    self_: Optional[str] = None
    watch_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetIssueResponseFieldsWatches"], src_dict: Dict[str, Any]):
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
