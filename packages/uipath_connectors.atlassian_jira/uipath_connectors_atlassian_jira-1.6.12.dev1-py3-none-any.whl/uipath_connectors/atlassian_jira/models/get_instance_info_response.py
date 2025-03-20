from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime


T = TypeVar("T", bound="GetInstanceInfoResponse")


@_attrs_define
class GetInstanceInfoResponse:
    """
    Attributes:
        base_url (Union[Unset, str]): The base URL of the Jira instance
        site_url (Union[Unset, str]): The site URL of the Jira instance
        build_date (Union[Unset, datetime.datetime]): The timestamp when the Jira version was built.
        build_number (Union[Unset, int]): The build number of the Jira version.
        deployment_type (Union[Unset, str]): The type of server deployment. This is always returned as *Cloud*.
        scm_info (Union[Unset, str]): The unique identifier of the Jira version.
        server_time (Union[Unset, datetime.datetime]): The time in Jira when this request was responded to.
        server_title (Union[Unset, str]): The name of the Jira instance.
        version (Union[Unset, str]): The version of Jira.
        version_numbers (Union[Unset, list[int]]):
    """

    base_url: Union[Unset, str] = UNSET
    site_url: Union[Unset, str] = UNSET
    build_date: Union[Unset, datetime.datetime] = UNSET
    build_number: Union[Unset, int] = UNSET
    deployment_type: Union[Unset, str] = UNSET
    scm_info: Union[Unset, str] = UNSET
    server_time: Union[Unset, datetime.datetime] = UNSET
    server_title: Union[Unset, str] = UNSET
    version: Union[Unset, str] = UNSET
    version_numbers: Union[Unset, list[int]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        base_url = self.base_url

        site_url = self.site_url

        build_date: Union[Unset, str] = UNSET
        if not isinstance(self.build_date, Unset):
            build_date = self.build_date.isoformat()

        build_number = self.build_number

        deployment_type = self.deployment_type

        scm_info = self.scm_info

        server_time: Union[Unset, str] = UNSET
        if not isinstance(self.server_time, Unset):
            server_time = self.server_time.isoformat()

        server_title = self.server_title

        version = self.version

        version_numbers: Union[Unset, list[int]] = UNSET
        if not isinstance(self.version_numbers, Unset):
            version_numbers = self.version_numbers

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if base_url is not UNSET:
            field_dict["baseUrl"] = base_url
        if site_url is not UNSET:
            field_dict["siteUrl"] = site_url
        if build_date is not UNSET:
            field_dict["buildDate"] = build_date
        if build_number is not UNSET:
            field_dict["buildNumber"] = build_number
        if deployment_type is not UNSET:
            field_dict["deploymentType"] = deployment_type
        if scm_info is not UNSET:
            field_dict["scmInfo"] = scm_info
        if server_time is not UNSET:
            field_dict["serverTime"] = server_time
        if server_title is not UNSET:
            field_dict["serverTitle"] = server_title
        if version is not UNSET:
            field_dict["version"] = version
        if version_numbers is not UNSET:
            field_dict["versionNumbers"] = version_numbers

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        base_url = d.pop("baseUrl", UNSET)

        site_url = d.pop("siteUrl", UNSET)

        _build_date = d.pop("buildDate", UNSET)
        build_date: Union[Unset, datetime.datetime]
        if isinstance(_build_date, Unset):
            build_date = UNSET
        else:
            build_date = isoparse(_build_date)

        build_number = d.pop("buildNumber", UNSET)

        deployment_type = d.pop("deploymentType", UNSET)

        scm_info = d.pop("scmInfo", UNSET)

        _server_time = d.pop("serverTime", UNSET)
        server_time: Union[Unset, datetime.datetime]
        if isinstance(_server_time, Unset):
            server_time = UNSET
        else:
            server_time = isoparse(_server_time)

        server_title = d.pop("serverTitle", UNSET)

        version = d.pop("version", UNSET)

        version_numbers = cast(list[int], d.pop("versionNumbers", UNSET))

        get_instance_info_response = cls(
            base_url=base_url,
            site_url=site_url,
            build_date=build_date,
            build_number=build_number,
            deployment_type=deployment_type,
            scm_info=scm_info,
            server_time=server_time,
            server_title=server_title,
            version=version,
            version_numbers=version_numbers,
        )

        get_instance_info_response.additional_properties = d
        return get_instance_info_response

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
