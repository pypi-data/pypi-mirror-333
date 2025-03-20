from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef(BaseModel):
    """
    Attributes:
        field (Optional[str]): The name of the field changed.
        field_id (Optional[str]): The ID of the field changed.
        fieldtype (Optional[str]): The type of the field changed.
        from_ (Optional[str]): The details of the original value.
        from_string (Optional[str]): The details of the original value as a string.
        to (Optional[str]): The details of the new value.
        to_string (Optional[str]): The details of the new value as a string.
    """

    model_config = ConfigDict(extra="allow")

    field: Optional[str] = None
    field_id: Optional[str] = None
    fieldtype: Optional[str] = None
    from_: Optional[str] = None
    from_string: Optional[str] = None
    to: Optional[str] = None
    to_string: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SearchIssuebyJQLChangelogHistoriesItemsArrayItemRef"],
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
