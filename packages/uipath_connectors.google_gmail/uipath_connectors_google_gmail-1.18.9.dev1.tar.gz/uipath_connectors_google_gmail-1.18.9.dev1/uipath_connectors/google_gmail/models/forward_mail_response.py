from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="ForwardMailResponse")


@_attrs_define
class ForwardMailResponse:
    """
    Attributes:
        thread_id (Union[Unset, str]): A unique identifier for the email thread. Example: 19468958b5e51c05.
        label_ids (Union[Unset, list[str]]):  Example: SENT.
        id (Union[Unset, str]): A unique identifier for the specific email message. Example: 19468958b5e51c05.
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

        forward_mail_response = cls(
            thread_id=thread_id,
            label_ids=label_ids,
            id=id,
        )

        forward_mail_response.additional_properties = d
        return forward_mail_response

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
