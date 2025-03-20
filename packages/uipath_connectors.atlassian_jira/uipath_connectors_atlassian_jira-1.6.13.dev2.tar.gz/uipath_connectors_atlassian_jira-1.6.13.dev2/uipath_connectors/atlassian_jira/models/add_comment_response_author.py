from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class AddCommentResponseAuthor(BaseModel):
    """
    Attributes:
        self_ (Optional[str]): The Author self Example: https://your-
            domain.atlassian.net/rest/api/3/user?accountId=5b10a2844c20165700ede21g.
        active (Optional[bool]): The Author active
        account_id (Optional[str]): The Author account ID Example: 5b10a2844c20165700ede21g.
        display_name (Optional[str]): The Author display name Example: Mia Krystof.
    """

    model_config = ConfigDict(extra="allow")

    self_: Optional[str] = None
    active: Optional[bool] = None
    account_id: Optional[str] = None
    display_name: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["AddCommentResponseAuthor"], src_dict: Dict[str, Any]):
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
