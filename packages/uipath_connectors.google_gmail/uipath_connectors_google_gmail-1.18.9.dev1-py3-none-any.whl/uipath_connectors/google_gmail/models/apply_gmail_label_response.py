from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="ApplyGmailLabelResponse")


@_attrs_define
class ApplyGmailLabelResponse:
    """
    Attributes:
        thread_id (Union[Unset, str]): Unique identifier for the email thread. Example: 19488b1d21aed8cf.
        snippet (Union[Unset, str]): A short preview of the email content.
        history_id (Union[Unset, str]): Unique identifier for the change history of the email. Example: 99320.
        label_ids (Union[Unset, list[str]]):  Example: UNREAD.
        id (Union[Unset, str]): A unique identifier for the email message. Example: 19488b1fa00ba1a8.
        size_estimate (Union[Unset, int]): An estimate of the email message size in bytes. Example: 557.0.
        internal_date (Union[Unset, str]): The date and time when the email was received by Gmail. Example:
            1737460152000.
    """

    thread_id: Union[Unset, str] = UNSET
    snippet: Union[Unset, str] = UNSET
    history_id: Union[Unset, str] = UNSET
    label_ids: Union[Unset, list[str]] = UNSET
    id: Union[Unset, str] = UNSET
    size_estimate: Union[Unset, int] = UNSET
    internal_date: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thread_id = self.thread_id

        snippet = self.snippet

        history_id = self.history_id

        label_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.label_ids, Unset):
            label_ids = self.label_ids

        id = self.id

        size_estimate = self.size_estimate

        internal_date = self.internal_date

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if snippet is not UNSET:
            field_dict["snippet"] = snippet
        if history_id is not UNSET:
            field_dict["historyId"] = history_id
        if label_ids is not UNSET:
            field_dict["labelIds"] = label_ids
        if id is not UNSET:
            field_dict["id"] = id
        if size_estimate is not UNSET:
            field_dict["sizeEstimate"] = size_estimate
        if internal_date is not UNSET:
            field_dict["internalDate"] = internal_date

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        thread_id = d.pop("threadId", UNSET)

        snippet = d.pop("snippet", UNSET)

        history_id = d.pop("historyId", UNSET)

        label_ids = cast(list[str], d.pop("labelIds", UNSET))

        id = d.pop("id", UNSET)

        size_estimate = d.pop("sizeEstimate", UNSET)

        internal_date = d.pop("internalDate", UNSET)

        apply_gmail_label_response = cls(
            thread_id=thread_id,
            snippet=snippet,
            history_id=history_id,
            label_ids=label_ids,
            id=id,
            size_estimate=size_estimate,
            internal_date=internal_date,
        )

        apply_gmail_label_response.additional_properties = d
        return apply_gmail_label_response

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
