from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CreateCalendarEventResponseReminders")


@_attrs_define
class CreateCalendarEventResponseReminders:
    """
    Attributes:
        use_default (Union[Unset, bool]):  Example: True.
    """

    use_default: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        use_default = self.use_default

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if use_default is not UNSET:
            field_dict["useDefault"] = use_default

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        use_default = d.pop("useDefault", UNSET)

        create_calendar_event_response_reminders = cls(
            use_default=use_default,
        )

        create_calendar_event_response_reminders.additional_properties = d
        return create_calendar_event_response_reminders

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
