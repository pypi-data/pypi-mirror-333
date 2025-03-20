from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.send_message_response_blocks_text import SendMessageResponseBlocksText


class SendMessageResponseBlocksArrayItemRef(BaseModel):
    """
    Attributes:
        block_id (Optional[str]):  Example: ZU=Pr.
        text (Optional[SendMessageResponseBlocksText]):
        type_ (Optional[str]):  Example: section.
    """

    model_config = ConfigDict(extra="allow")

    block_id: Optional[str] = None
    text: Optional["SendMessageResponseBlocksText"] = None
    type_: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["SendMessageResponseBlocksArrayItemRef"], src_dict: Dict[str, Any]
    ):
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
