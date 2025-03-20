from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.create_calendar_event_response_show_as import (
    CreateCalendarEventResponseShowAs,
)
from ..models.create_calendar_event_response_visibility import (
    CreateCalendarEventResponseVisibility,
)
from dateutil.parser import isoparse
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.create_calendar_event_response_reminders import (
        CreateCalendarEventResponseReminders,
    )
    from ..models.create_calendar_event_response_end import (
        CreateCalendarEventResponseEnd,
    )
    from ..models.create_calendar_event_response_creator import (
        CreateCalendarEventResponseCreator,
    )
    from ..models.create_calendar_event_response_start import (
        CreateCalendarEventResponseStart,
    )
    from ..models.create_calendar_event_response_organizer import (
        CreateCalendarEventResponseOrganizer,
    )


T = TypeVar("T", bound="CreateCalendarEventResponse")


@_attrs_define
class CreateCalendarEventResponse:
    """
    Attributes:
        show_as (Union[Unset, CreateCalendarEventResponseShowAs]): Show as Example: string.
        visibility (Union[Unset, CreateCalendarEventResponseVisibility]): Visibility of the event. Example: string.
        created (Union[Unset, datetime.datetime]):  Example: 2023-01-02T04:49:58.0000000+00:00.
        creator (Union[Unset, CreateCalendarEventResponseCreator]):
        end (Union[Unset, CreateCalendarEventResponseEnd]):
        etag (Union[Unset, str]):  Example: "3345269997634000".
        event_type (Union[Unset, str]):  Example: default.
        html_link (Union[Unset, str]):  Example:
            https://www.google.com/calendar/event?eid=dGV0NmVhMW90MWNjNDNsaHJ1NzF2c3I2aGsgdGVzdGNsb3VkMTU1QG0.
        i_cal_uid (Union[Unset, str]):  Example: tet6ea1ot1cc43lhru71vsr6hk@google.com.
        id (Union[Unset, str]):  Example: tet6ea1ot1cc43lhru71vsr6hk.
        kind (Union[Unset, str]):  Example: calendar#event.
        organizer (Union[Unset, CreateCalendarEventResponseOrganizer]):
        reminders (Union[Unset, CreateCalendarEventResponseReminders]):
        sequence (Union[Unset, int]):  Example: 0.0.
        start (Union[Unset, CreateCalendarEventResponseStart]):
        status (Union[Unset, str]):  Example: confirmed.
        summary (Union[Unset, str]):  Example: New.
        updated (Union[Unset, datetime.datetime]):  Example: 2023-01-02T04:49:58.8170000+00:00.
    """

    show_as: Union[Unset, CreateCalendarEventResponseShowAs] = UNSET
    visibility: Union[Unset, CreateCalendarEventResponseVisibility] = UNSET
    created: Union[Unset, datetime.datetime] = UNSET
    creator: Union[Unset, "CreateCalendarEventResponseCreator"] = UNSET
    end: Union[Unset, "CreateCalendarEventResponseEnd"] = UNSET
    etag: Union[Unset, str] = UNSET
    event_type: Union[Unset, str] = UNSET
    html_link: Union[Unset, str] = UNSET
    i_cal_uid: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    kind: Union[Unset, str] = UNSET
    organizer: Union[Unset, "CreateCalendarEventResponseOrganizer"] = UNSET
    reminders: Union[Unset, "CreateCalendarEventResponseReminders"] = UNSET
    sequence: Union[Unset, int] = UNSET
    start: Union[Unset, "CreateCalendarEventResponseStart"] = UNSET
    status: Union[Unset, str] = UNSET
    summary: Union[Unset, str] = UNSET
    updated: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        show_as: Union[Unset, str] = UNSET
        if not isinstance(self.show_as, Unset):
            show_as = self.show_as.value

        visibility: Union[Unset, str] = UNSET
        if not isinstance(self.visibility, Unset):
            visibility = self.visibility.value

        created: Union[Unset, str] = UNSET
        if not isinstance(self.created, Unset):
            created = self.created.isoformat()

        creator: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        end: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.end, Unset):
            end = self.end.to_dict()

        etag = self.etag

        event_type = self.event_type

        html_link = self.html_link

        i_cal_uid = self.i_cal_uid

        id = self.id

        kind = self.kind

        organizer: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.organizer, Unset):
            organizer = self.organizer.to_dict()

        reminders: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.reminders, Unset):
            reminders = self.reminders.to_dict()

        sequence = self.sequence

        start: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.start, Unset):
            start = self.start.to_dict()

        status = self.status

        summary = self.summary

        updated: Union[Unset, str] = UNSET
        if not isinstance(self.updated, Unset):
            updated = self.updated.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if show_as is not UNSET:
            field_dict["ShowAs"] = show_as
        if visibility is not UNSET:
            field_dict["Visibility"] = visibility
        if created is not UNSET:
            field_dict["created"] = created
        if creator is not UNSET:
            field_dict["creator"] = creator
        if end is not UNSET:
            field_dict["end"] = end
        if etag is not UNSET:
            field_dict["etag"] = etag
        if event_type is not UNSET:
            field_dict["eventType"] = event_type
        if html_link is not UNSET:
            field_dict["htmlLink"] = html_link
        if i_cal_uid is not UNSET:
            field_dict["iCalUID"] = i_cal_uid
        if id is not UNSET:
            field_dict["id"] = id
        if kind is not UNSET:
            field_dict["kind"] = kind
        if organizer is not UNSET:
            field_dict["organizer"] = organizer
        if reminders is not UNSET:
            field_dict["reminders"] = reminders
        if sequence is not UNSET:
            field_dict["sequence"] = sequence
        if start is not UNSET:
            field_dict["start"] = start
        if status is not UNSET:
            field_dict["status"] = status
        if summary is not UNSET:
            field_dict["summary"] = summary
        if updated is not UNSET:
            field_dict["updated"] = updated

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.create_calendar_event_response_reminders import (
            CreateCalendarEventResponseReminders,
        )
        from ..models.create_calendar_event_response_end import (
            CreateCalendarEventResponseEnd,
        )
        from ..models.create_calendar_event_response_creator import (
            CreateCalendarEventResponseCreator,
        )
        from ..models.create_calendar_event_response_start import (
            CreateCalendarEventResponseStart,
        )
        from ..models.create_calendar_event_response_organizer import (
            CreateCalendarEventResponseOrganizer,
        )

        d = src_dict.copy()
        _show_as = d.pop("ShowAs", UNSET)
        show_as: Union[Unset, CreateCalendarEventResponseShowAs]
        if isinstance(_show_as, Unset):
            show_as = UNSET
        else:
            show_as = CreateCalendarEventResponseShowAs(_show_as)

        _visibility = d.pop("Visibility", UNSET)
        visibility: Union[Unset, CreateCalendarEventResponseVisibility]
        if isinstance(_visibility, Unset):
            visibility = UNSET
        else:
            visibility = CreateCalendarEventResponseVisibility(_visibility)

        _created = d.pop("created", UNSET)
        created: Union[Unset, datetime.datetime]
        if isinstance(_created, Unset):
            created = UNSET
        else:
            created = isoparse(_created)

        _creator = d.pop("creator", UNSET)
        creator: Union[Unset, CreateCalendarEventResponseCreator]
        if isinstance(_creator, Unset):
            creator = UNSET
        else:
            creator = CreateCalendarEventResponseCreator.from_dict(_creator)

        _end = d.pop("end", UNSET)
        end: Union[Unset, CreateCalendarEventResponseEnd]
        if isinstance(_end, Unset):
            end = UNSET
        else:
            end = CreateCalendarEventResponseEnd.from_dict(_end)

        etag = d.pop("etag", UNSET)

        event_type = d.pop("eventType", UNSET)

        html_link = d.pop("htmlLink", UNSET)

        i_cal_uid = d.pop("iCalUID", UNSET)

        id = d.pop("id", UNSET)

        kind = d.pop("kind", UNSET)

        _organizer = d.pop("organizer", UNSET)
        organizer: Union[Unset, CreateCalendarEventResponseOrganizer]
        if isinstance(_organizer, Unset):
            organizer = UNSET
        else:
            organizer = CreateCalendarEventResponseOrganizer.from_dict(_organizer)

        _reminders = d.pop("reminders", UNSET)
        reminders: Union[Unset, CreateCalendarEventResponseReminders]
        if isinstance(_reminders, Unset):
            reminders = UNSET
        else:
            reminders = CreateCalendarEventResponseReminders.from_dict(_reminders)

        sequence = d.pop("sequence", UNSET)

        _start = d.pop("start", UNSET)
        start: Union[Unset, CreateCalendarEventResponseStart]
        if isinstance(_start, Unset):
            start = UNSET
        else:
            start = CreateCalendarEventResponseStart.from_dict(_start)

        status = d.pop("status", UNSET)

        summary = d.pop("summary", UNSET)

        _updated = d.pop("updated", UNSET)
        updated: Union[Unset, datetime.datetime]
        if isinstance(_updated, Unset):
            updated = UNSET
        else:
            updated = isoparse(_updated)

        create_calendar_event_response = cls(
            show_as=show_as,
            visibility=visibility,
            created=created,
            creator=creator,
            end=end,
            etag=etag,
            event_type=event_type,
            html_link=html_link,
            i_cal_uid=i_cal_uid,
            id=id,
            kind=kind,
            organizer=organizer,
            reminders=reminders,
            sequence=sequence,
            start=start,
            status=status,
            summary=summary,
            updated=updated,
        )

        create_calendar_event_response.additional_properties = d
        return create_calendar_event_response

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
