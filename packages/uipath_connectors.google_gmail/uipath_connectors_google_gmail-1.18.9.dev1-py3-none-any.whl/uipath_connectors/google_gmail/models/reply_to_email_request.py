from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reply_to_email_request_importance import ReplyToEmailRequestImportance
from typing import Union


T = TypeVar("T", bound="ReplyToEmailRequest")


@_attrs_define
class ReplyToEmailRequest:
    """
    Attributes:
        reply_to (str): The email message to reply to Example: string.
        bcc (Union[Unset, str]):  Example: string.
        body (Union[Unset, str]): Body Example: string.
        cc (Union[Unset, str]):  Example: string.
        importance (Union[Unset, ReplyToEmailRequestImportance]): Importance of email Example: string.
        subject (Union[Unset, str]):  Example: string.
        to (Union[Unset, str]):  Example: string.
        thread_id (Union[Unset, str]):  Example: 18572a181dfd50a3.
        reply_to_all (Union[Unset, bool]): Reply to all
    """

    reply_to: str
    bcc: Union[Unset, str] = UNSET
    body: Union[Unset, str] = UNSET
    cc: Union[Unset, str] = UNSET
    importance: Union[Unset, ReplyToEmailRequestImportance] = UNSET
    subject: Union[Unset, str] = UNSET
    to: Union[Unset, str] = UNSET
    thread_id: Union[Unset, str] = UNSET
    reply_to_all: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        reply_to = self.reply_to

        bcc = self.bcc

        body = self.body

        cc = self.cc

        importance: Union[Unset, str] = UNSET
        if not isinstance(self.importance, Unset):
            importance = self.importance.value

        subject = self.subject

        to = self.to

        thread_id = self.thread_id

        reply_to_all = self.reply_to_all

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "ReplyTo": reply_to,
            }
        )
        if bcc is not UNSET:
            field_dict["BCC"] = bcc
        if body is not UNSET:
            field_dict["Body"] = body
        if cc is not UNSET:
            field_dict["CC"] = cc
        if importance is not UNSET:
            field_dict["Importance"] = importance
        if subject is not UNSET:
            field_dict["Subject"] = subject
        if to is not UNSET:
            field_dict["To"] = to
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if reply_to_all is not UNSET:
            field_dict["ReplyToAll"] = reply_to_all

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        reply_to = d.pop("ReplyTo")

        bcc = d.pop("BCC", UNSET)

        body = d.pop("Body", UNSET)

        cc = d.pop("CC", UNSET)

        _importance = d.pop("Importance", UNSET)
        importance: Union[Unset, ReplyToEmailRequestImportance]
        if isinstance(_importance, Unset):
            importance = UNSET
        else:
            importance = ReplyToEmailRequestImportance(_importance)

        subject = d.pop("Subject", UNSET)

        to = d.pop("To", UNSET)

        thread_id = d.pop("threadId", UNSET)

        reply_to_all = d.pop("ReplyToAll", UNSET)

        reply_to_email_request = cls(
            reply_to=reply_to,
            bcc=bcc,
            body=body,
            cc=cc,
            importance=importance,
            subject=subject,
            to=to,
            thread_id=thread_id,
            reply_to_all=reply_to_all,
        )

        reply_to_email_request.additional_properties = d
        return reply_to_email_request

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
