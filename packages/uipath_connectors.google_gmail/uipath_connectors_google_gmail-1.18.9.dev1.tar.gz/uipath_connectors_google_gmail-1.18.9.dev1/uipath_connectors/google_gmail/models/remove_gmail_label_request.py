from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast
from typing import Union


T = TypeVar("T", bound="RemoveGmailLabelRequest")


@_attrs_define
class RemoveGmailLabelRequest:
    """
    Attributes:
        remove_label_ids (Union[Unset, list[str]]):
    """

    remove_label_ids: Union[Unset, list[str]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        remove_label_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.remove_label_ids, Unset):
            remove_label_ids = self.remove_label_ids

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if remove_label_ids is not UNSET:
            field_dict["removeLabelIds"] = remove_label_ids

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        remove_label_ids = cast(list[str], d.pop("removeLabelIds", UNSET))

        remove_gmail_label_request = cls(
            remove_label_ids=remove_label_ids,
        )

        remove_gmail_label_request.additional_properties = d
        return remove_gmail_label_request

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
