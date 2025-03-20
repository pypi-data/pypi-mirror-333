from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict



class ApplyGmailLabelResponse(BaseModel):
    """
    Attributes:
        thread_id (Optional[str]): Unique identifier for the email thread. Example: 19488b1d21aed8cf.
        snippet (Optional[str]): A short preview of the email content.
        history_id (Optional[str]): Unique identifier for the change history of the email. Example: 99320.
        label_ids (Optional[list[str]]):  Example: UNREAD.
        id (Optional[str]): A unique identifier for the email message. Example: 19488b1fa00ba1a8.
        size_estimate (Optional[int]): An estimate of the email message size in bytes. Example: 557.0.
        internal_date (Optional[str]): The date and time when the email was received by Gmail. Example: 1737460152000.
    """

    model_config = ConfigDict(extra="allow")

    thread_id: Optional[str] = None
    snippet: Optional[str] = None
    history_id: Optional[str] = None
    label_ids: Optional[list[str]] = None
    id: Optional[str] = None
    size_estimate: Optional[int] = None
    internal_date: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["ApplyGmailLabelResponse"], src_dict: Dict[str, Any]):
        return cls.model_validate(src_dict)

    @property
    def additional_keys(self) -> list[str]:
        base_fields = self.model_fields.keys()
        return [k for k in self.__dict__ if k not in base_fields]

    def __getitem__(self, key: str) -> Any:
        if key in self.__dict__:
            return self.__dict__[key]
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        self.__dict__[key] = value

    def __delitem__(self, key: str) -> None:
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        return key in self.__dict__
