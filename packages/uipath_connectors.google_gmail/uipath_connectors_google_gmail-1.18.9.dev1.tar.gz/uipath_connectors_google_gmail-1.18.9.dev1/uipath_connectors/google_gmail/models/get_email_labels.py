from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetEmailLabels")


@_attrs_define
class GetEmailLabels:
    """
    Attributes:
        display_name (Union[Unset, str]): The name of the folder as shown in the user interface. Example: INBOX.
        id (Union[Unset, str]): The unique identifier for the folder. Example: CHAT.
        is_folder (Union[Unset, bool]): A boolean flag to determine if the item is a folder or not. Example: True.
        label_list_visibility (Union[Unset, str]): Indicates if the label is visible in the label list. Example:
            labelShow.
        message_list_visibility (Union[Unset, str]): Indicates if messages are visible in the folder's message list.
            Example: show.
        name (Union[Unset, str]): The unique identifier name of the folder used by the system. Example: INBOX.
        parent_reference (Union[Unset, str]): A reference identifier for the parent folder, if any.
        type_ (Union[Unset, str]): The type of the folder, such as inbox, sent, etc. Example: system.
    """

    display_name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    is_folder: Union[Unset, bool] = UNSET
    label_list_visibility: Union[Unset, str] = UNSET
    message_list_visibility: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    parent_reference: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        id = self.id

        is_folder = self.is_folder

        label_list_visibility = self.label_list_visibility

        message_list_visibility = self.message_list_visibility

        name = self.name

        parent_reference = self.parent_reference

        type_ = self.type_

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if id is not UNSET:
            field_dict["id"] = id
        if is_folder is not UNSET:
            field_dict["isFolder"] = is_folder
        if label_list_visibility is not UNSET:
            field_dict["labelListVisibility"] = label_list_visibility
        if message_list_visibility is not UNSET:
            field_dict["messageListVisibility"] = message_list_visibility
        if name is not UNSET:
            field_dict["name"] = name
        if parent_reference is not UNSET:
            field_dict["parentReference"] = parent_reference
        if type_ is not UNSET:
            field_dict["type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        display_name = d.pop("displayName", UNSET)

        id = d.pop("id", UNSET)

        is_folder = d.pop("isFolder", UNSET)

        label_list_visibility = d.pop("labelListVisibility", UNSET)

        message_list_visibility = d.pop("messageListVisibility", UNSET)

        name = d.pop("name", UNSET)

        parent_reference = d.pop("parentReference", UNSET)

        type_ = d.pop("type", UNSET)

        get_email_labels = cls(
            display_name=display_name,
            id=id,
            is_folder=is_folder,
            label_list_visibility=label_list_visibility,
            message_list_visibility=message_list_visibility,
            name=name,
            parent_reference=parent_reference,
            type_=type_,
        )

        get_email_labels.additional_properties = d
        return get_email_labels

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
