from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="CreateCalendarEventResponseOrganizer")


@_attrs_define
class CreateCalendarEventResponseOrganizer:
    """
    Attributes:
        email (Union[Unset, str]):  Example: testcloud155@gmail.com.
        self_ (Union[Unset, bool]):  Example: True.
    """

    email: Union[Unset, str] = UNSET
    self_: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        self_ = self.self_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["email"] = email
        if self_ is not UNSET:
            field_dict["self"] = self_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("email", UNSET)

        self_ = d.pop("self", UNSET)

        create_calendar_event_response_organizer = cls(
            email=email,
            self_=self_,
        )

        create_calendar_event_response_organizer.additional_properties = d
        return create_calendar_event_response_organizer

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
