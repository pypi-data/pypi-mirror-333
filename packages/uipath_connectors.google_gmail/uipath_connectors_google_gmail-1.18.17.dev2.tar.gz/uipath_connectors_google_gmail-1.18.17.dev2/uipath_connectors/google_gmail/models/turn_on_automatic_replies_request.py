from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

import datetime


class TurnOnAutomaticRepliesRequest(BaseModel):
    """
    Attributes:
        response_subject (str): The subject line used for the automatic reply email.
        response_body_plain_text (Optional[str]): The text content of the automatic reply.
        restrict_to_contacts (Optional[bool]): Limit automatic replies to only those in your contacts list.
        start_time (Optional[datetime.datetime]): The date and time when automatic replies will begin. Example:
            1737527373.
        end_time (Optional[datetime.datetime]): The date and time when automatic replies will stop. Example: 1737527373.
        send_replies_outside_domain (Optional[bool]): Sends replies to user who are outside users domain.
    """

    model_config = ConfigDict(extra="allow")

    response_subject: str
    response_body_plain_text: Optional[str] = None
    restrict_to_contacts: Optional[bool] = None
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    send_replies_outside_domain: Optional[bool] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["TurnOnAutomaticRepliesRequest"], src_dict: Dict[str, Any]):
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
