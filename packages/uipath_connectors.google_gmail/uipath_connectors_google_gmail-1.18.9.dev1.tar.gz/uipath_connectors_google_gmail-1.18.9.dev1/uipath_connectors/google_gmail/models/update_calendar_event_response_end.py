from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime


T = TypeVar("T", bound="UpdateCalendarEventResponseEnd")


@_attrs_define
class UpdateCalendarEventResponseEnd:
    """
    Attributes:
        date_time (Union[Unset, datetime.datetime]):  Example: 2023-01-11T17:30:00.0000000+05:30.
        time_zone (Union[Unset, str]):  Example: Asia/Kolkata.
    """

    date_time: Union[Unset, datetime.datetime] = UNSET
    time_zone: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        date_time: Union[Unset, str] = UNSET
        if not isinstance(self.date_time, Unset):
            date_time = self.date_time.isoformat()

        time_zone = self.time_zone

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if date_time is not UNSET:
            field_dict["dateTime"] = date_time
        if time_zone is not UNSET:
            field_dict["timeZone"] = time_zone

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _date_time = d.pop("dateTime", UNSET)
        date_time: Union[Unset, datetime.datetime]
        if isinstance(_date_time, Unset):
            date_time = UNSET
        else:
            date_time = isoparse(_date_time)

        time_zone = d.pop("timeZone", UNSET)

        update_calendar_event_response_end = cls(
            date_time=date_time,
            time_zone=time_zone,
        )

        update_calendar_event_response_end.additional_properties = d
        return update_calendar_event_response_end

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
