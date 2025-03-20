from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetSingleLabelByIDResponse")


@_attrs_define
class GetSingleLabelByIDResponse:
    """
    Attributes:
        display_name (Union[Unset, str]): The name of the folder as shown in the user interface. Example: INBOX.
        id (Union[Unset, str]): The unique identifier for the folder. Example: CHAT.
        label_list_visibility (Union[Unset, str]): Indicates if the label is visible in the label list. Example:
            labelShow.
        message_list_visibility (Union[Unset, str]): Indicates if messages are visible in the folder's message list.
            Example: show.
        name (Union[Unset, str]): The unique identifier name of the folder used by the system. Example: INBOX.
        type_ (Union[Unset, str]): The type of the folder, such as inbox, sent, etc. Example: system.
        messages_total (Union[Unset, int]): The total count of messages within the folder. Example: 3202.0.
        messages_unread (Union[Unset, int]): The total number of unread messages within the folder. Example: 3079.0.
        threads_unread (Union[Unset, int]): The total number of unread conversation threads within the folder. Example:
            3031.0.
        threads_total (Union[Unset, int]): The total count of email threads within the folder. Example: 3136.0.
    """

    display_name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    label_list_visibility: Union[Unset, str] = UNSET
    message_list_visibility: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    type_: Union[Unset, str] = UNSET
    messages_total: Union[Unset, int] = UNSET
    messages_unread: Union[Unset, int] = UNSET
    threads_unread: Union[Unset, int] = UNSET
    threads_total: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        display_name = self.display_name

        id = self.id

        label_list_visibility = self.label_list_visibility

        message_list_visibility = self.message_list_visibility

        name = self.name

        type_ = self.type_

        messages_total = self.messages_total

        messages_unread = self.messages_unread

        threads_unread = self.threads_unread

        threads_total = self.threads_total

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if id is not UNSET:
            field_dict["id"] = id
        if label_list_visibility is not UNSET:
            field_dict["labelListVisibility"] = label_list_visibility
        if message_list_visibility is not UNSET:
            field_dict["messageListVisibility"] = message_list_visibility
        if name is not UNSET:
            field_dict["name"] = name
        if type_ is not UNSET:
            field_dict["type"] = type_
        if messages_total is not UNSET:
            field_dict["messagesTotal"] = messages_total
        if messages_unread is not UNSET:
            field_dict["messagesUnread"] = messages_unread
        if threads_unread is not UNSET:
            field_dict["threadsUnread"] = threads_unread
        if threads_total is not UNSET:
            field_dict["threadsTotal"] = threads_total

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        display_name = d.pop("displayName", UNSET)

        id = d.pop("id", UNSET)

        label_list_visibility = d.pop("labelListVisibility", UNSET)

        message_list_visibility = d.pop("messageListVisibility", UNSET)

        name = d.pop("name", UNSET)

        type_ = d.pop("type", UNSET)

        messages_total = d.pop("messagesTotal", UNSET)

        messages_unread = d.pop("messagesUnread", UNSET)

        threads_unread = d.pop("threadsUnread", UNSET)

        threads_total = d.pop("threadsTotal", UNSET)

        get_single_label_by_id_response = cls(
            display_name=display_name,
            id=id,
            label_list_visibility=label_list_visibility,
            message_list_visibility=message_list_visibility,
            name=name,
            type_=type_,
            messages_total=messages_total,
            messages_unread=messages_unread,
            threads_unread=threads_unread,
            threads_total=threads_total,
        )

        get_single_label_by_id_response.additional_properties = d
        return get_single_label_by_id_response

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
