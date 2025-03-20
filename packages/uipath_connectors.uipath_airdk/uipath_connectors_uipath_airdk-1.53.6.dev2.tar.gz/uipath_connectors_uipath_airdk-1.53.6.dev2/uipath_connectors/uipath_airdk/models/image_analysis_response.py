from typing import Any, Dict, Type, Optional
from pydantic import BaseModel, ConfigDict

from ..models.image_analysis_response_choices_array_item_ref import (
    ImageAnalysisResponseChoicesArrayItemRef,
)
from ..models.image_analysis_response_usage import ImageAnalysisResponseUsage


class ImageAnalysisResponse(BaseModel):
    """
    Attributes:
        choices (Optional[list['ImageAnalysisResponseChoicesArrayItemRef']]):
        usage (Optional[ImageAnalysisResponseUsage]):
        created (Optional[int]): The Created Example: 1.709197578E9.
        model (Optional[str]): The name or ID of the model or deployment to use for the chat completion Example:
            gpt-35-turbo-16k.
        id (Optional[str]): The ID Example: chatcmpl-8xWeoCeGSDzgCUaMs3edg3X6n78PP.
        text (Optional[str]): The image analysis completion text Example: UiPath is widely considered to be the leading
            organization in the field of Robotic Process Automation (RPA). It offers a comprehensive RPA platform that
            enables businesses to automate repetitive tasks, streamline processes, and improve operational efficiency.
            UiPath has gained significant.
        object_ (Optional[str]): The Object Example: chat.completion.
        total_tokens (Optional[int]): The count of total tokens processed in the request Example: 912.0.
        completion_tokens (Optional[int]): The number of tokens the model is allowed to use for generating the
            completion Example: 259.0.
        prompt_tokens (Optional[int]): The number of tokens used in the prompt for generating the completion Example:
            653.0.
    """

    model_config = ConfigDict(extra="allow")

    choices: Optional[list["ImageAnalysisResponseChoicesArrayItemRef"]] = None
    usage: Optional["ImageAnalysisResponseUsage"] = None
    created: Optional[int] = None
    model: Optional[str] = None
    id: Optional[str] = None
    text: Optional[str] = None
    object_: Optional[str] = None
    total_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    prompt_tokens: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls: Type["ImageAnalysisResponse"], src_dict: Dict[str, Any]):
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
