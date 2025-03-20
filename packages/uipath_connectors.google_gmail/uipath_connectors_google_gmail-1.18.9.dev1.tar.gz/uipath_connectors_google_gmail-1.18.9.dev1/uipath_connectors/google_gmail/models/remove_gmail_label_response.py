from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="RemoveGmailLabelResponse")


@_attrs_define
class RemoveGmailLabelResponse:
    """
    Attributes:
        thread_id (Union[Unset, str]): Unique identifier for the email thread. Example: 19488b1d21aed8cf.
        label_ids (Union[Unset, list[str]]):  Example: IMPORTANT.
        id (Union[Unset, str]): Unique identifier for the specific email message. Example: 19488b1fa00ba1a8.
    """

    thread_id: Union[Unset, str] = UNSET
    label_ids: Union[Unset, list[str]] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        thread_id = self.thread_id

        label_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.label_ids, Unset):
            label_ids = self.label_ids

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id
        if label_ids is not UNSET:
            field_dict["labelIds"] = label_ids
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        thread_id = d.pop("threadId", UNSET)

        label_ids = cast(list[str], d.pop("labelIds", UNSET))

        id = d.pop("id", UNSET)

        remove_gmail_label_response = cls(
            thread_id=thread_id,
            label_ids=label_ids,
            id=id,
        )

        remove_gmail_label_response.additional_properties = d
        return remove_gmail_label_response

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
