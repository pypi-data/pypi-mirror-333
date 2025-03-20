from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.list_email_type import ListEmailType
from typing import Union

if TYPE_CHECKING:
    from ..models.list_email_parent_folders_array_item_ref import (
        ListEmailParentFoldersArrayItemRef,
    )
    from ..models.list_email_to_array_item_ref import ListEmailToArrayItemRef
    from ..models.list_email_from import ListEmailFrom
    from ..models.list_email_cc_array_item_ref import ListEmailCCArrayItemRef
    from ..models.list_email_categories_array_item_ref import (
        ListEmailCategoriesArrayItemRef,
    )
    from ..models.list_email_bcc_array_item_ref import ListEmailBCCArrayItemRef


T = TypeVar("T", bound="ListEmail")


@_attrs_define
class ListEmail:
    """
    Attributes:
        id (Union[Unset, str]):  Example: 184e63ea8560e37d.
        thread_id (Union[Unset, str]):  Example: 184e63ea8560e37d.
        from_ (Union[Unset, ListEmailFrom]):
        to (Union[Unset, list['ListEmailToArrayItemRef']]):
        subject (Union[Unset, str]):  Example: Test email with attachment.
        cc (Union[Unset, list['ListEmailCCArrayItemRef']]):
        bcc (Union[Unset, list['ListEmailBCCArrayItemRef']]):
        has_attachments (Union[Unset, bool]):  Example: true.
        parent_folders (Union[Unset, list['ListEmailParentFoldersArrayItemRef']]):
        categories (Union[Unset, list['ListEmailCategoriesArrayItemRef']]):
        type_ (Union[Unset, ListEmailType]):  Example: email.
    """

    id: Union[Unset, str] = UNSET
    thread_id: Union[Unset, str] = UNSET
    from_: Union[Unset, "ListEmailFrom"] = UNSET
    to: Union[Unset, list["ListEmailToArrayItemRef"]] = UNSET
    subject: Union[Unset, str] = UNSET
    cc: Union[Unset, list["ListEmailCCArrayItemRef"]] = UNSET
    bcc: Union[Unset, list["ListEmailBCCArrayItemRef"]] = UNSET
    has_attachments: Union[Unset, bool] = UNSET
    parent_folders: Union[Unset, list["ListEmailParentFoldersArrayItemRef"]] = UNSET
    categories: Union[Unset, list["ListEmailCategoriesArrayItemRef"]] = UNSET
    type_: Union[Unset, ListEmailType] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        id = self.id

        thread_id = self.thread_id

        from_: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_.to_dict()

        to: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.to, Unset):
            to = []
            for componentsschemas_list_email_to_item_data in self.to:
                componentsschemas_list_email_to_item = (
                    componentsschemas_list_email_to_item_data.to_dict()
                )
                to.append(componentsschemas_list_email_to_item)

        subject = self.subject

        cc: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.cc, Unset):
            cc = []
            for componentsschemas_list_email_cc_item_data in self.cc:
                componentsschemas_list_email_cc_item = (
                    componentsschemas_list_email_cc_item_data.to_dict()
                )
                cc.append(componentsschemas_list_email_cc_item)

        bcc: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.bcc, Unset):
            bcc = []
            for componentsschemas_list_email_bcc_item_data in self.bcc:
                componentsschemas_list_email_bcc_item = (
                    componentsschemas_list_email_bcc_item_data.to_dict()
                )
                bcc.append(componentsschemas_list_email_bcc_item)

        has_attachments = self.has_attachments

        parent_folders: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parent_folders, Unset):
            parent_folders = []
            for (
                componentsschemas_list_email_parent_folders_item_data
            ) in self.parent_folders:
                componentsschemas_list_email_parent_folders_item = (
                    componentsschemas_list_email_parent_folders_item_data.to_dict()
                )
                parent_folders.append(componentsschemas_list_email_parent_folders_item)

        categories: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.categories, Unset):
            categories = []
            for componentsschemas_list_email_categories_item_data in self.categories:
                componentsschemas_list_email_categories_item = (
                    componentsschemas_list_email_categories_item_data.to_dict()
                )
                categories.append(componentsschemas_list_email_categories_item)

        type_: Union[Unset, str] = UNSET
        if not isinstance(self.type_, Unset):
            type_ = self.type_.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if id is not UNSET:
            field_dict["ID"] = id
        if thread_id is not UNSET:
            field_dict["ThreadID"] = thread_id
        if from_ is not UNSET:
            field_dict["From"] = from_
        if to is not UNSET:
            field_dict["To"] = to
        if subject is not UNSET:
            field_dict["Subject"] = subject
        if cc is not UNSET:
            field_dict["CC"] = cc
        if bcc is not UNSET:
            field_dict["BCC"] = bcc
        if has_attachments is not UNSET:
            field_dict["HasAttachments"] = has_attachments
        if parent_folders is not UNSET:
            field_dict["ParentFolders"] = parent_folders
        if categories is not UNSET:
            field_dict["Categories"] = categories
        if type_ is not UNSET:
            field_dict["Type"] = type_

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.list_email_parent_folders_array_item_ref import (
            ListEmailParentFoldersArrayItemRef,
        )
        from ..models.list_email_to_array_item_ref import ListEmailToArrayItemRef
        from ..models.list_email_from import ListEmailFrom
        from ..models.list_email_cc_array_item_ref import ListEmailCCArrayItemRef
        from ..models.list_email_categories_array_item_ref import (
            ListEmailCategoriesArrayItemRef,
        )
        from ..models.list_email_bcc_array_item_ref import ListEmailBCCArrayItemRef

        d = src_dict.copy()
        id = d.pop("ID", UNSET)

        thread_id = d.pop("ThreadID", UNSET)

        _from_ = d.pop("From", UNSET)
        from_: Union[Unset, ListEmailFrom]
        if isinstance(_from_, Unset):
            from_ = UNSET
        else:
            from_ = ListEmailFrom.from_dict(_from_)

        to = []
        _to = d.pop("To", UNSET)
        for componentsschemas_list_email_to_item_data in _to or []:
            componentsschemas_list_email_to_item = ListEmailToArrayItemRef.from_dict(
                componentsschemas_list_email_to_item_data
            )

            to.append(componentsschemas_list_email_to_item)

        subject = d.pop("Subject", UNSET)

        cc = []
        _cc = d.pop("CC", UNSET)
        for componentsschemas_list_email_cc_item_data in _cc or []:
            componentsschemas_list_email_cc_item = ListEmailCCArrayItemRef.from_dict(
                componentsschemas_list_email_cc_item_data
            )

            cc.append(componentsschemas_list_email_cc_item)

        bcc = []
        _bcc = d.pop("BCC", UNSET)
        for componentsschemas_list_email_bcc_item_data in _bcc or []:
            componentsschemas_list_email_bcc_item = ListEmailBCCArrayItemRef.from_dict(
                componentsschemas_list_email_bcc_item_data
            )

            bcc.append(componentsschemas_list_email_bcc_item)

        has_attachments = d.pop("HasAttachments", UNSET)

        parent_folders = []
        _parent_folders = d.pop("ParentFolders", UNSET)
        for componentsschemas_list_email_parent_folders_item_data in (
            _parent_folders or []
        ):
            componentsschemas_list_email_parent_folders_item = (
                ListEmailParentFoldersArrayItemRef.from_dict(
                    componentsschemas_list_email_parent_folders_item_data
                )
            )

            parent_folders.append(componentsschemas_list_email_parent_folders_item)

        categories = []
        _categories = d.pop("Categories", UNSET)
        for componentsschemas_list_email_categories_item_data in _categories or []:
            componentsschemas_list_email_categories_item = (
                ListEmailCategoriesArrayItemRef.from_dict(
                    componentsschemas_list_email_categories_item_data
                )
            )

            categories.append(componentsschemas_list_email_categories_item)

        _type_ = d.pop("Type", UNSET)
        type_: Union[Unset, ListEmailType]
        if isinstance(_type_, Unset):
            type_ = UNSET
        else:
            type_ = ListEmailType(_type_)

        list_email = cls(
            id=id,
            thread_id=thread_id,
            from_=from_,
            to=to,
            subject=subject,
            cc=cc,
            bcc=bcc,
            has_attachments=has_attachments,
            parent_folders=parent_folders,
            categories=categories,
            type_=type_,
        )

        list_email.additional_properties = d
        return list_email

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
