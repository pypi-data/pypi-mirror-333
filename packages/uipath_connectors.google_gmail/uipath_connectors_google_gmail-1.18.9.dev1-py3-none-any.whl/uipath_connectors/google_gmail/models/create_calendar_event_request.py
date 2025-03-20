from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_calendar_event_request_show_as import (
    CreateCalendarEventRequestShowAs,
)
from ..models.create_calendar_event_request_visibility import (
    CreateCalendarEventRequestVisibility,
)
from dateutil.parser import isoparse
from typing import Union
import datetime


T = TypeVar("T", bound="CreateCalendarEventRequest")


@_attrs_define
class CreateCalendarEventRequest:
    """
    Attributes:
        end_date_time (datetime.datetime):  Example: 2023-01-02T06:35:28.6310000+00:00.
        event_title (str):  Example: string.
        start_date_time (datetime.datetime):  Example: 2023-01-02T06:35:28.6310000+00:00.
        all_day_event (Union[Unset, bool]):
        can_invite_others (Union[Unset, bool]):
        can_modify_event (Union[Unset, bool]):
        can_see_attendees_list (Union[Unset, bool]):
        description (Union[Unset, str]):  Example: string.
        location (Union[Unset, str]):  Example: string.
        optional_attendees (Union[Unset, str]):  Example: string.
        output_event_timezone (Union[Unset, str]):  Example: string.
        required_attendees (Union[Unset, str]):  Example: string.
        resource_attendees (Union[Unset, str]):  Example: string.
        show_as (Union[Unset, CreateCalendarEventRequestShowAs]): Show as Example: string.
        timezone (Union[Unset, str]):  Example: string.
        visibility (Union[Unset, CreateCalendarEventRequestVisibility]): Visibility of the event. Example: string.
    """

    end_date_time: datetime.datetime
    event_title: str
    start_date_time: datetime.datetime
    all_day_event: Union[Unset, bool] = UNSET
    can_invite_others: Union[Unset, bool] = UNSET
    can_modify_event: Union[Unset, bool] = UNSET
    can_see_attendees_list: Union[Unset, bool] = UNSET
    description: Union[Unset, str] = UNSET
    location: Union[Unset, str] = UNSET
    optional_attendees: Union[Unset, str] = UNSET
    output_event_timezone: Union[Unset, str] = UNSET
    required_attendees: Union[Unset, str] = UNSET
    resource_attendees: Union[Unset, str] = UNSET
    show_as: Union[Unset, CreateCalendarEventRequestShowAs] = UNSET
    timezone: Union[Unset, str] = UNSET
    visibility: Union[Unset, CreateCalendarEventRequestVisibility] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        end_date_time = self.end_date_time.isoformat()

        event_title = self.event_title

        start_date_time = self.start_date_time.isoformat()

        all_day_event = self.all_day_event

        can_invite_others = self.can_invite_others

        can_modify_event = self.can_modify_event

        can_see_attendees_list = self.can_see_attendees_list

        description = self.description

        location = self.location

        optional_attendees = self.optional_attendees

        output_event_timezone = self.output_event_timezone

        required_attendees = self.required_attendees

        resource_attendees = self.resource_attendees

        show_as: Union[Unset, str] = UNSET
        if not isinstance(self.show_as, Unset):
            show_as = self.show_as.value

        timezone = self.timezone

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "EndDateTime": end_date_time,
                "EventTitle": event_title,
                "StartDateTime": start_date_time,
            }
        )
        if all_day_event is not UNSET:
            field_dict["AllDayEvent"] = all_day_event
        if can_invite_others is not UNSET:
            field_dict["CanInviteOthers"] = can_invite_others
        if can_modify_event is not UNSET:
            field_dict["CanModifyEvent"] = can_modify_event
        if can_see_attendees_list is not UNSET:
            field_dict["CanSeeAttendeesList"] = can_see_attendees_list
        if description is not UNSET:
            field_dict["Description"] = description
        if location is not UNSET:
            field_dict["Location"] = location
        if optional_attendees is not UNSET:
            field_dict["OptionalAttendees"] = optional_attendees
        if output_event_timezone is not UNSET:
            field_dict["OutputEventTimezone"] = output_event_timezone
        if required_attendees is not UNSET:
            field_dict["RequiredAttendees"] = required_attendees
        if resource_attendees is not UNSET:
            field_dict["ResourceAttendees"] = resource_attendees
        if show_as is not UNSET:
            field_dict["ShowAs"] = show_as
        if timezone is not UNSET:
            field_dict["Timezone"] = timezone
        if visibility is not UNSET:
            field_dict["Visibility"] = visibility

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        end_date_time = isoparse(d.pop("EndDateTime"))

        event_title = d.pop("EventTitle")

        start_date_time = isoparse(d.pop("StartDateTime"))

        all_day_event = d.pop("AllDayEvent", UNSET)

        can_invite_others = d.pop("CanInviteOthers", UNSET)

        can_modify_event = d.pop("CanModifyEvent", UNSET)

        can_see_attendees_list = d.pop("CanSeeAttendeesList", UNSET)

        description = d.pop("Description", UNSET)

        location = d.pop("Location", UNSET)

        optional_attendees = d.pop("OptionalAttendees", UNSET)

        output_event_timezone = d.pop("OutputEventTimezone", UNSET)

        required_attendees = d.pop("RequiredAttendees", UNSET)

        resource_attendees = d.pop("ResourceAttendees", UNSET)

        _show_as = d.pop("ShowAs", UNSET)
        show_as: Union[Unset, CreateCalendarEventRequestShowAs]
        if isinstance(_show_as, Unset):
            show_as = UNSET
        else:
            show_as = CreateCalendarEventRequestShowAs(_show_as)

        timezone = d.pop("Timezone", UNSET)

        _visibility = d.pop("Visibility", UNSET)
        visibility: Union[Unset, CreateCalendarEventRequestVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = CreateCalendarEventRequestVisibility(_visibility)

        create_calendar_event_request = cls(
            end_date_time=end_date_time,
            event_title=event_title,
            start_date_time=start_date_time,
            all_day_event=all_day_event,
            can_invite_others=can_invite_others,
            can_modify_event=can_modify_event,
            can_see_attendees_list=can_see_attendees_list,
            description=description,
            location=location,
            optional_attendees=optional_attendees,
            output_event_timezone=output_event_timezone,
            required_attendees=required_attendees,
            resource_attendees=resource_attendees,
            show_as=show_as,
            timezone=timezone,
            visibility=visibility,
        )

        create_calendar_event_request.additional_properties = d
        return create_calendar_event_request

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
