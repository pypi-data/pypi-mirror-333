from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime


T = TypeVar("T", bound="TurnOnAutomaticRepliesRequest")


@_attrs_define
class TurnOnAutomaticRepliesRequest:
    """
    Attributes:
        response_subject (str): The subject line used for the automatic reply email.
        response_body_plain_text (Union[Unset, str]): The text content of the automatic reply.
        restrict_to_contacts (Union[Unset, bool]): Limit automatic replies to only those in your contacts list.
        start_time (Union[Unset, datetime.datetime]): The date and time when automatic replies will begin. Example:
            1737527373.
        end_time (Union[Unset, datetime.datetime]): The date and time when automatic replies will stop. Example:
            1737527373.
        send_replies_outside_domain (Union[Unset, bool]): Sends replies to user who are outside users domain.
    """

    response_subject: str
    response_body_plain_text: Union[Unset, str] = UNSET
    restrict_to_contacts: Union[Unset, bool] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    send_replies_outside_domain: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response_subject = self.response_subject

        response_body_plain_text = self.response_body_plain_text

        restrict_to_contacts = self.restrict_to_contacts

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        send_replies_outside_domain = self.send_replies_outside_domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "responseSubject": response_subject,
            }
        )
        if response_body_plain_text is not UNSET:
            field_dict["responseBodyPlainText"] = response_body_plain_text
        if restrict_to_contacts is not UNSET:
            field_dict["restrictToContacts"] = restrict_to_contacts
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if send_replies_outside_domain is not UNSET:
            field_dict["sendRepliesOutsideDomain"] = send_replies_outside_domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        response_subject = d.pop("responseSubject")

        response_body_plain_text = d.pop("responseBodyPlainText", UNSET)

        restrict_to_contacts = d.pop("restrictToContacts", UNSET)

        _start_time = d.pop("startTime", UNSET)
        start_time: Union[Unset, datetime.datetime]
        if isinstance(_start_time, Unset):
            start_time = UNSET
        else:
            start_time = isoparse(_start_time)

        _end_time = d.pop("endTime", UNSET)
        end_time: Union[Unset, datetime.datetime]
        if isinstance(_end_time, Unset):
            end_time = UNSET
        else:
            end_time = isoparse(_end_time)

        send_replies_outside_domain = d.pop("sendRepliesOutsideDomain", UNSET)

        turn_on_automatic_replies_request = cls(
            response_subject=response_subject,
            response_body_plain_text=response_body_plain_text,
            restrict_to_contacts=restrict_to_contacts,
            start_time=start_time,
            end_time=end_time,
            send_replies_outside_domain=send_replies_outside_domain,
        )

        turn_on_automatic_replies_request.additional_properties = d
        return turn_on_automatic_replies_request

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
