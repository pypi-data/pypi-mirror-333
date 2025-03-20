from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class GetUserByEmailResponseProfile(BaseModel):
    """
    Attributes:
        avatar_hash (Optional[str]):  Example: g6d998d80169.
        display_name (Optional[str]):
        display_name_normalized (Optional[str]):
        email (Optional[str]):  Example: dhandu1995@gmail.com.
        huddle_state (Optional[str]):  Example: default_unset.
        image_192 (Optional[str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=192&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-192.png.
        image_24 (Optional[str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=24&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-24.png.
        image_32 (Optional[str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=32&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-32.png.
        image_48 (Optional[str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=48&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-48.png.
        image_512 (Optional[str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=512&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-512.png.
        image_72 (Optional[str]):  Example:
            https://secure.gravatar.com/avatar/6d998d801691b9d9198fe83d3f77c9f7.jpg?s=72&d=https%3A%2F%2Fa.slack-
            edge.com%2Fdf10d%2Fimg%2Favatars%2Fava_0025-72.png.
        phone (Optional[str]):
        real_name (Optional[str]):  Example: dhandu1995.
        real_name_normalized (Optional[str]):  Example: dhandu1995.
        skype (Optional[str]):
        status_emoji (Optional[str]):
        status_expiration (Optional[int]):  Example: 0.0.
        status_text (Optional[str]):
        status_text_canonical (Optional[str]):
        team (Optional[str]):  Example: T01G1P7CKR8.
        title (Optional[str]):
    """

    model_config = ConfigDict(extra="allow")

    avatar_hash: Optional[str] = None
    display_name: Optional[str] = None
    display_name_normalized: Optional[str] = None
    email: Optional[str] = None
    huddle_state: Optional[str] = None
    image_192: Optional[str] = None
    image_24: Optional[str] = None
    image_32: Optional[str] = None
    image_48: Optional[str] = None
    image_512: Optional[str] = None
    image_72: Optional[str] = None
    phone: Optional[str] = None
    real_name: Optional[str] = None
    real_name_normalized: Optional[str] = None
    skype: Optional[str] = None
    status_emoji: Optional[str] = None
    status_expiration: Optional[int] = None
    status_text: Optional[str] = None
    status_text_canonical: Optional[str] = None
    team: Optional[str] = None
    title: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["GetUserByEmailResponseProfile"], src_dict: Dict[str, Any]):
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
