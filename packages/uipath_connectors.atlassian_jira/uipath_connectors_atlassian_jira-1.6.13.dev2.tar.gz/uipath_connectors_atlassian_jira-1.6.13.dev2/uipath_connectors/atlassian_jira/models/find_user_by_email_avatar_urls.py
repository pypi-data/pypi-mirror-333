from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class FindUserByEmailAvatarUrls(BaseModel):
    """
    Attributes:
        field_16x16 (Optional[str]): The URL of the item's 16x16 pixel avatar.
        field_24x24 (Optional[str]): The URL of the item's 24x24 pixel avatar.
        field_32x32 (Optional[str]): The URL of the item's 32x32 pixel avatar.
        field_48x48 (Optional[str]): The URL of the item's 48x48 pixel avatar.
    """

    model_config = ConfigDict(extra="allow")

    field_16x16: Optional[str] = None
    field_24x24: Optional[str] = None
    field_32x32: Optional[str] = None
    field_48x48: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["FindUserByEmailAvatarUrls"], src_dict: Dict[str, Any]):
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
