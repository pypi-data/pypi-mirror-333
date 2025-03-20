from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_button_response_request_formatting_options_parse import (
    SendButtonResponseRequestFormattingOptionsParse,
)
from ..models.send_button_response_request_response_type import (
    SendButtonResponseRequestResponseType,
)


class SendButtonResponseRequest(BaseModel):
    """
    Attributes:
        response_url (str): Response URL Example: https://hooks.slack.com/actions/YESZCJHUD/34249/cd9WjkruWmXOA.
        response_type (SendButtonResponseRequestResponseType): In channel posts a normal chat message; ephemeral posts
            message only visible to user. Example: ephemeral.
        text (str): The formatted text of the message to be sent. This is also same as the 'block' section text Example:
            Would you like to play a game?.
        replace_original (Optional[bool]): Replace the original message with this message? Example: True.
        delete_original (Optional[bool]): Delete the original message so that a new message is posted in the channel
            Example: True.
        image (Optional[str]): The URL of the secondary image attachment to be shared as part of the message. The image
            will always be at the bottom of the entire message block Example: string.
        parse (Optional[SendButtonResponseRequestFormattingOptionsParse]): Change how messages are treated. Pass 'none'
            for removing hyperlinks and pass 'full' to ignore slack's default formatting Example: none.
    """

    model_config = ConfigDict(extra="allow")

    response_url: str
    response_type: SendButtonResponseRequestResponseType
    text: str
    replace_original: Optional[bool] = None
    delete_original: Optional[bool] = None
    image: Optional[str] = None
    parse: Optional[SendButtonResponseRequestFormattingOptionsParse] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["SendButtonResponseRequest"], src_dict: Dict[str, Any]):
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
