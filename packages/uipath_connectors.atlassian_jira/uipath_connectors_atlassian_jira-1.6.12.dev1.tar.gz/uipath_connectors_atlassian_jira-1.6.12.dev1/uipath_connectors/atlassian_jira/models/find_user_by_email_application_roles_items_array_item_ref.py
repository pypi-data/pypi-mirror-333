from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="FindUserByEmailApplicationRolesItemsArrayItemRef")


@_attrs_define
class FindUserByEmailApplicationRolesItemsArrayItemRef:
    """
    Attributes:
        default_groups (Union[Unset, list[str]]):
        defined (Union[Unset, bool]): Deprecated.
        groups (Union[Unset, list[str]]):
        has_unlimited_seats (Union[Unset, bool]):
        key (Union[Unset, str]): The key of the application role.
        name (Union[Unset, str]): The display name of the application role.
        number_of_seats (Union[Unset, int]): The maximum count of users on your license.
        platform (Union[Unset, bool]): Indicates if the application role belongs to Jira platform (`jira-core`).
        remaining_seats (Union[Unset, int]): The count of users remaining on your license.
        selected_by_default (Union[Unset, bool]): Determines whether this application role should be selected by default
            on user creation.
        user_count (Union[Unset, int]): The number of users counting against your license.
        user_count_description (Union[Unset, str]): The [type of users](https://confluence.atlassian.com/x/lRW3Ng) being
            counted against your license.
    """

    default_groups: Union[Unset, list[str]] = UNSET
    defined: Union[Unset, bool] = UNSET
    groups: Union[Unset, list[str]] = UNSET
    has_unlimited_seats: Union[Unset, bool] = UNSET
    key: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    number_of_seats: Union[Unset, int] = UNSET
    platform: Union[Unset, bool] = UNSET
    remaining_seats: Union[Unset, int] = UNSET
    selected_by_default: Union[Unset, bool] = UNSET
    user_count: Union[Unset, int] = UNSET
    user_count_description: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        default_groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.default_groups, Unset):
            default_groups = self.default_groups

        defined = self.defined

        groups: Union[Unset, list[str]] = UNSET
        if not isinstance(self.groups, Unset):
            groups = self.groups

        has_unlimited_seats = self.has_unlimited_seats

        key = self.key

        name = self.name

        number_of_seats = self.number_of_seats

        platform = self.platform

        remaining_seats = self.remaining_seats

        selected_by_default = self.selected_by_default

        user_count = self.user_count

        user_count_description = self.user_count_description

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if default_groups is not UNSET:
            field_dict["defaultGroups"] = default_groups
        if defined is not UNSET:
            field_dict["defined"] = defined
        if groups is not UNSET:
            field_dict["groups"] = groups
        if has_unlimited_seats is not UNSET:
            field_dict["hasUnlimitedSeats"] = has_unlimited_seats
        if key is not UNSET:
            field_dict["key"] = key
        if name is not UNSET:
            field_dict["name"] = name
        if number_of_seats is not UNSET:
            field_dict["numberOfSeats"] = number_of_seats
        if platform is not UNSET:
            field_dict["platform"] = platform
        if remaining_seats is not UNSET:
            field_dict["remainingSeats"] = remaining_seats
        if selected_by_default is not UNSET:
            field_dict["selectedByDefault"] = selected_by_default
        if user_count is not UNSET:
            field_dict["userCount"] = user_count
        if user_count_description is not UNSET:
            field_dict["userCountDescription"] = user_count_description

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        default_groups = cast(list[str], d.pop("defaultGroups", UNSET))

        defined = d.pop("defined", UNSET)

        groups = cast(list[str], d.pop("groups", UNSET))

        has_unlimited_seats = d.pop("hasUnlimitedSeats", UNSET)

        key = d.pop("key", UNSET)

        name = d.pop("name", UNSET)

        number_of_seats = d.pop("numberOfSeats", UNSET)

        platform = d.pop("platform", UNSET)

        remaining_seats = d.pop("remainingSeats", UNSET)

        selected_by_default = d.pop("selectedByDefault", UNSET)

        user_count = d.pop("userCount", UNSET)

        user_count_description = d.pop("userCountDescription", UNSET)

        find_user_by_email_application_roles_items_array_item_ref = cls(
            default_groups=default_groups,
            defined=defined,
            groups=groups,
            has_unlimited_seats=has_unlimited_seats,
            key=key,
            name=name,
            number_of_seats=number_of_seats,
            platform=platform,
            remaining_seats=remaining_seats,
            selected_by_default=selected_by_default,
            user_count=user_count,
            user_count_description=user_count_description,
        )

        find_user_by_email_application_roles_items_array_item_ref.additional_properties = d
        return find_user_by_email_application_roles_items_array_item_ref

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
