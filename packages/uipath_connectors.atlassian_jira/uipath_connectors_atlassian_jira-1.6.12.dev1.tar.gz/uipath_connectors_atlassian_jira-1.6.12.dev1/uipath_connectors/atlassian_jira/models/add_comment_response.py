from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.add_comment_response_visibility import AddCommentResponseVisibility
    from ..models.add_comment_response_author import AddCommentResponseAuthor
    from ..models.add_comment_response_update_author import (
        AddCommentResponseUpdateAuthor,
    )


T = TypeVar("T", bound="AddCommentResponse")


@_attrs_define
class AddCommentResponse:
    """
    Attributes:
        body (Union[Unset, str]): Provide input for the comment using text
        author (Union[Unset, AddCommentResponseAuthor]):
        created (Union[Unset, datetime.datetime]): The Created Example: 2021-01-17T12:34:00.0000000+00:00.
        update_author (Union[Unset, AddCommentResponseUpdateAuthor]):
        visibility (Union[Unset, AddCommentResponseVisibility]):
        self_ (Union[Unset, str]): The Self Example: https://your-
            domain.atlassian.net/rest/api/3/issue/10010/comment/10000.
        id (Union[Unset, str]): The ID of the new comment Example: 10000.
        updated (Union[Unset, datetime.datetime]): The Updated Example: 2021-01-18T23:45:00.0000000+00:00.
    """

    body: Union[Unset, str] = UNSET
    author: Union[Unset, "AddCommentResponseAuthor"] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    update_author: Union[Unset, "AddCommentResponseUpdateAuthor"] = UNSET
    visibility: Union[Unset, "AddCommentResponseVisibility"] = UNSET
    self_: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        body = self.body

        author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        update_author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.update_author, Unset):
            update_author = self.update_author.to_dict()

        visibility: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.to_dict()

        self_ = self.self_

        id = self.id

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if author is not UNSET:
            field_dict["author"] = author
        if created is not UNSET:
            field_dict["created"] = created
        if update_author is not UNSET:
            field_dict["updateAuthor"] = update_author
        if visibility is not UNSET:
            field_dict["visibility"] = visibility
        if self_ is not UNSET:
            field_dict["self"] = self_
        if id is not UNSET:
            field_dict["id"] = id
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.add_comment_response_visibility import (
            AddCommentResponseVisibility,
        )
        from ..models.add_comment_response_author import AddCommentResponseAuthor
        from ..models.add_comment_response_update_author import (
            AddCommentResponseUpdateAuthor,
        )

        d = src_dict.copy()
        body = d.pop("body", UNSET)

        _author = d.pop("author", UNSET)
        author: Union[Unset, AddCommentResponseAuthor]
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = AddCommentResponseAuthor.from_dict(_author)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _update_author = d.pop("updateAuthor", UNSET)
        update_author: Union[Unset, AddCommentResponseUpdateAuthor]
        if isinstance(_update_author, Unset):
            update_author = UNSET
        else:
            update_author = AddCommentResponseUpdateAuthor.from_dict(_update_author)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, AddCommentResponseVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = AddCommentResponseVisibility.from_dict(_visibility)

        self_ = d.pop("self", UNSET)

        id = d.pop("id", UNSET)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        add_comment_response = cls(
            body=body,
            author=author,
            created=created,
            update_author=update_author,
            visibility=visibility,
            self_=self_,
            id=id,
            updated=updated,
        )

        add_comment_response.additional_properties = d
        return add_comment_response

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
