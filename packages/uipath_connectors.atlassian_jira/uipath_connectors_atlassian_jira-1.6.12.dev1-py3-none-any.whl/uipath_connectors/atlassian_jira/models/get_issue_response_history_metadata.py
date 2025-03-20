from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_issue_response_history_metadata_actor import (
        GetIssueResponseHistoryMetadataActor,
    )
    from ..models.get_issue_response_history_metadata_generator import (
        GetIssueResponseHistoryMetadataGenerator,
    )
    from ..models.get_issue_response_history_metadata_cause import (
        GetIssueResponseHistoryMetadataCause,
    )


T = TypeVar("T", bound="GetIssueResponseHistoryMetadata")


@_attrs_define
class GetIssueResponseHistoryMetadata:
    """
    Attributes:
        activity_description (Union[Unset, str]): The activity described in the history record
        activity_description_key (Union[Unset, str]): The key of the activity described in the history record
        actor (Union[Unset, GetIssueResponseHistoryMetadataActor]):
        cause (Union[Unset, GetIssueResponseHistoryMetadataCause]):
        description (Union[Unset, str]): The description of the history record
        description_key (Union[Unset, str]): The description key of the history record
        email_description (Union[Unset, str]): The description of the email address associated the history record
        email_description_key (Union[Unset, str]): The description key of the email address associated the history
            record
        generator (Union[Unset, GetIssueResponseHistoryMetadataGenerator]):
        type_ (Union[Unset, str]): The type of the history record
    """

    activity_description: Union[Unset, str] = UNSET
    activity_description_key: Union[Unset, str] = UNSET
    actor: Union[Unset, "GetIssueResponseHistoryMetadataActor"] = UNSET
    cause: Union[Unset, "GetIssueResponseHistoryMetadataCause"] = UNSET
    description: Union[Unset, str] = UNSET
    description_key: Union[Unset, str] = UNSET
    email_description: Union[Unset, str] = UNSET
    email_description_key: Union[Unset, str] = UNSET
    generator: Union[Unset, "GetIssueResponseHistoryMetadataGenerator"] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        activity_description = self.activity_description

        activity_description_key = self.activity_description_key

        actor: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.actor, Unset):
            actor = self.actor.to_dict()

        cause: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.cause, Unset):
            cause = self.cause.to_dict()

        description = self.description

        description_key = self.description_key

        email_description = self.email_description

        email_description_key = self.email_description_key

        generator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.generator, Unset):
            generator = self.generator.to_dict()

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if activity_description is not UNSET:
            field_dict["activityDescription"] = activity_description
        if activity_description_key is not UNSET:
            field_dict["activityDescriptionKey"] = activity_description_key
        if actor is not UNSET:
            field_dict["actor"] = actor
        if cause is not UNSET:
            field_dict["cause"] = cause
        if description is not UNSET:
            field_dict["description"] = description
        if description_key is not UNSET:
            field_dict["descriptionKey"] = description_key
        if email_description is not UNSET:
            field_dict["emailDescription"] = email_description
        if email_description_key is not UNSET:
            field_dict["emailDescriptionKey"] = email_description_key
        if generator is not UNSET:
            field_dict["generator"] = generator
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_issue_response_history_metadata_actor import (
            GetIssueResponseHistoryMetadataActor,
        )
        from ..models.get_issue_response_history_metadata_generator import (
            GetIssueResponseHistoryMetadataGenerator,
        )
        from ..models.get_issue_response_history_metadata_cause import (
            GetIssueResponseHistoryMetadataCause,
        )

        d = src_dict.copy()
        activity_description = d.pop("activityDescription", UNSET)

        activity_description_key = d.pop("activityDescriptionKey", UNSET)

        _actor = d.pop("actor", UNSET)
        actor: Union[Unset, GetIssueResponseHistoryMetadataActor]
        if isinstance(_actor, Unset):
            actor = UNSET
        else:
            actor = GetIssueResponseHistoryMetadataActor.from_dict(_actor)

        _cause = d.pop("cause", UNSET)
        cause: Union[Unset, GetIssueResponseHistoryMetadataCause]
        if isinstance(_cause, Unset):
            cause = UNSET
        else:
            cause = GetIssueResponseHistoryMetadataCause.from_dict(_cause)

        description = d.pop("description", UNSET)

        description_key = d.pop("descriptionKey", UNSET)

        email_description = d.pop("emailDescription", UNSET)

        email_description_key = d.pop("emailDescriptionKey", UNSET)

        _generator = d.pop("generator", UNSET)
        generator: Union[Unset, GetIssueResponseHistoryMetadataGenerator]
        if isinstance(_generator, Unset):
            generator = UNSET
        else:
            generator = GetIssueResponseHistoryMetadataGenerator.from_dict(_generator)

        type_ = d.pop("type", UNSET)

        get_issue_response_history_metadata = cls(
            activity_description=activity_description,
            activity_description_key=activity_description_key,
            actor=actor,
            cause=cause,
            description=description,
            description_key=description_key,
            email_description=email_description,
            email_description_key=email_description_key,
            generator=generator,
            type_=type_,
        )

        get_issue_response_history_metadata.additional_properties = d
        return get_issue_response_history_metadata

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
