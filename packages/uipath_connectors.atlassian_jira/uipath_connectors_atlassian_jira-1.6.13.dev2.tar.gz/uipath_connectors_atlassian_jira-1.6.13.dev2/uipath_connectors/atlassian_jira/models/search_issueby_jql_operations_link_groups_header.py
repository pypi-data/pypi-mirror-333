from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class SearchIssuebyJQLOperationsLinkGroupsHeader(BaseModel):
    """
    Attributes:
        href (Optional[str]):
        icon_class (Optional[str]):
        id (Optional[str]):
        label (Optional[str]):
        style_class (Optional[str]):
        title (Optional[str]):
        weight (Optional[int]):
    """

    model_config = ConfigDict(extra="allow")

    href: Optional[str] = None
    icon_class: Optional[str] = None
    id: Optional[str] = None
    label: Optional[str] = None
    style_class: Optional[str] = None
    title: Optional[str] = None
    weight: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SearchIssuebyJQLOperationsLinkGroupsHeader"],
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
