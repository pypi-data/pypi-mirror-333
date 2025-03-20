from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.search_issueby_jql_changelog_histories_history_metadata_cause import (
    SearchIssuebyJQLChangelogHistoriesHistoryMetadataCause,
)
from ..models.search_issueby_jql_changelog_histories_history_metadata_generator import (
    SearchIssuebyJQLChangelogHistoriesHistoryMetadataGenerator,
)
from ..models.search_issueby_jql_changelog_histories_history_metadata_actor import (
    SearchIssuebyJQLChangelogHistoriesHistoryMetadataActor,
)


class SearchIssuebyJQLChangelogHistoriesHistoryMetadata(BaseModel):
    """
    Attributes:
        activity_description (Optional[str]): The activity described in the history record.
        activity_description_key (Optional[str]): The key of the activity described in the history record.
        actor (Optional[SearchIssuebyJQLChangelogHistoriesHistoryMetadataActor]):
        cause (Optional[SearchIssuebyJQLChangelogHistoriesHistoryMetadataCause]):
        description (Optional[str]): The description of the history record.
        description_key (Optional[str]): The description key of the history record.
        email_description (Optional[str]): The description of the email address associated the history record.
        email_description_key (Optional[str]): The description key of the email address associated the history record.
        generator (Optional[SearchIssuebyJQLChangelogHistoriesHistoryMetadataGenerator]):
        type_ (Optional[str]): The type of the history record.
    """

    model_config = ConfigDict(extra="allow")

    activity_description: Optional[str] = None
    activity_description_key: Optional[str] = None
    actor: Optional["SearchIssuebyJQLChangelogHistoriesHistoryMetadataActor"] = None
    cause: Optional["SearchIssuebyJQLChangelogHistoriesHistoryMetadataCause"] = None
    description: Optional[str] = None
    description_key: Optional[str] = None
    email_description: Optional[str] = None
    email_description_key: Optional[str] = None
    generator: Optional[
        "SearchIssuebyJQLChangelogHistoriesHistoryMetadataGenerator"
    ] = None
    type_: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SearchIssuebyJQLChangelogHistoriesHistoryMetadata"],
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
