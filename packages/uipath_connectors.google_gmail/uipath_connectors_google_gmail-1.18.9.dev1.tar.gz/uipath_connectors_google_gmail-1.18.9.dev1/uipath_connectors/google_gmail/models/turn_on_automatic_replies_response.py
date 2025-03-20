from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import Union
import datetime


T = TypeVar("T", bound="TurnOnAutomaticRepliesResponse")


@_attrs_define
class TurnOnAutomaticRepliesResponse:
    """
    Attributes:
        response_body_plain_text (Union[Unset, str]): The text content of the automatic reply.
        response_subject (Union[Unset, str]): The subject line used for the automatic reply email.
        enable_auto_reply (Union[Unset, bool]): Toggle to turn the automatic reply feature on or off.
        restrict_to_contacts (Union[Unset, bool]): Limit automatic replies to only those in your contacts list.
        start_time (Union[Unset, datetime.datetime]): The date and time when automatic replies will begin. Example:
            1737527373.
        end_time (Union[Unset, datetime.datetime]): The date and time when automatic replies will stop. Example:
            1737527373.
        restrict_to_domain (Union[Unset, bool]): Send automatic replies to recipients outside your domain.
    """

    response_body_plain_text: Union[Unset, str] = UNSET
    response_subject: Union[Unset, str] = UNSET
    enable_auto_reply: Union[Unset, bool] = UNSET
    restrict_to_contacts: Union[Unset, bool] = UNSET
    start_time: Union[Unset, datetime.datetime] = UNSET
    end_time: Union[Unset, datetime.datetime] = UNSET
    restrict_to_domain: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response_body_plain_text = self.response_body_plain_text

        response_subject = self.response_subject

        enable_auto_reply = self.enable_auto_reply

        restrict_to_contacts = self.restrict_to_contacts

        start_time: Union[Unset, str] = UNSET
        if not isinstance(self.start_time, Unset):
            start_time = self.start_time.isoformat()

        end_time: Union[Unset, str] = UNSET
        if not isinstance(self.end_time, Unset):
            end_time = self.end_time.isoformat()

        restrict_to_domain = self.restrict_to_domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if response_body_plain_text is not UNSET:
            field_dict["responseBodyPlainText"] = response_body_plain_text
        if response_subject is not UNSET:
            field_dict["responseSubject"] = response_subject
        if enable_auto_reply is not UNSET:
            field_dict["enableAutoReply"] = enable_auto_reply
        if restrict_to_contacts is not UNSET:
            field_dict["restrictToContacts"] = restrict_to_contacts
        if start_time is not UNSET:
            field_dict["startTime"] = start_time
        if end_time is not UNSET:
            field_dict["endTime"] = end_time
        if restrict_to_domain is not UNSET:
            field_dict["restrictToDomain"] = restrict_to_domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        response_body_plain_text = d.pop("responseBodyPlainText", UNSET)

        response_subject = d.pop("responseSubject", UNSET)

        enable_auto_reply = d.pop("enableAutoReply", UNSET)

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

        restrict_to_domain = d.pop("restrictToDomain", UNSET)

        turn_on_automatic_replies_response = cls(
            response_body_plain_text=response_body_plain_text,
            response_subject=response_subject,
            enable_auto_reply=enable_auto_reply,
            restrict_to_contacts=restrict_to_contacts,
            start_time=start_time,
            end_time=end_time,
            restrict_to_domain=restrict_to_domain,
        )

        turn_on_automatic_replies_response.additional_properties = d
        return turn_on_automatic_replies_response

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
