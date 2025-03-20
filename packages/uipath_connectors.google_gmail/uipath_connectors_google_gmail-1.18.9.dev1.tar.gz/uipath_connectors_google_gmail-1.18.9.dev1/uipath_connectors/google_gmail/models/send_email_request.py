from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.send_email_request_importance import SendEmailRequestImportance
from typing import Union


T = TypeVar("T", bound="SendEmailRequest")


@_attrs_define
class SendEmailRequest:
    """
    Attributes:
        body (str): Body of email Example: string.
        to (str): The primary recipients of email, separated by comma (,) Example: string.
        bcc (Union[Unset, str]): The hidden recipients of the email, separated by comma (,) Example: string.
        cc (Union[Unset, str]): The secondary recipients of the email, separated by comma (,) Example: string.
        importance (Union[Unset, SendEmailRequestImportance]): Importance Example: string.
        reply_to (Union[Unset, str]): The email addresses to use when replying, separated by comma (,) Example: string.
        subject (Union[Unset, str]): The subject of email Example: string.
    """

    body: str
    to: str
    bcc: Union[Unset, str] = UNSET
    cc: Union[Unset, str] = UNSET
    importance: Union[Unset, SendEmailRequestImportance] = UNSET
    reply_to: Union[Unset, str] = UNSET
    subject: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        to = self.to

        bcc = self.bcc

        cc = self.cc

        importance: Union[Unset, str] = UNSET
        if not isinstance(self.importance, Unset):
            importance = self.importance.value

        reply_to = self.reply_to

        subject = self.subject

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "Body": body,
                "To": to,
            }
        )
        if bcc is not UNSET:
            field_dict["BCC"] = bcc
        if cc is not UNSET:
            field_dict["CC"] = cc
        if importance is not UNSET:
            field_dict["Importance"] = importance
        if reply_to is not UNSET:
            field_dict["ReplyTo"] = reply_to
        if subject is not UNSET:
            field_dict["Subject"] = subject

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("Body")

        to = d.pop("To")

        bcc = d.pop("BCC", UNSET)

        cc = d.pop("CC", UNSET)

        _importance = d.pop("Importance", UNSET)
        importance: Union[Unset, SendEmailRequestImportance]
        if isinstance(_importance, Unset):
            importance = UNSET
        else:
            importance = SendEmailRequestImportance(_importance)

        reply_to = d.pop("ReplyTo", UNSET)

        subject = d.pop("Subject", UNSET)

        send_email_request = cls(
            body=body,
            to=to,
            bcc=bcc,
            cc=cc,
            importance=importance,
            reply_to=reply_to,
            subject=subject,
        )

        send_email_request.additional_properties = d
        return send_email_request

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
