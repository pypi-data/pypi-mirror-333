from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.list_email_categories_array_item_ref_category_id import (
    ListEmailCategoriesArrayItemRefCategoryId,
)
from ..models.list_email_categories_array_item_ref_category_name import (
    ListEmailCategoriesArrayItemRefCategoryName,
)
from typing import Union


T = TypeVar("T", bound="ListEmailCategoriesArrayItemRef")


@_attrs_define
class ListEmailCategoriesArrayItemRef:
    """
    Attributes:
        id (Union[Unset, ListEmailCategoriesArrayItemRefCategoryId]):  Example: id123.
        name (Union[Unset, ListEmailCategoriesArrayItemRefCategoryName]):  Example: INBOX.
    """

    id: Union[Unset, ListEmailCategoriesArrayItemRefCategoryId] = UNSET
    name: Union[Unset, ListEmailCategoriesArrayItemRefCategoryName] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id: Union[Unset, str] = UNSET
        if not isinstance(self.id, Unset):
            id = self.id.value

        name: Union[Unset, str] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["ID"] = id
        if name is not UNSET:
            field_dict["Name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        _id = d.pop("ID", UNSET)
        id: Union[Unset, ListEmailCategoriesArrayItemRefCategoryId]
        if isinstance(_id, Unset):
            id = UNSET
        else:
            id = ListEmailCategoriesArrayItemRefCategoryId(_id)

        _name = d.pop("Name", UNSET)
        name: Union[Unset, ListEmailCategoriesArrayItemRefCategoryName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = ListEmailCategoriesArrayItemRefCategoryName(_name)

        list_email_categories_array_item_ref = cls(
            id=id,
            name=name,
        )

        list_email_categories_array_item_ref.additional_properties = d
        return list_email_categories_array_item_ref

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
