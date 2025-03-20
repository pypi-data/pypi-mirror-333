from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.reply_to_email_response_importance import ReplyToEmailResponseImportance
from typing import cast
from typing import Union


T = TypeVar("T", bound="ReplyToEmailResponse")


@_attrs_define
class ReplyToEmailResponse:
    """
    Attributes:
        body (Union[Unset, str]): Body Example: string.
        importance (Union[Unset, ReplyToEmailResponseImportance]): Importance of email Example: string.
        reply_to (Union[Unset, str]): The email message to reply to Example: string.
        id (Union[Unset, str]):  Example: 18572a181dfd50a3.
        label_ids (Union[Unset, list[str]]):  Example: ['SENT'].
        thread_id (Union[Unset, str]):  Example: 18572a181dfd50a3.
    """

    body: Union[Unset, str] = UNSET
    importance: Union[Unset, ReplyToEmailResponseImportance] = UNSET
    reply_to: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    label_ids: Union[Unset, list[str]] = UNSET
    thread_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        body = self.body

        importance: Union[Unset, str] = UNSET
        if not isinstance(self.importance, Unset):
            importance = self.importance.value

        reply_to = self.reply_to

        id = self.id

        label_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.label_ids, Unset):
            label_ids = self.label_ids

        thread_id = self.thread_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["Body"] = body
        if importance is not UNSET:
            field_dict["Importance"] = importance
        if reply_to is not UNSET:
            field_dict["ReplyTo"] = reply_to
        if id is not UNSET:
            field_dict["id"] = id
        if label_ids is not UNSET:
            field_dict["labelIds"] = label_ids
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        body = d.pop("Body", UNSET)

        _importance = d.pop("Importance", UNSET)
        importance: Union[Unset, ReplyToEmailResponseImportance]
        if isinstance(_importance, Unset):
            importance = UNSET
        else:
            importance = ReplyToEmailResponseImportance(_importance)

        reply_to = d.pop("ReplyTo", UNSET)

        id = d.pop("id", UNSET)

        label_ids = cast(list[str], d.pop("labelIds", UNSET))

        thread_id = d.pop("threadId", UNSET)

        reply_to_email_response = cls(
            body=body,
            importance=importance,
            reply_to=reply_to,
            id=id,
            label_ids=label_ids,
            thread_id=thread_id,
        )

        reply_to_email_response.additional_properties = d
        return reply_to_email_response

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
