from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.get_issue_response_changelog_histories_history_metadata_cause import (
    GetIssueResponseChangelogHistoriesHistoryMetadataCause,
)
from ..models.get_issue_response_changelog_histories_history_metadata_actor import (
    GetIssueResponseChangelogHistoriesHistoryMetadataActor,
)
from ..models.get_issue_response_changelog_histories_history_metadata_generator import (
    GetIssueResponseChangelogHistoriesHistoryMetadataGenerator,
)


class GetIssueResponseChangelogHistoriesHistoryMetadata(BaseModel):
    """
    Attributes:
        activity_description (Optional[str]): The activity described in the history record
        activity_description_key (Optional[str]): The key of the activity described in the history record
        actor (Optional[GetIssueResponseChangelogHistoriesHistoryMetadataActor]):
        cause (Optional[GetIssueResponseChangelogHistoriesHistoryMetadataCause]):
        description (Optional[str]): The description of the history record
        description_key (Optional[str]): The description key of the history record
        email_description (Optional[str]): The description of the email address associated the history record
        email_description_key (Optional[str]): The description key of the email address associated the history record
        generator (Optional[GetIssueResponseChangelogHistoriesHistoryMetadataGenerator]):
        type_ (Optional[str]): The type of the history record
    """

    model_config = ConfigDict(extra="allow")

    activity_description: Optional[str] = None
    activity_description_key: Optional[str] = None
    actor: Optional["GetIssueResponseChangelogHistoriesHistoryMetadataActor"] = None
    cause: Optional["GetIssueResponseChangelogHistoriesHistoryMetadataCause"] = None
    description: Optional[str] = None
    description_key: Optional[str] = None
    email_description: Optional[str] = None
    email_description_key: Optional[str] = None
    generator: Optional[
        "GetIssueResponseChangelogHistoriesHistoryMetadataGenerator"
    ] = None
    type_: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["GetIssueResponseChangelogHistoriesHistoryMetadata"],
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
