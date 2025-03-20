from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="TurnOffAutomaticRepliesResponse")


@_attrs_define
class TurnOffAutomaticRepliesResponse:
    """
    Attributes:
        response_subject (Union[Unset, str]): The subject line used in automatic reply emails.
        enable_auto_reply (Union[Unset, bool]): Indicates if automatic replies are currently enabled.
        restrict_to_contacts (Union[Unset, bool]): Limits automatic replies to only your contacts.
        restrict_to_domain (Union[Unset, bool]): Limits automatic replies to recipients within your domain.
    """

    response_subject: Union[Unset, str] = UNSET
    enable_auto_reply: Union[Unset, bool] = UNSET
    restrict_to_contacts: Union[Unset, bool] = UNSET
    restrict_to_domain: Union[Unset, bool] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response_subject = self.response_subject

        enable_auto_reply = self.enable_auto_reply

        restrict_to_contacts = self.restrict_to_contacts

        restrict_to_domain = self.restrict_to_domain

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if response_subject is not UNSET:
            field_dict["responseSubject"] = response_subject
        if enable_auto_reply is not UNSET:
            field_dict["enableAutoReply"] = enable_auto_reply
        if restrict_to_contacts is not UNSET:
            field_dict["restrictToContacts"] = restrict_to_contacts
        if restrict_to_domain is not UNSET:
            field_dict["restrictToDomain"] = restrict_to_domain

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        response_subject = d.pop("responseSubject", UNSET)

        enable_auto_reply = d.pop("enableAutoReply", UNSET)

        restrict_to_contacts = d.pop("restrictToContacts", UNSET)

        restrict_to_domain = d.pop("restrictToDomain", UNSET)

        turn_off_automatic_replies_response = cls(
            response_subject=response_subject,
            enable_auto_reply=enable_auto_reply,
            restrict_to_contacts=restrict_to_contacts,
            restrict_to_domain=restrict_to_domain,
        )

        turn_off_automatic_replies_response.additional_properties = d
        return turn_off_automatic_replies_response

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
