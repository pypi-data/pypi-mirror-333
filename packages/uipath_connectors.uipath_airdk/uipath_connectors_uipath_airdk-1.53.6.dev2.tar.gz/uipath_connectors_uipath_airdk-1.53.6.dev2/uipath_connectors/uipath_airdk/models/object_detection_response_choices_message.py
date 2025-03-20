from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict


class ObjectDetectionResponseChoicesMessage(BaseModel):
    """
    Attributes:
        content (Optional[str]): The actual content of the message returned in the API response. Example: {
              "detected_entities": [
                {
                  "name": "Package",
                  "detected": "Yes",
                  "details": "Multiple packages are placed in front of the doorstep, clearly visible and accessible."
                },
                {
                  "name": "Doorstep",
                  "detected": "No",
                  "details": "The doorstep is partially blocked by multiple packages."
                }
              ]
            }.
        role (Optional[str]): Specifies the role or category of the detected object in the image. Example: assistant.
    """

    model_config = ConfigDict(extra="allow")

    content: Optional[str] = None
    role: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(
        cls: Type["ObjectDetectionResponseChoicesMessage"], src_dict: Dict[str, Any]
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
