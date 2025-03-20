from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.send_button_response_request_formatting_options_parse import (
    SendButtonResponseRequestFormattingOptionsParse,
)
from ..models.send_button_response_request_response_type import (
    SendButtonResponseRequestResponseType,
)
from typing import Union


T = TypeVar("T", bound="SendButtonResponseRequest")


@_attrs_define
class SendButtonResponseRequest:
    """
    Attributes:
        response_url (str): Response URL Example: https://hooks.slack.com/actions/YESZCJHUD/34249/cd9WjkruWmXOA.
        response_type (SendButtonResponseRequestResponseType): In channel posts a normal chat message; ephemeral posts
            message only visible to user. Example: ephemeral.
        text (str): The formatted text of the message to be sent. This is also same as the 'block' section text Example:
            Would you like to play a game?.
        replace_original (Union[Unset, bool]): Replace the original message with this message? Example: True.
        delete_original (Union[Unset, bool]): Delete the original message so that a new message is posted in the channel
            Example: True.
        image (Union[Unset, str]): The URL of the secondary image attachment to be shared as part of the message. The
            image will always be at the bottom of the entire message block Example: string.
        parse (Union[Unset, SendButtonResponseRequestFormattingOptionsParse]): Change how messages are treated. Pass
            'none' for removing hyperlinks and pass 'full' to ignore slack's default formatting Example: none.
    """

    response_url: str
    response_type: SendButtonResponseRequestResponseType
    text: str
    replace_original: Union[Unset, bool] = UNSET
    delete_original: Union[Unset, bool] = UNSET
    image: Union[Unset, str] = UNSET
    parse: Union[Unset, SendButtonResponseRequestFormattingOptionsParse] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        response_url = self.response_url

        response_type = self.response_type.value

        text = self.text

        replace_original = self.replace_original

        delete_original = self.delete_original

        image = self.image

        parse: Union[Unset, str] = UNSET
        if not isinstance(self.parse, Unset):
            parse = self.parse.value

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "response_url": response_url,
                "response_type": response_type,
                "text": text,
            }
        )
        if replace_original is not UNSET:
            field_dict["replace_original"] = replace_original
        if delete_original is not UNSET:
            field_dict["delete_original"] = delete_original
        if image is not UNSET:
            field_dict["image"] = image
        if parse is not UNSET:
            field_dict["parse"] = parse

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: dict[str, Any]) -> T:
        d = src_dict.copy()
        response_url = d.pop("response_url")

        response_type = SendButtonResponseRequestResponseType(d.pop("response_type"))

        text = d.pop("text")

        replace_original = d.pop("replace_original", UNSET)

        delete_original = d.pop("delete_original", UNSET)

        image = d.pop("image", UNSET)

        _parse = d.pop("parse", UNSET)
        parse: Union[Unset, SendButtonResponseRequestFormattingOptionsParse]
        if isinstance(_parse, Unset):
            parse = UNSET
        else:
            parse = SendButtonResponseRequestFormattingOptionsParse(_parse)

        send_button_response_request = cls(
            response_url=response_url,
            response_type=response_type,
            text=text,
            replace_original=replace_original,
            delete_original=delete_original,
            image=image,
            parse=parse,
        )

        send_button_response_request.additional_properties = d
        return send_button_response_request

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
