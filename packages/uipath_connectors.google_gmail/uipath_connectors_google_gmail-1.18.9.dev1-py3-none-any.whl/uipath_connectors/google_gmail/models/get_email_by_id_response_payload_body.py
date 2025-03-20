from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetEmailByIDResponsePayloadBody")


@_attrs_define
class GetEmailByIDResponsePayloadBody:
    """
    Attributes:
        attachment_id (Union[Unset, str]):
        data (Union[Unset, str]):
        size (Union[Unset, int]):
    """

    attachment_id: Union[Unset, str] = UNSET
    data: Union[Unset, str] = UNSET
    size: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        attachment_id = self.attachment_id

        data = self.data

        size = self.size

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if attachment_id is not UNSET:
            field_dict["attachmentId"] = attachment_id
        if data is not UNSET:
            field_dict["data"] = data
        if size is not UNSET:
            field_dict["size"] = size

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        attachment_id = d.pop("attachmentId", UNSET)

        data = d.pop("data", UNSET)

        size = d.pop("size", UNSET)

        get_email_by_id_response_payload_body = cls(
            attachment_id=attachment_id,
            data=data,
            size=size,
        )

        get_email_by_id_response_payload_body.additional_properties = d
        return get_email_by_id_response_payload_body

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
