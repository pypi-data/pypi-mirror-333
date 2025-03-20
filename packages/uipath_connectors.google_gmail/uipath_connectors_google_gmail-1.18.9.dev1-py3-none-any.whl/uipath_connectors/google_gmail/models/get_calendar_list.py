from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union


T = TypeVar("T", bound="GetCalendarList")


@_attrs_define
class GetCalendarList:
    """
    Attributes:
        type_ (Union[Unset, str]): The Type Example: folder.
        is_folder (Union[Unset, bool]): The Is folder Example: True.
        time_zone (Union[Unset, str]): The Time zone Example: Asia/Kolkata.
        reference_id (Union[Unset, str]): The Reference ID Example: me.
        selectable (Union[Unset, bool]): The Selectable
        full_name (Union[Unset, str]): The Full name Example: My Calendars.
        id (Union[Unset, str]): The ID Example: me.
    """

    type_: Union[Unset, str] = UNSET
    is_folder: Union[Unset, bool] = UNSET
    time_zone: Union[Unset, str] = UNSET
    reference_id: Union[Unset, str] = UNSET
    selectable: Union[Unset, bool] = UNSET
    full_name: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        type_ = self.type_

        is_folder = self.is_folder

        time_zone = self.time_zone

        reference_id = self.reference_id

        selectable = self.selectable

        full_name = self.full_name

        id = self.id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if type_ is not UNSET:
            field_dict["Type"] = type_
        if is_folder is not UNSET:
            field_dict["isFolder"] = is_folder
        if time_zone is not UNSET:
            field_dict["TimeZone"] = time_zone
        if reference_id is not UNSET:
            field_dict["ReferenceID"] = reference_id
        if selectable is not UNSET:
            field_dict["Selectable"] = selectable
        if full_name is not UNSET:
            field_dict["FullName"] = full_name
        if id is not UNSET:
            field_dict["ID"] = id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        type_ = d.pop("Type", UNSET)

        is_folder = d.pop("isFolder", UNSET)

        time_zone = d.pop("TimeZone", UNSET)

        reference_id = d.pop("ReferenceID", UNSET)

        selectable = d.pop("Selectable", UNSET)

        full_name = d.pop("FullName", UNSET)

        id = d.pop("ID", UNSET)

        get_calendar_list = cls(
            type_=type_,
            is_folder=is_folder,
            time_zone=time_zone,
            reference_id=reference_id,
            selectable=selectable,
            full_name=full_name,
            id=id,
        )

        get_calendar_list.additional_properties = d
        return get_calendar_list

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
