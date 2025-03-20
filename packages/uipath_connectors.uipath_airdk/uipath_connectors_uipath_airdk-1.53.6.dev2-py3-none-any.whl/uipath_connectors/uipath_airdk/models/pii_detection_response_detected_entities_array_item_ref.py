from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class PIIDetectionResponseDetectedEntitiesArrayItemRef(BaseModel):
    """
    Attributes:
        identifier (Optional[str]): Detected entities identifier Example: PhoneNumber-19.
        text (Optional[str]): Detected entities text Example: 312-555-1234.
        confidence_score (Optional[float]): The Detected entities confidence score Example: 0.8.
    """

    model_config = ConfigDict(extra="allow")

    identifier: Optional[str] = None
    text: Optional[str] = None
    confidence_score: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["PIIDetectionResponseDetectedEntitiesArrayItemRef"],
        src_dict: Dict[str, Any],
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
