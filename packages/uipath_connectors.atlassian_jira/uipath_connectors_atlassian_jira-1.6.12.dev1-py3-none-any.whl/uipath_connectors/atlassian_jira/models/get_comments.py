from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.get_comments_author import GetCommentsAuthor
    from ..models.get_comments_properties_array_item_ref import (
        GetCommentsPropertiesArrayItemRef,
    )
    from ..models.get_comments_update_author import GetCommentsUpdateAuthor
    from ..models.get_comments_visibility import GetCommentsVisibility


T = TypeVar("T", bound="GetComments")


@_attrs_define
class GetComments:
    """
    Attributes:
        author (Union[Unset, GetCommentsAuthor]):
        body (Union[Unset, str]): Provide input for the comment using text
        created (Union[Unset, datetime.datetime]): The date and time at which the comment was created.
        id (Union[Unset, str]): The ID of the new comment.
        jsd_public (Union[Unset, bool]): Whether the comment is visible in Jira Service Desk. Defaults to true when
            comments are created in the Jira Cloud Platform. This includes when the site doesn't use Jira Service Desk or
            the project isn't a Jira Service Desk project and, therefore, there is no Jira Service Desk for the issue to be
            visible on. To create a comment with its visibility in Jira Service Desk set to false, use the Jira Service Desk
            REST API [Create request comment](https://developer.atlassian.com/cloud/jira/service-desk/rest/#api-rest-
            servicedeskapi-request-issueIdOrKey-comment-post) operation.
        properties (Union[Unset, list['GetCommentsPropertiesArrayItemRef']]):
        rendered_body (Union[Unset, str]): The rendered version of the comment.
        self_ (Union[Unset, str]): The URL of the comment.
        update_author (Union[Unset, GetCommentsUpdateAuthor]):
        updated (Union[Unset, datetime.datetime]): The date and time at which the comment was updated last.
        visibility (Union[Unset, GetCommentsVisibility]):
    """

    author: Union[Unset, "GetCommentsAuthor"] = UNSET
    body: Union[Unset, str] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    id: Union[Unset, str] = UNSET
    jsd_public: Union[Unset, bool] = UNSET
    properties: Union[Unset, list["GetCommentsPropertiesArrayItemRef"]] = UNSET
    rendered_body: Union[Unset, str] = UNSET
    self_: Union[Unset, str] = UNSET
    update_author: Union[Unset, "GetCommentsUpdateAuthor"] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    visibility: Union[Unset, "GetCommentsVisibility"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.author, Unset):
            author = self.author.to_dict()

        body = self.body

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        id = self.id

        jsd_public = self.jsd_public

        properties: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.properties, Unset):
            properties = []
            for componentsschemas_get_comments_properties_item_data in self.properties:
                componentsschemas_get_comments_properties_item = (
                    componentsschemas_get_comments_properties_item_data.to_dict()
                )
                properties.append(componentsschemas_get_comments_properties_item)

        rendered_body = self.rendered_body

        self_ = self.self_

        update_author: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.update_author, Unset):
            update_author = self.update_author.to_dict()

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        visibility: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if author is not UNSET:
            field_dict["author"] = author
        if body is not UNSET:
            field_dict["body"] = body
        if created is not UNSET:
            field_dict["created"] = created
        if id is not UNSET:
            field_dict["id"] = id
        if jsd_public is not UNSET:
            field_dict["jsdPublic"] = jsd_public
        if properties is not UNSET:
            field_dict["properties"] = properties
        if rendered_body is not UNSET:
            field_dict["renderedBody"] = rendered_body
        if self_ is not UNSET:
            field_dict["self"] = self_
        if update_author is not UNSET:
            field_dict["updateAuthor"] = update_author
        if updated is not UNSET:
            field_dict["updated"] = updated
        if visibility is not UNSET:
            field_dict["visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_comments_author import GetCommentsAuthor
        from ..models.get_comments_properties_array_item_ref import (
            GetCommentsPropertiesArrayItemRef,
        )
        from ..models.get_comments_update_author import GetCommentsUpdateAuthor
        from ..models.get_comments_visibility import GetCommentsVisibility

        d = src_dict.copy()
        _author = d.pop("author", UNSET)
        author: Union[Unset, GetCommentsAuthor]
        if isinstance(_author, Unset):
            author = UNSET
        else:
            author = GetCommentsAuthor.from_dict(_author)

        body = d.pop("body", UNSET)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        id = d.pop("id", UNSET)

        jsd_public = d.pop("jsdPublic", UNSET)

        properties = []
        _properties = d.pop("properties", UNSET)
        for componentsschemas_get_comments_properties_item_data in _properties or []:
            componentsschemas_get_comments_properties_item = (
                GetCommentsPropertiesArrayItemRef.from_dict(
                    componentsschemas_get_comments_properties_item_data
                )
            )

            properties.append(componentsschemas_get_comments_properties_item)

        rendered_body = d.pop("renderedBody", UNSET)

        self_ = d.pop("self", UNSET)

        _update_author = d.pop("updateAuthor", UNSET)
        update_author: Union[Unset, GetCommentsUpdateAuthor]
        if isinstance(_update_author, Unset):
            update_author = UNSET
        else:
            update_author = GetCommentsUpdateAuthor.from_dict(_update_author)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        _visibility = d.pop("visibility", UNSET)
        visibility: Union[Unset, GetCommentsVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = GetCommentsVisibility.from_dict(_visibility)

        get_comments = cls(
            author=author,
            body=body,
            created=created,
            id=id,
            jsd_public=jsd_public,
            properties=properties,
            rendered_body=rendered_body,
            self_=self_,
            update_author=update_author,
            updated=updated,
            visibility=visibility,
        )

        get_comments.additional_properties = d
        return get_comments

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
