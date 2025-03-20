from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="SearchIssuebyJQLFieldsVotes")


@_attrs_define
class SearchIssuebyJQLFieldsVotes:
    """
    Attributes:
        has_voted (Union[Unset, bool]):
        self_ (Union[Unset, str]):
        votes (Union[Unset, int]):
    """

    has_voted: Union[Unset, bool] = UNSET
    self_: Union[Unset, str] = UNSET
    votes: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        has_voted = self.has_voted

        self_ = self.self_

        votes = self.votes

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if has_voted is not UNSET:
            field_dict["hasVoted"] = has_voted
        if self_ is not UNSET:
            field_dict["self"] = self_
        if votes is not UNSET:
            field_dict["votes"] = votes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        has_voted = d.pop("hasVoted", UNSET)

        self_ = d.pop("self", UNSET)

        votes = d.pop("votes", UNSET)

        search_issueby_jql_fields_votes = cls(
            has_voted=has_voted,
            self_=self_,
            votes=votes,
        )

        search_issueby_jql_fields_votes.additional_properties = d
        return search_issueby_jql_fields_votes

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
