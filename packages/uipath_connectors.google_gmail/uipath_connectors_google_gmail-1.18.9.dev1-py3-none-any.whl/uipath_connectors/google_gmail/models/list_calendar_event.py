from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.list_calendar_event_attendees_array_item_ref import (
        ListCalendarEventAttendeesArrayItemRef,
    )


T = TypeVar("T", bound="ListCalendarEvent")


@_attrs_define
class ListCalendarEvent:
    """
    Attributes:
        all_day (Union[Unset, bool]):
        attendees (Union[Unset, list['ListCalendarEventAttendeesArrayItemRef']]):
        calendar_id (Union[Unset, str]):  Example: primary.
        calendar_name (Union[Unset, str]):  Example: primary.
        description (Union[Unset, str]):  Example: string.
        has_attachments (Union[Unset, bool]):
        id (Union[Unset, str]):  Example: tet6ea1ot1cc43lhru71vsr6hk.
        title (Union[Unset, str]):  Example: New.
        self_organizer (Union[Unset, bool]):  Example: True.
    """

    all_day: Union[Unset, bool] = UNSET
    attendees: Union[Unset, list["ListCalendarEventAttendeesArrayItemRef"]] = UNSET
    calendar_id: Union[Unset, str] = UNSET
    calendar_name: Union[Unset, str] = UNSET
    description: Union[Unset, str] = UNSET
    has_attachments: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET
    title: Union[Unset, str] = UNSET
    self_organizer: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        all_day = self.all_day

        attendees: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.attendees, Unset):
            attendees = []
            for (
                componentsschemas_list_calendar_event_attendees_item_data
            ) in self.attendees:
                componentsschemas_list_calendar_event_attendees_item = (
                    componentsschemas_list_calendar_event_attendees_item_data.to_dict()
                )
                attendees.append(componentsschemas_list_calendar_event_attendees_item)

        calendar_id = self.calendar_id

        calendar_name = self.calendar_name

        description = self.description

        has_attachments = self.has_attachments

        id = self.id

        title = self.title

        self_organizer = self.self_organizer

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if all_day is not UNSET:
            field_dict["AllDay"] = all_day
        if attendees is not UNSET:
            field_dict["Attendees"] = attendees
        if calendar_id is not UNSET:
            field_dict["CalendarID"] = calendar_id
        if calendar_name is not UNSET:
            field_dict["CalendarName"] = calendar_name
        if description is not UNSET:
            field_dict["Description"] = description
        if has_attachments is not UNSET:
            field_dict["HasAttachments"] = has_attachments
        if id is not UNSET:
            field_dict["ID"] = id
        if title is not UNSET:
            field_dict["Title"] = title
        if self_organizer is not UNSET:
            field_dict["selfOrganizer"] = self_organizer

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.list_calendar_event_attendees_array_item_ref import (
            ListCalendarEventAttendeesArrayItemRef,
        )

        d = src_dict.copy()
        all_day = d.pop("AllDay", UNSET)

        attendees = []
        _attendees = d.pop("Attendees", UNSET)
        for componentsschemas_list_calendar_event_attendees_item_data in (
            _attendees or []
        ):
            componentsschemas_list_calendar_event_attendees_item = (
                ListCalendarEventAttendeesArrayItemRef.from_dict(
                    componentsschemas_list_calendar_event_attendees_item_data
                )
            )

            attendees.append(componentsschemas_list_calendar_event_attendees_item)

        calendar_id = d.pop("CalendarID", UNSET)

        calendar_name = d.pop("CalendarName", UNSET)

        description = d.pop("Description", UNSET)

        has_attachments = d.pop("HasAttachments", UNSET)

        id = d.pop("ID", UNSET)

        title = d.pop("Title", UNSET)

        self_organizer = d.pop("selfOrganizer", UNSET)

        list_calendar_event = cls(
            all_day=all_day,
            attendees=attendees,
            calendar_id=calendar_id,
            calendar_name=calendar_name,
            description=description,
            has_attachments=has_attachments,
            id=id,
            title=title,
            self_organizer=self_organizer,
        )

        list_calendar_event.additional_properties = d
        return list_calendar_event

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
