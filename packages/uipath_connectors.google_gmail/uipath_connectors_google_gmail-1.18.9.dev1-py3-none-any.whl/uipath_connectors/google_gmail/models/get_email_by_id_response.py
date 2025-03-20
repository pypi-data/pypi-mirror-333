from typing import Any, TypeVar, TYPE_CHECKING

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from dateutil.parser import isoparse
from typing import cast
from typing import Union
import datetime

if TYPE_CHECKING:
    from ..models.get_email_by_id_response_payload import GetEmailByIDResponsePayload


T = TypeVar("T", bound="GetEmailByIDResponse")


@_attrs_define
class GetEmailByIDResponse:
    """
    Attributes:
        history_id (Union[Unset, str]):
        id (Union[Unset, str]):
        internal_date (Union[Unset, datetime.datetime]):
        label_ids (Union[Unset, list[str]]):
        payload (Union[Unset, GetEmailByIDResponsePayload]):
        raw (Union[Unset, str]):
        size_estimate (Union[Unset, int]):
        snippet (Union[Unset, str]):
        thread_id (Union[Unset, str]):
    """

    history_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    internal_date: Union[Unset, datetime.datetime] = UNSET
    label_ids: Union[Unset, list[str]] = UNSET
    payload: Union[Unset, "GetEmailByIDResponsePayload"] = UNSET
    raw: Union[Unset, str] = UNSET
    size_estimate: Union[Unset, int] = UNSET
    snippet: Union[Unset, str] = UNSET
    thread_id: Union[Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:

        history_id = self.history_id

        id = self.id

        internal_date: Union[Unset, str] = UNSET
        if not isinstance(self.internal_date, Unset):
            internal_date = self.internal_date.isoformat()

        label_ids: Union[Unset, list[str]] = UNSET
        if not isinstance(self.label_ids, Unset):
            label_ids = self.label_ids

        payload: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.payload, Unset):
            payload = self.payload.to_dict()

        raw = self.raw

        size_estimate = self.size_estimate

        snippet = self.snippet

        thread_id = self.thread_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if history_id is not UNSET:
            field_dict["historyId"] = history_id
        if id is not UNSET:
            field_dict["id"] = id
        if internal_date is not UNSET:
            field_dict["internalDate"] = internal_date
        if label_ids is not UNSET:
            field_dict["labelIds"] = label_ids
        if payload is not UNSET:
            field_dict["payload"] = payload
        if raw is not UNSET:
            field_dict["raw"] = raw
        if size_estimate is not UNSET:
            field_dict["sizeEstimate"] = size_estimate
        if snippet is not UNSET:
            field_dict["snippet"] = snippet
        if thread_id is not UNSET:
            field_dict["threadId"] = thread_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        from ..models.get_email_by_id_response_payload import (
            GetEmailByIDResponsePayload,
        )

        d = src_dict.copy()
        history_id = d.pop("historyId", UNSET)

        id = d.pop("id", UNSET)

        _internal_date = d.pop("internalDate", UNSET)
        internal_date: Union[Unset, datetime.datetime]
        if isinstance(_internal_date, Unset):
            internal_date = UNSET
        else:
            internal_date = isoparse(_internal_date)

        label_ids = cast(list[str], d.pop("labelIds", UNSET))

        _payload = d.pop("payload", UNSET)
        payload: Union[Unset, GetEmailByIDResponsePayload]
        if isinstance(_payload, Unset):
            payload = UNSET
        else:
            payload = GetEmailByIDResponsePayload.from_dict(_payload)

        raw = d.pop("raw", UNSET)

        size_estimate = d.pop("sizeEstimate", UNSET)

        snippet = d.pop("snippet", UNSET)

        thread_id = d.pop("threadId", UNSET)

        get_email_by_id_response = cls(
            history_id=history_id,
            id=id,
            internal_date=internal_date,
            label_ids=label_ids,
            payload=payload,
            raw=raw,
            size_estimate=size_estimate,
            snippet=snippet,
            thread_id=thread_id,
        )

        get_email_by_id_response.additional_properties = d
        return get_email_by_id_response

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
