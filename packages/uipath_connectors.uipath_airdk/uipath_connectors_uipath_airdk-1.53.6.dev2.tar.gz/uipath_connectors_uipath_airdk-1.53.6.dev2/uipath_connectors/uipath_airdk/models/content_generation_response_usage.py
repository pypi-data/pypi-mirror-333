from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class ContentGenerationResponseUsage(BaseModel):
    """
    Attributes:
        total_tokens (Optional[int]): The Usage total tokens Example: 84.0.
        prompt_tokens (Optional[int]): The Usage prompt tokens Example: 34.0.
        completion_tokens (Optional[int]): The Usage completion tokens Example: 50.0.
    """

    model_config = ConfigDict(extra="allow")

    total_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["ContentGenerationResponseUsage"], src_dict: Dict[str, Any]
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
