from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field
import json

from ..types import UNSET, Unset

from ..types import File, FileJsonType
from io import BytesIO
from typing import Union

if TYPE_CHECKING:
    from ..models.reply_to_email_request import ReplyToEmailRequest


T = TypeVar("T", bound="ReplyToEmailBody")


@_attrs_define
class ReplyToEmailBody:
    """
    Attributes:
        body (ReplyToEmailRequest):
        file (Union[Unset, File]): Email attachment
    """

    body: "ReplyToEmailRequest"
    file: Union[Unset, File] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        body = self.body.to_dict()

        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "body": body,
            }
        )
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict

    def to_multipart(self) -> dict[str, Any]:
        body = (None, json.dumps(self.body.to_dict()).encode(), "application/json")

        file: Union[Unset, FileJsonType] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_tuple()

        field_dict: dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "body": body,
            }
        )
        if file is not UNSET:
            field_dict["file"] = file

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.reply_to_email_request import ReplyToEmailRequest

        d = src_dict.copy()
        body = ReplyToEmailRequest.from_dict(d.pop("body"))

        _file = d.pop("file", UNSET)
        file: Union[Unset, File]
        if isinstance(_file, Unset):
            file = UNSET
        else:
            file = File(payload=BytesIO(_file))

        reply_to_email_body = cls(
            body=body,
            file=file,
        )

        reply_to_email_body.additional_properties = d
        return reply_to_email_body

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
