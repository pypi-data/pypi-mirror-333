from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.send_email_response_importance import SendEmailResponseImportance
from typing import cast
from typing import Union


T = TypeVar("T", bound="SendEmailResponse")


@_attrs_define
class SendEmailResponse:
    """
    Attributes:
        importance (Union[Unset, SendEmailResponseImportance]): Importance Example: string.
        id (Union[Unset, str]):  Example: 18572a181dfd50a3.
        label_ids (Union[Unset, list[str]]):  Example: ['SENT'].
        thread_id (Union[Unset, str]):  Example: 18572a181dfd50a3.
    """

    importance: Union[Unset, SendEmailResponseImportance] = UNSET
    id: Union[Unset, str] = UNSET
    label_ids: Union[Unset, list[str]] = UNSET
    thread_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        importance: Union[Unset, str] = UNSET
        if not isinstance(self.importance, Unset):
            importance = self.importance.value

        id = self.id

        label_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.label_ids, Unset):
            label_ids = self.label_ids

        thread_id = self.thread_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if importance is not UNSET:
            field_dict["Importance"] = importance
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
        _importance = d.pop("Importance", UNSET)
        importance: Union[Unset, SendEmailResponseImportance]
        if isinstance(_importance, Unset):
            importance = UNSET
        else:
            importance = SendEmailResponseImportance(_importance)

        id = d.pop("id", UNSET)

        label_ids = cast(list[str], d.pop("labelIds", UNSET))

        thread_id = d.pop("threadId", UNSET)

        send_email_response = cls(
            importance=importance,
            id=id,
            label_ids=label_ids,
            thread_id=thread_id,
        )

        send_email_response.additional_properties = d
        return send_email_response

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
