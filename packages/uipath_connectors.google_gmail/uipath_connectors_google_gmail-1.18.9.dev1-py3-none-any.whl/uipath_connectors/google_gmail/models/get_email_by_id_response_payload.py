from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import Union

if TYPE_CHECKING:
    from ..models.get_email_by_id_response_payload_body import (
        GetEmailByIDResponsePayloadBody,
    )
    from ..models.get_email_by_id_response_payload_headers_array_item_ref import (
        GetEmailByIDResponsePayloadHeadersArrayItemRef,
    )
    from ..models.get_email_by_id_response_payload_parts_array_item_ref import (
        GetEmailByIDResponsePayloadPartsArrayItemRef,
    )


T = TypeVar("T", bound="GetEmailByIDResponsePayload")


@_attrs_define
class GetEmailByIDResponsePayload:
    """
    Attributes:
        body (Union[Unset, GetEmailByIDResponsePayloadBody]):
        filename (Union[Unset, str]):
        headers (Union[Unset, list['GetEmailByIDResponsePayloadHeadersArrayItemRef']]):
        mime_type (Union[Unset, str]):
        part_id (Union[Unset, str]):
        parts (Union[Unset, list['GetEmailByIDResponsePayloadPartsArrayItemRef']]):
    """

    body: Union[Unset, "GetEmailByIDResponsePayloadBody"] = UNSET
    filename: Union[Unset, str] = UNSET
    headers: Union[Unset, list["GetEmailByIDResponsePayloadHeadersArrayItemRef"]] = (
        UNSET
    )
    mime_type: Union[Unset, str] = UNSET
    part_id: Union[Unset, str] = UNSET
    parts: Union[Unset, list["GetEmailByIDResponsePayloadPartsArrayItemRef"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        body: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.body, Unset):
            body = self.body.to_dict()

        filename = self.filename

        headers: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.headers, Unset):
            headers = []
            for (
                componentsschemas_get_email_by_id_response_payload_headers_item_data
            ) in self.headers:
                componentsschemas_get_email_by_id_response_payload_headers_item = componentsschemas_get_email_by_id_response_payload_headers_item_data.to_dict()
                headers.append(
                    componentsschemas_get_email_by_id_response_payload_headers_item
                )

        mime_type = self.mime_type

        part_id = self.part_id

        parts: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.parts, Unset):
            parts = []
            for (
                componentsschemas_get_email_by_id_response_payload_parts_item_data
            ) in self.parts:
                componentsschemas_get_email_by_id_response_payload_parts_item = componentsschemas_get_email_by_id_response_payload_parts_item_data.to_dict()
                parts.append(
                    componentsschemas_get_email_by_id_response_payload_parts_item
                )

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if body is not UNSET:
            field_dict["body"] = body
        if filename is not UNSET:
            field_dict["filename"] = filename
        if headers is not UNSET:
            field_dict["headers"] = headers
        if mime_type is not UNSET:
            field_dict["mimeType"] = mime_type
        if part_id is not UNSET:
            field_dict["partId"] = part_id
        if parts is not UNSET:
            field_dict["parts"] = parts

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_email_by_id_response_payload_body import (
            GetEmailByIDResponsePayloadBody,
        )
        from ..models.get_email_by_id_response_payload_headers_array_item_ref import (
            GetEmailByIDResponsePayloadHeadersArrayItemRef,
        )
        from ..models.get_email_by_id_response_payload_parts_array_item_ref import (
            GetEmailByIDResponsePayloadPartsArrayItemRef,
        )

        d = src_dict.copy()
        _body = d.pop("body", UNSET)
        body: Union[Unset, GetEmailByIDResponsePayloadBody]
        if isinstance(_body, Unset):
            body = UNSET
        else:
            body = GetEmailByIDResponsePayloadBody.from_dict(_body)

        filename = d.pop("filename", UNSET)

        headers = []
        _headers = d.pop("headers", UNSET)
        for componentsschemas_get_email_by_id_response_payload_headers_item_data in (
            _headers or []
        ):
            componentsschemas_get_email_by_id_response_payload_headers_item = (
                GetEmailByIDResponsePayloadHeadersArrayItemRef.from_dict(
                    componentsschemas_get_email_by_id_response_payload_headers_item_data
                )
            )

            headers.append(
                componentsschemas_get_email_by_id_response_payload_headers_item
            )

        mime_type = d.pop("mimeType", UNSET)

        part_id = d.pop("partId", UNSET)

        parts = []
        _parts = d.pop("parts", UNSET)
        for componentsschemas_get_email_by_id_response_payload_parts_item_data in (
            _parts or []
        ):
            componentsschemas_get_email_by_id_response_payload_parts_item = (
                GetEmailByIDResponsePayloadPartsArrayItemRef.from_dict(
                    componentsschemas_get_email_by_id_response_payload_parts_item_data
                )
            )

            parts.append(componentsschemas_get_email_by_id_response_payload_parts_item)

        get_email_by_id_response_payload = cls(
            body=body,
            filename=filename,
            headers=headers,
            mime_type=mime_type,
            part_id=part_id,
            parts=parts,
        )

        get_email_by_id_response_payload.additional_properties = d
        return get_email_by_id_response_payload

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
