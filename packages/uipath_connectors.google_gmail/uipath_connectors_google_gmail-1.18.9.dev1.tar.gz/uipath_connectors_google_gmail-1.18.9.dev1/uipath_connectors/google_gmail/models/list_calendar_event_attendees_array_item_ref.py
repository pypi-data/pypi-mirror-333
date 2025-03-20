from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="ListCalendarEventAttendeesArrayItemRef")


@_attrs_define
class ListCalendarEventAttendeesArrayItemRef:
    """
    Attributes:
        email (Union[Unset, str]):  Example: mohit.achary@uipath.com.
        response (Union[Unset, str]):  Example: needsAction.
        type_ (Union[Unset, str]):  Example: required.
    """

    email: Union[Unset, str] = UNSET
    response: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        email = self.email

        response = self.response

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if email is not UNSET:
            field_dict["Email"] = email
        if response is not UNSET:
            field_dict["Response"] = response
        if type_ is not UNSET:
            field_dict["Type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        email = d.pop("Email", UNSET)

        response = d.pop("Response", UNSET)

        type_ = d.pop("Type", UNSET)

        list_calendar_event_attendees_array_item_ref = cls(
            email=email,
            response=response,
            type_=type_,
        )

        list_calendar_event_attendees_array_item_ref.additional_properties = d
        return list_calendar_event_attendees_array_item_ref

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
